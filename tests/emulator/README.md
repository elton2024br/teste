# Testes no emulador

O runner usa a biblioteca nativa do mGBA. Os testes abaixo validam a introdução e a escolha dos parceiros; não equivalem a completar a missão da pedra com cada um.

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

## Save normal

```bash
tests/emulator/runner pokefirered/pokefirered_rev1.gba \
  --save /tmp/bichos-teste.sav \
  --symbols tests/emulator/current-symbols.txt
```

`run MASCARA FRAMES` controla as teclas (A=1, B=2, Start=8, direita=16, esquerda=32, cima=64, baixo=128). Salve pelo menu do jogo, aguarde a mensagem de conclusão e use `quit`. Depois inicie outro processo com o mesmo `--save`, escolha Continue, termine a retrospectiva e confira `progress`.

O runner entrega o arquivo ao mecanismo nativo de save do mGBA e fecha o core normalmente. O antigo `flushsave`, que tentava clonar os dados e truncar o arquivo ainda em uso, foi removido do fluxo; chamá-lo dá um erro explícito e passa pela limpeza do core. Não o use para validar persistência.

`save CAMINHO` e `load CAMINHO` continuam disponíveis apenas para estados do emulador. Suas respostas são STATE_SAVED/STATE_LOADED para distingui-los de saves normais. Eles não comprovam persistência pelo menu.

`progress` resolve gSaveBlock1Ptr e gPlayerPartyCount do arquivo de símbolos, seguindo o ponteiro atual após transições. Os offsets da estrutura e flags correspondem ao código FireRed fixado neste projeto e precisam acompanhar qualquer alteração futura desse layout.
