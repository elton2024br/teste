# Testes no emulador

O runner usa a biblioteca nativa do mGBA. Os testes abaixo cobrem introdução, escolha/save dos parceiros, derrota/recuperação com Ararafogo e a missão da pedra com Ararafogo e Tatupedra. Não validam a campanha dos cinco habitats.

## Compilar e executar

Depois de compilar a ROM, instale o pacote de desenvolvimento do mGBA, se necessário (`libmgba-dev` em Debian/Ubuntu). Na raiz do repositório:

```bash
cc -std=gnu11 -Wall -Wextra -Werror tests/emulator/runner.c -lmgba -o tests/emulator/runner
arm-none-eabi-nm pokefirered/pokefirered_rev1.elf > tests/emulator/current-symbols.txt
python3 tests/emulator/check_starters.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --output "$(pwd)/tests/emulator/results/starters"
```

Use os símbolos do mesmo build da ROM. O teste começa um jogo novo em cada ramo, verifica ausência de concessão antes/depois do cancelamento, confirma o parceiro, confere o índice e a equipe, e repete o diálogo de suprimentos. Logs, capturas PPM e results.json ficam na pasta de saída, ignorada pelo Git.

A sequência de entradas da introdução foi gravada para a versão atual. Mudanças na introdução podem exigir atualização da sequência; as asserções devem continuar verificando o comportamento real.

## Intro amazônica

`check_intro.py` testa as duas aparências, nome personalizado, recusa do nome seguida de um nome diferente, nomes padrão quando o teclado fica em branco, Sam com identidade fixa e chegada à casa sem parceiro. Também salva pelo menu do jogo, fecha o processo e confere Continue/identidade em outro processo. Execute com uma pasta de saída nova para evitar reaproveitar saves:

```bash
python3 tests/emulator/check_intro.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --output "$(pwd)/tests/emulator/results/intro-nova-execucao"
```

Esse ciclo de save acontece na casa, antes da escolha do parceiro. Não substitui um teste integral da missão. Os relatórios atuais estão em `docs/intro-validation.json` e `docs/intro-starter-regression-results.json`; o relatório anterior de parceiros foi preservado como histórico.

## Captura e consumo de cápsulas

```bash
python3 tests/emulator/check_capture.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --output "$(pwd)/tests/emulator/results/capture-nova-execucao"
```

Use uma pasta vazia. O cenário gravado começa um jogo novo com Capivágua, recebe as cinco cápsulas, encontra Tatupedra de nível 3 na grama da Route1, enfraquece com Tackle e tenta capturar pela bolsa. Exige `B_OUTCOME_CAUGHT`, equipe com dois animais e redução das cápsulas igual ao número de lançamentos. Salva pelo menu e reabre Continue em outro processo, conferindo equipe, nome/nível da captura, cápsulas, flags e posição. Nenhum item, criatura, HP, RNG ou resultado é injetado; estados do emulador não são usados no teste.

Esse é um caso com entradas e pausas fixas, dependente do build e do ritmo atual do RNG. Mudanças no fluxo podem exigir nova gravação; falhas de captura não devem ser convertidas em PASS. Não mede taxa de captura nem valida outras espécies, equipe cheia/envio ao PC, inventário cheio ou todos os ramos de falha. Veja `docs/capture-validation.json`.

## Missão da Pedra das Águas

```bash
python3 tests/emulator/check_mission.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --output "$(pwd)/tests/emulator/results/mission-nova-execucao"
```

Use uma pasta vazia. O teste começa jogos novos com Ararafogo e Tatupedra, confirma o controle bloqueado, vence o agente, ativa o controle, atravessa a ponte, recebe a pedra e retorna ao guia na vila. Salva pelo menu e confere parceiro, equipe, flags, item e posição por Continue em outro processo. A estratégia seleciona o segundo ataque no menu de batalha, consultando o handler e o cursor pelos símbolos do ELF; não escreve na memória nem usa savestates. Uma derrota ou limite de espera excedido falha o teste. Isso não valida captura, inventário cheio ou quantidade/duplicação da pedra.

## Revisita à pedra e ao cuidador

Depois de executar `check_mission.py` no build atual, use a pasta de resultados dele como entrada:

```bash
python3 tests/emulator/check_stone_revisit.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --mission-results "$(pwd)/tests/emulator/results/mission-nova-execucao" \
  --output "$(pwd)/tests/emulator/results/stone-revisit-nova-execucao"
```

O teste exige uma saída vazia e fixtures do mesmo hash de ROM. Copia os saves nativos de Ararafogo e Tatupedra para preservar os originais, carrega Continue e caminha de volta pela ponte. Confere todos os 30 slots de itens especiais, decifrando as quantidades pela chave do save. A pedra deve ocupar um único slot, com quantidade 1, antes e depois de três tentativas de interação no antigo local e três interações com o cuidador. Não usa escrita de memória ou estados do emulador. Não cobre mochila cheia, reposição de pedra ausente, captura nem um novo ciclo de save após as revisitas.

## Fixtures artificiais: reposição da pedra e bolsa cheia

```bash
python3 tests/emulator/check_stone_repair.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --mission-results "$(pwd)/tests/emulator/results/mission-nova-execucao" \
  --output "$(pwd)/tests/emulator/results/stone-repair-nova-execucao"
```

**Este teste prepara estados artificiais por escrita de memória.** Não é evidência de uma mochila enchida ou de uma pedra perdida em gameplay natural. Exige fixtures de `check_mission.py` do mesmo build, copia o save de Ararafogo e preserva o original. Com a flag da pedra já obtida, prepara dois cenários: bolsa especial vazia e 30 itens especiais distintos sem a pedra. O cuidador deve repor uma pedra no primeiro, recusar sem alterar os itens no segundo e repor após liberar exatamente um slot. Uma nova interação não pode duplicar a pedra. Salva pelo menu (incluindo confirmação de sobrescrita), fecha e reabre Continue para conferir toda a bolsa e o progresso.

O runner só aceita `write32 ENDERECO VALOR` com `--test-writes enabled`, em EWRAM alinhada; o comando responde `TEST_WRITE32`. Os logs das sessões artificiais têm um cabeçalho explícito. O teste confere a recusa sem opt-in, para endereço de ROM e para endereço desalinhado. Reabre Continue sem habilitar escritas. Os testes anteriores continuam com esse modo desabilitado por padrão.

Relatório: `docs/stone-repair-validation.json`. Não cobre a aquisição pelo objeto da pedra com a bolsa cheia, outros bolsos nem acesso natural aos estados preparados.

## Derrota e recuperação

```bash
python3 tests/emulator/check_defeat_recovery.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --output "$(pwd)/tests/emulator/results/defeat-recovery-nova-execucao"
```

Use uma pasta vazia. O teste começa um jogo novo com Ararafogo, confere o bloqueio do rio e do controle, enfrenta o agente usando o primeiro ataque até perder, e verifica retorno à casa, HP restaurado e flags sem liberação indevida. Salva pelo menu SALVAR, fecha o emulador e carrega Continue em outro processo, comparando posição, parceiro, equipe, flags, item da pedra e HP. Depois caminha novamente até o controle e confirma que continua bloqueado e que o jogador consegue se mover ao fechar o diálogo. Só usa entradas de controle e leituras de memória; não injeta derrota, HP ou flags. Asserções de posição e HP usam os layouts das estruturas do código FireRed fixado; os endereços vêm do ELF atual. O cenário de derrota depende da sequência e do balanceamento atuais: uma vitória inesperada é falha do teste, não é registrada como recuperação aprovada.

O arquivo nativo de save e as capturas permanecem na pasta de resultados ignorada pelo Git. Esse caso não certifica vitória, captura, inventário cheio, save após obter a pedra nem recuperação com os outros parceiros.

## Save normal

Para verificar save/Continue na vila após receber cada um dos três parceiros e os suprimentos:

```bash
python3 tests/emulator/check_partner_saves.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --output "$(pwd)/tests/emulator/results/partner-saves-nova-execucao"
```

Use uma pasta de saída nova. Cada caso salva pelo menu SALVAR, encerra o processo e abre outro com o mesmo arquivo nativo. O teste compara parceiro, índice escolhido, equipe, flags e localização na vila, e repete a interação com o guia após Continue para conferir que não há duplicação. Os arquivos `.sav`, logs e capturas ficam na pasta de resultados ignorada pelo Git. Isso não valida captura, derrota, inventário cheio nem save depois de obter a pedra.

Para uma sessão manual:

```bash
tests/emulator/runner pokefirered/pokefirered_rev1.gba \
  --save /tmp/bichos-teste.sav \
  --symbols tests/emulator/current-symbols.txt
```

`run MASCARA FRAMES` controla as teclas (A=1, B=2, Start=8, direita=16, esquerda=32, cima=64, baixo=128). Salve pelo menu do jogo, aguarde a mensagem de conclusão e use `quit`. Depois inicie outro processo com o mesmo `--save`, escolha Continue, termine a retrospectiva e confira `progress`.

O runner entrega o arquivo ao mecanismo nativo de save do mGBA e fecha o core normalmente. O antigo `flushsave`, que tentava clonar os dados e truncar o arquivo ainda em uso, foi removido do fluxo; chamá-lo dá um erro explícito e passa pela limpeza do core. Não o use para validar persistência.

`save CAMINHO` e `load CAMINHO` continuam disponíveis apenas para estados do emulador. Suas respostas são STATE_SAVED/STATE_LOADED para distingui-los de saves normais. Eles não comprovam persistência pelo menu.

`progress` resolve gSaveBlock1Ptr e gPlayerPartyCount do arquivo de símbolos, seguindo o ponteiro atual após transições. Os offsets da estrutura e flags correspondem ao código FireRed fixado neste projeto e precisam acompanhar qualquer alteração futura desse layout.
