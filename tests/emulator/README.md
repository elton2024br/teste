# Testes no emulador

O runner usa a biblioteca nativa do mGBA. Os testes abaixo cobrem introdução, escolha/save dos parceiros, derrota/recuperação dos três parceiros e a campanha mínima dos cinco habitats até o desfecho com os três parceiros. Cada teste declara seus limites; isso não certifica arte, balanceamento ou acabamento final.

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

## Diálogo normal da mãe e descanso

```bash
python3 tests/emulator/check_mom_dialogue.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --output "$(pwd)/tests/emulator/results/mom-dialogue-nova-execucao"
```

Use uma pasta vazia. Nas duas aparências, o teste começa um jogo novo, conversa com a mãe antes da escolha, sai normalmente e recebe Capivágua e as cápsulas pela guia. Confere ausência de concessão prematura e volta para casa, onde o descanso deve estar disponível pela flag de parceiro escolhido. **Somente nessa etapa prepara HP=1 artificialmente**, usando escrita opt-in no campo não cifrado de HP; nenhuma flag, parceiro ou item é injetado. A conversa normal deve restaurar HP completo, preservar os cinco suprimentos e liberar movimento.

As capturas conferidas estão em `docs/screenshots/mom-dialogue/preview.png`, e o relatório em `docs/mom-dialogue-validation.json`. Não comprova dano recebido em batalha natural, recuperação de status/PP, todos os tamanhos de equipe ou um novo ciclo de save.

## Captura e consumo de cápsulas

```bash
python3 tests/emulator/check_capture.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --output "$(pwd)/tests/emulator/results/capture-nova-execucao"
```

Use uma pasta vazia. O cenário gravado começa um jogo novo com Capivágua, recebe as cinco cápsulas, encontra Tatupedra de nível 3 na grama da Route1, enfraquece com Tackle e tenta capturar pela bolsa. Exige `B_OUTCOME_CAUGHT`, equipe com dois animais e redução das cápsulas igual ao número de lançamentos. Salva pelo menu e reabre Continue em outro processo, conferindo equipe, nome/nível da captura, cápsulas, flags e posição. Nenhum item, criatura, HP, RNG ou resultado é injetado; estados do emulador não são usados no teste.

Esse é um caso com entradas e pausas fixas, dependente do build e do ritmo atual do RNG. O padrão usa Capivágua e encontra Tatupedra nível 3; `--partner ararafogo` seleciona Ararafogo e encontra Tatupedra nível 2. `--partner tatupedra --capture-delay-frames 90` usa Mud-Slap, espera normalmente 90 frames e captura Ararafogo nível 4. A pausa apenas avança o jogo: não escreve RNG, HP ou resultado. Mudanças no fluxo podem exigir nova gravação; falhas de captura não devem ser convertidas em PASS. Não mede taxa de captura nem valida inventário cheio ou todos os ramos de falha. Veja `docs/capture-validation.json`, `docs/natural-ararafogo-two-member-campaign-validation.json` e `docs/natural-tatupedra-two-member-campaign-validation.json`.

Para continuar a captura natural pela campanha, passe essa saída a `check_captured_first_mission.py`:

```bash
python3 tests/emulator/check_captured_first_mission.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --capture-results "$(pwd)/tests/emulator/results/capture-nova-execucao" \
  --output "$(pwd)/tests/emulator/results/missao-natural-dois-membros"
```

O teste retorna pela Route 1, usa normalmente a cura do cuidador, enfrenta o primeiro agente, trata a troca obrigatória se o líder desmaiar, recebe a Pedra das Águas e sobrescreve o save pelo menu. Ele lê o parceiro do relatório de captura e produz `capivagua.sav`, `ararafogo.sav` ou `tatupedra.sav` conforme o caso. A saída tem o mesmo formato consumido por `check_second_habitat.py`; encadeie os demais habitats e `check_campaign_ending.py` como descrito abaixo. Personalidade, ID do treinador, espécie e nome dos dois membros são comparados depois de cada recompensa e Continue. Nenhum desses testes habilita escrita de memória ou usa savestate. Relatórios: `docs/natural-two-member-campaign-validation.json` e `docs/natural-ararafogo-two-member-campaign-validation.json`.

Os fluxos validados cobrem Capivágua ou Ararafogo com Tatupedra capturado e Tatupedra com Ararafogo capturado. Não representam estatística de captura, todas as duplas, estratégia otimizada de troca ou balanceamento final.

Para o caso de equipe cheia, mantenha o parceiro padrão Capivágua, acrescente `--full-party-fixture` e use outra pasta vazia. **A equipe cheia é artificial**: o runner recebe opt-in de escrita para copiar o parceiro válido nos cinco slots restantes e ajustar a contagem para seis. Não injeta criaturas no PC, cápsulas, alvo selvagem, HP, RNG ou resultado da captura. O encontro/captura usa controles normais; deve deixar seis animais na equipe e exatamente um na primeira caixa, sem modificar os cinco slots de reserva. A criatura armazenada é conferida por espécie, nome, experiência e checksum dos dados cifrados. Save normal/Continue deve preservar tudo; o processo de Continue tem escritas desabilitadas. Relatório: `docs/full-party-capture-validation.json`.

Esse caso confere envio ao PC por leitura de dados e persistência; não valida obtenção natural de seis animais, retirada pela interface do PC, caixa cheia ou todos os caminhos de armazenamento.

## Posto da vila: guardar e retirar pela interface

O posto provisório fica em (13,16), perto do cuidador, e abre o armazenamento após a escolha do parceiro. Para testar, gere primeiro um save com `check_capture.py --full-party-fixture` no build atual, usando a saída `tests/emulator/results/capture-equipe-cheia`. Depois:

```bash
python3 tests/emulator/check_village_pc.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --capture-results "$(pwd)/tests/emulator/results/capture-equipe-cheia" \
  --output "$(pwd)/tests/emulator/results/village-pc-nova-execucao"
```

O teste exige saída vazia e fixture do mesmo hash de ROM. Confere o bloqueio antes de escolher parceiro e, depois de obter um parceiro por controles normais, verifica a recusa de guardar o último membro e captura as cinco opções/descrições. No save de equipe cheia, confere a recusa de retirada com seis membros, guarda um Capivágua e retira Tatupedra. Verifica contagens, espécie, experiência, identidade/checksum e preservação dos sete animais entre equipe/PC, além de save normal/Continue. O teste da interface não habilita escritas nem usa savestates; o save de origem é copiado e preservado. A equipe cheia de origem continua sendo artificial.

O fluxo também abre/fecha Resumo e cancela a confirmação de Libertar, comparando os dados antes de prosseguir com a retirada. Nenhum animal é libertado nesse teste. A pergunta de saída é capturada antes de escolher sair das caixas.

Relatório: `docs/village-pc-validation.json`; capturas revisadas em `docs/screenshots/village-pc/preview.png` e `docs/screenshots/box-actions/preview.png`. Menu principal, rótulos do menu de ações e os avisos exercitados estão em português; a revisão visual não é uma validação automática de todo o texto ou de todos os nomes. Não cobre libertação efetiva, PC cheio, operações de mover parceiros/itens, todas as caixas ou obtenção natural dos seis membros. A placa, títulos gráficos, conteúdo do resumo e parte das mensagens ainda usam recursos provisórios/herdados; a interface interna não está totalmente traduzida.

## Libertar: confirmação em cópia isolada

Depois de gerar a origem com `check_capture.py --full-party-fixture` no build atual:

```bash
python3 tests/emulator/check_village_release.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --capture-results "$(pwd)/tests/emulator/results/capture-equipe-cheia" \
  --output "$(pwd)/tests/emulator/results/village-release-nova-execucao"
```

Exige saída vazia e origem do mesmo hash de ROM. O teste copia o save e opera somente em `isolated-release.sav`: guarda um Capivágua, cancela Libertar para conferir preservação e depois seleciona SIM explicitamente para libertar apenas Tatupedra da caixa. Confere que o slot foi zerado e os outros seis animais, dados, progresso e quatro cápsulas permanecem intactos. Salva pelo menu e reabre Continue na cópia; verifica por hash que a origem não mudou.

A origem tem equipe cheia artificial, mas o teste de interface não habilita escritas nem usa savestates. Relatório em `docs/village-release-validation.json` e capturas revisadas em `docs/screenshots/release/preview.png`. Não cobre libertação de membro da equipe, recusa por ovo/HM, todos os apelidos ou todos os caminhos. As mensagens de sucesso/despedida estão em português; outros avisos e títulos da interface ainda são herdados.

## Missão da Pedra das Águas

```bash
python3 tests/emulator/check_mission.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --output "$(pwd)/tests/emulator/results/mission-nova-execucao"
```

Use uma pasta vazia. O teste começa jogos novos com Ararafogo e Tatupedra, confirma o controle bloqueado, vence o agente, ativa o controle, atravessa a ponte, recebe a pedra e retorna ao guia na vila. Salva pelo menu e confere parceiro, equipe, flags, item e posição por Continue em outro processo. A estratégia seleciona o segundo ataque no menu de batalha, consultando o handler e o cursor pelos símbolos do ELF; não escreve na memória nem usa savestates. Uma derrota ou limite de espera excedido falha o teste. Isso não valida captura, inventário cheio ou quantidade/duplicação da pedra.

Para rodar somente Capivágua, acrescente `--partners capivagua` e use uma pasta de saída nova. Também é possível selecionar parceiros por nome com `--partners`; o padrão continua Ararafogo e Tatupedra para preservar os consumidores de fixtures existentes, que exigem essa dupla. A validação isolada de Capivágua está em `docs/capivagua-mission-validation.json`; os dois outros ramos estão em `docs/mission-current-validation.json`.

## Segundo ao quinto habitat

Depois de gerar os três saves com `check_mission.py`, execute `check_second_habitat.py` uma vez por parceiro, passando `--first-mission-results`, `--partner` e uma pasta de saída vazia. Encadeie então `check_third_habitat.py`, `check_fourth_habitat.py`, `check_fifth_habitat.py` e `check_campaign_ending.py`, sempre usando o resultado da etapa anterior, o mesmo parceiro e outra saída vazia.

Os testes percorrem Campo Cerrado, Caatinga, Mata Atlântica, Pantanal e Terras Raras, conferem os cinco itens especiais, exigem HP máximo depois de cada recompensa e enfrentam Lobo-guará, Asa-branca, Mico-leão, Tuiuiú e Onça-pintada. Os testes dos habitats e do desfecho capturam a primeira seleção de golpe contra cada adversário próprio. `check_campaign_ending.py` percorre a faixa de solo seco ao lado da lagoa, interage com os cinco marcos originais, captura a resolução antes da transformação e a mensagem final depois da revelação do santuário. Após save/Continue, ele cancela uma visita, aceita o retorno opcional à vila em outra, compara pedras, flags e identidade, percorre novamente os cinco habitats e visita o santuário pela terceira vez; cada etapa deve liberar os controles. Todos exigem fixtures do mesmo hash da ROM, preservam a origem e não habilitam escritas nem usam savestates. Estes testes de vitória não cobrem mochila cheia, estratégias otimizadas, balanceamento final, créditos ou arte final; as regressões de derrota cobertas estão descritas separadamente abaixo.

O mesmo teste exige e captura o epílogo posterior à revelação do santuário, verificando que o controle continua bloqueado durante a mensagem e volta ao jogador ao final. Depois interage com a guia, recusa e aceita a viagem opcional de volta ao santuário, retorna novamente à vila e só então atravessa os habitats pelo caminho normal. Assim, encerramento, dois sentidos e exploração sem atalho permanecem cobertos.

Para validar recuperação de uma equipe maior, acrescente `--recovery-fixture` a cada teste do segundo ao quinto habitat e encadeie as saídas normalmente. A primeira etapa clona o parceiro válido no segundo slot; antes de cada percurso de habitat, a fixture opt-in reduz o HP dos dois membros, aplica veneno somente ao segundo e reduz PP cifrado, recalculando o checksum. Batalhas, recompensas, saves e Continue continuam acontecendo pelas regras e entradas normais. Cada recompensa deve restaurar HP, status e PP dos dois membros, e o processo novo de Continue deve preservar o resultado. Encadeie por fim `check_campaign_ending.py` sem a opção para comprovar a equipe de dois membros até o santuário. O relatório consolidado está em `docs/team-recovery-validation.json`.

A equipe de dois membros é sintética e usa duas cópias do parceiro, portanto não comprova captura natural, troca ou desmaio deliberado durante a batalha, seis membros ou condições além de veneno. Escritas são habilitadas somente no processo que prepara a condição; os processos de Continue permanecem sem escrita, e cada save de origem é conferido por hash.

## Derrota no chefe e nova tentativa

Depois de gerar o resultado do quinto habitat para um parceiro, execute `check_campaign_final_defeat.py` com `--fifth-habitat-results`, `--partner` e uma saída vazia. Repita para os três parceiros. O teste copia o save e prepara somente HP=1 no primeiro membro por escrita opt-in; não escreve flags, itens, parceiro ou resultado. A derrota deve ocorrer normalmente, retornar à casa, restaurar HP e preservar as cinco pedras sem marcar o final. Em seguida salva sobre a cópia, abre Continue com escritas desativadas, percorre novamente todos os habitats e vence Tio Sam.

Para uma saída natural de dois membros, acrescente `--all-party-hp-fixture`. O teste exige exatamente dois membros, prepara HP=1 em ambos e trata pela interface a troca obrigatória após a queda do líder. Depois da derrota, exige HP, status e PP restaurados nos dois membros, além de personalidade, ID do treinador, espécie e nome preservados antes e depois de Continue e da revanche. A preparação continua limitada ao HP atual; flags, itens, identidades e resultados não são escritos.

Relatórios: `docs/campaign-final-defeat-validation.json` para a matriz original e `docs/natural-two-member-final-defeat-validation.json` para Capivágua com Tatupedra capturado. A fixture não comprova dano acumulado naturalmente, todas as composições de equipe, agentes intermediários ou todos os caminhos de recuperação.

`check_fifth_habitat_defeat.py` aplica a mesma fixture ao agente do Pantanal, partindo do resultado do quarto habitat. A derrota deve preservar as quatro pedras e deixar tanto a flag de vitória quanto a Pedra das Cheias pendentes. Depois de save/Continue com escritas desativadas, o teste retorna pelos habitats anteriores, vence normalmente e exige a quinta pedra e a recuperação total. Ele também aceita `--all-party-hp-fixture` para a equipe natural de dois membros, com as mesmas garantias de troca, recuperação e identidade do teste do chefe. Relatório: `docs/fifth-habitat-defeat-validation.json`.

`check_intermediate_habitat_defeat.py` cobre a mesma sequência no Cerrado, Caatinga e Mata Atlântica. Use `--stage second|third|fourth` e forneça em `--source-results` respectivamente a saída da primeira missão, do segundo habitat ou do terceiro habitat para o mesmo parceiro. O teste prepara somente HP=1, exige derrota sem conceder a pedra/flags pendentes, recuperação, save/Continue com escritas desativadas, retorno pelo percurso real, vitória e recompensa correta. `--all-party-hp-fixture` estende a sequência à equipe natural de dois membros. Nesse modo, os verificadores de vitória tratam e contam uma eventual troca obrigatória também na revanche. A matriz original dos três habitats com os três parceiros está resumida em `docs/intermediate-habitat-defeat-validation.json`; a cadeia natural de Capivágua nos cinco confrontos está em `docs/natural-two-member-defeat-matrix-validation.json`, e os quatro agentes intermediários com as três equipes naturais estão em `docs/natural-team-intermediate-defeat-matrix-validation.json`.

Essas fixtures não comprovam dano acumulado naturalmente, todas as composições de equipe, status infligido em batalha ou bolso especial cheio. Os saves de origem são preservados e conferidos por hash.

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

## Fixture artificial: coleta da pedra com bolsa cheia

```bash
python3 tests/emulator/check_stone_collection_full.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --mission-results "$(pwd)/tests/emulator/results/mission-nova-execucao" \
  --output "$(pwd)/tests/emulator/results/stone-collection-full-nova-execucao"
```

**Prepara um estado artificial**, copiando o save pós-missão de Ararafogo, preenchendo o bolso especial com 30 itens distintos e limpando somente a flag de obtenção da pedra antes de entrar no bosque. Vitória e controle liberado são preservados. Três tentativas normais de coleta devem manter a bolsa intacta, o objeto ativo e a flag não marcada. Depois de liberar artificialmente um slot, a interação deve conceder uma pedra, remover o objeto e preservar os outros 29 itens. Repetir a interação não pode duplicar o item.

O teste também salva pelo menu diretamente no bosque e abre Continue em outro processo com escritas desabilitadas: compara bolsa/progresso, confirma a ausência do objeto e atravessa a ponte. Usa uma saída vazia e resultados de missão do mesmo hash de ROM; preserva o save de origem. Não comprova acesso natural à bolsa cheia, outros parceiros/bolsos nem todos os caminhos de save. Relatório: `docs/stone-collection-full-validation.json`.

## Derrota e recuperação

```bash
python3 tests/emulator/check_defeat_recovery.py \
  --runner "$(pwd)/tests/emulator/runner" \
  --rom "$(pwd)/pokefirered/pokefirered_rev1.gba" \
  --symbols "$(pwd)/tests/emulator/current-symbols.txt" \
  --output "$(pwd)/tests/emulator/results/defeat-recovery-nova-execucao"
```

Use uma pasta vazia. O teste começa um jogo novo com Ararafogo, confere o bloqueio do rio e do controle, enfrenta o agente usando o primeiro ataque até perder, e verifica retorno à casa, HP restaurado e flags sem liberação indevida. Salva pelo menu SALVAR, fecha o emulador e carrega Continue em outro processo, comparando posição, parceiro, equipe, flags, item da pedra e HP. Depois caminha novamente até o controle e confirma que continua bloqueado e que o jogador consegue se mover ao fechar o diálogo. Só usa entradas de controle e leituras de memória; não injeta derrota, HP ou flags. Asserções de posição e HP usam os layouts das estruturas do código FireRed fixado; os endereços vêm do ELF atual. O cenário de derrota depende da sequência e do balanceamento atuais: uma vitória inesperada é falha do teste, não é registrada como recuperação aprovada.

Para os ramos restantes, acrescente `--partner capivagua --strategy trainer-balls` ou `--partner tatupedra --strategy trainer-balls`, sempre com uma pasta de saída nova. Essa estratégia tenta usar as cinco cápsulas contra o treinador e depois usa o primeiro ataque se necessário, até a derrota. Não força HP ou resultado; uma vitória inesperada falha o teste. O padrão permanece Ararafogo com o primeiro ataque. Relatórios dos novos ramos: `docs/defeat-capivagua-validation.json` e `docs/defeat-tatupedra-validation.json`; o relatório de Ararafogo está em `docs/defeat-recovery-validation.json`. Os três relatórios atuais foram gerados no build dos textos de recuperação em português.

O arquivo nativo de save e as capturas permanecem na pasta de resultados ignorada pelo Git. Cada execução cobre somente o parceiro/estratégia selecionados; não certifica vitória, captura, inventário cheio ou save após obter a pedra.

As capturas `defeat-*.ppm` e `recovery-*.ppm` registram a sequência para revisão visual. A prévia revisada está em `docs/screenshots/recovery/preview.png`; não é uma validação automática de todos os textos ou comprimentos de nome.

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
