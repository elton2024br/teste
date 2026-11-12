# Instrução atual para esta versão GitHub

O projeto está completo em termos de arquivos-fonte neste repositório. Use pokefirered/ e agbcc/ diretamente. Não clone uma segunda base e não aplique source.patch. As menções a ZIP, source.patch e project/ abaixo são históricas. Nesta estrutura project/docs = docs, project/tools = tools, project/assets = assets e project/tests = tests.

# ATENCAO: PACOTE DE CODIGO COMPLETO

A restauracao ja foi feita na nuvem. O conteudo abaixo conserva o historico e as pendencias, mas suas instrucoes de clonar e aplicar source.patch estao SUPERADAS: use diretamente a pasta pokefirered/ deste pacote e LEIA-PRIMEIRO.md. Nao repita a aplicacao do patch.

# Bichos do Brasil — ponto de retomada

## Retorno à casa em português

Foram adaptadas as mensagens de esgotamento/derrota em `src/battle_message.c`, o retorno para casa em `src/strings.c` e os dois diálogos automáticos da mãe em `data/text/white_out.inc`. As orientações agora explicam energia/HP e indicam descanso em casa ou ajuda gratuita do cuidador da vila, em vez da referência herdada ao Professor Oak e ao Centro Pokémon. O rótulo MAMAE segue o diálogo já existente da casa. Placeholders, perda de dinheiro e demais mecânicas foram preservados.

Build Linux PASS: SHA-1 `b89c8c560eae9d999b68fd22b6ace17409b2f913`, registrado em `SOURCE_STATE.json`; símbolos regenerados do ELF. Os testes completos de derrota/recuperação foram repetidos com os três parceiros no novo build: Ararafogo com primeiro ataque, Capivágua e Tatupedra com tentativas de cápsulas contra o treinador. Todos passaram: derrota, retorno à casa, HP completo (19/19, 21/21 e 22/22), flags `01`, ausência da pedra, save normal/Continue em outro processo e retorno ao controle ainda bloqueado. Os três relatórios `docs/defeat-*-validation.json` foram atualizados (Ararafogo usa `defeat-recovery-validation.json`).

O teste agora captura as páginas de derrota e recuperação, sem alterar as entradas do jogo. Revisão visual manual das telas de Ararafogo confirmou leitura e quebras de linha sem corte observado nas páginas capturadas; prévia em `docs/screenshots/recovery/preview.png`. As capturas completas e logs ficam em `tests/emulator/results/recovery-pt-{ararafogo,capivagua,tatupedra}-20261112/`, ignorados pelo Git. `py_compile` e `git diff --check` passaram. Nenhuma ROM ou save é publicada.

Escopo: retorno à casa após a derrota para o agente. A revisão não cobre todos os nomes possíveis, perdas em batalha selvagem/sem dinheiro, desmaio por veneno ou recuperação em Centro Pokémon; esses caminhos ainda contêm textos herdados. O símbolo monetário existente foi mantido. Relatórios de missão/captura/inventário anteriores continuam identificados pelo hash 2cd252b4dbb1926e28e89944333d5c7b033fa304; fixtures desses relatórios precisam ser regeneradas antes de usar testes que exigem o hash atual.

Próximo passo concreto: alinhar o diálogo normal da mãe com a escolha de parceiro pela guia na vila — ele ainda manda procurar um professor no laboratório. Equipe cheia/envio de captura ao PC e acabamento visual amazônico também permanecem pendentes.

## Derrota/recuperação — Capivágua e Tatupedra

`check_defeat_recovery.py` ganhou `--partner` e `--strategy`, preservando o padrão anterior de Ararafogo/primeiro ataque. Capivágua e Tatupedra passaram desde jogos novos com a estratégia `trainer-balls`: tentativas normais de cápsula contra o agente e primeiro ataque se necessário, sem escrita de memória, fixtures ou savestates. A derrota exigiu `B_OUTCOME_LOST = 2`; uma vitória inesperada é falha. Os dois retornaram à casa em (8,5), com parceiro/equipe preservados, HP cheio (21/21 e 22/22), flags `01` e nenhum item da pedra.

O save pelo menu SALVAR foi fechado e reaberto em outro processo em ambos os casos. Continue preservou parceiro, índice, flags, posição e HP. Foi possível sair normalmente da casa, caminhar de volta ao bosque, confirmar que o rio/controle permaneciam bloqueados e voltar a se mover após fechar o diálogo. Relatórios: `docs/defeat-capivagua-validation.json` e `docs/defeat-tatupedra-validation.json`.

Validações: `make -j4 firered_rev1` incremental PASS, SHA-1 inalterado `2cd252b4dbb1926e28e89944333d5c7b033fa304`, símbolos regenerados; os dois testes completos PASS em `tests/emulator/results/defeat-capivagua-20261112/` e `defeat-tatupedra-20261112/`; `py_compile` e `git diff --check` PASS. O ramo Ararafogo não foi repetido: seu relatório histórico usa o build `8c41ff7ada0ebf8b5791d1871eee3569cec8fcf9`. Isso não significa validar os três ramos de derrota no mesmo build. Nenhum código ou asset do jogo foi alterado; nenhuma ROM ou save é publicada.

Limites: as estratégias são sequências gravadas dependentes do build/balanceamento e não medem taxa de captura ou consumo de cápsulas contra treinadores. Os testes verificam o resultado de derrota e a recuperação/persistência, não todos os ramos de batalha. Próximo passo concreto: adaptar ao português os textos herdados da sequência de derrota/recuperação. Equipe cheia/envio de captura ao PC e acabamento visual amazônico continuam pendentes.

## Missão atual com Capivágua

`check_mission.py --partners capivagua` passou desde um jogo novo, sem fixtures, escrita de memória ou savestates: controle bloqueado antes da vitória, agente vencido com o segundo ataque (Water Gun), controle liberado, ponte atravessada, Pedra das Águas recebida e retorno ao guia na vila. O save normal pelo menu foi encerrado e reaberto em outro processo. Continue preservou parceiro/equipe de um animal, índice 1, flags `0F`, item 361 e posição (8,9). Relatório: `docs/capivagua-mission-validation.json`.

O teste ganhou seleção opcional por `--partners`, permitindo validar somente o ramo pendente. O padrão Ararafogo/Tatupedra foi preservado para os consumidores de fixtures existentes. Esses ramos não foram repetidos nesta execução: suas evidências em `docs/mission-current-validation.json` têm o mesmo hash de ROM, completando agora a cobertura dos três parceiros no build atual.

Validações: `make -j4 firered_rev1` incremental PASS, SHA-1 inalterado `2cd252b4dbb1926e28e89944333d5c7b033fa304`, símbolos regenerados do ELF; teste completo PASS em `tests/emulator/results/capivagua-mission-20261112/`; `py_compile`, `--help` e `git diff --check` PASS. Nenhum código ou asset do jogo foi alterado. Somente teste, documentação e relatório JSON são publicados; nenhuma ROM ou save.

Limites: esse ramo confere o ID da pedra e as flags, não a quantidade nem todos os caminhos de save. Os testes separados de inventário/revisita continuam com seus escopos registrados. Próximo passo concreto: validar derrota/recuperação com Capivágua e Tatupedra. Equipe cheia/envio de captura ao PC e acabamento amazônico também continuam pendentes.

## Coleta com bolsa cheia e save dentro do bosque

`tests/emulator/check_stone_collection_full.py` passou em uma fixture artificial de Ararafogo anterior à coleta: uma cópia do save pós-missão recebeu 30 itens especiais distintos sem a pedra e teve somente a flag WATER_STONE limpa, preservando parceiro, suprimentos, vitória e controle liberado. Ao entrar no bosque, o objeto da pedra reapareceu. Três tentativas normais de coleta mantiveram os itens, o objeto ativo e flags `07`. Depois de liberar artificialmente um slot, a coleta normal concedeu uma pedra, removeu o objeto e marcou flags `0F`, preservando os outros 29 itens. Repetir a interação não duplicou a pedra.

O teste salvou pelo menu diretamente no bosque, fechou o processo e abriu Continue sem habilitar escritas: bolsa e progresso persistiram, o objeto permaneceu ausente e a ponte foi atravessada rumo ao sul. O campo simples `progress keyitem` mostra 259, pois esse é o primeiro slot da fixture; as asserções percorrem todos os 30 slots e conferem a pedra 361 com quantidade 1 no último slot. O save de origem foi preservado.

Validação: `make -j4 firered_rev1` incremental PASS e símbolos regenerados; SHA-1 inalterado `2cd252b4dbb1926e28e89944333d5c7b033fa304`; teste completo PASS em `tests/emulator/results/stone-collection-full-20261111/`; `py_compile` e `git diff --check` PASS. Relatório: `docs/stone-collection-full-validation.json`; instruções em `tests/emulator/README.md`. Não houve mudança no jogo. Somente teste, documentação e relatório são publicados, sem ROM ou saves.

Limite: a bolsa cheia e a flag anterior à coleta foram preparadas por escrita de memória opt-in, não alcançadas em gameplay natural. Nenhum resultado da coleta foi forçado após preparar a fixture. O ciclo de save no bosque cobre essa condição específica, não todos os caminhos de carregamento. Próximo passo concreto: missão completa com Capivágua no build atual. Equipe cheia/envio ao PC, derrota dos demais parceiros e acabamento amazônico seguem pendentes.

## Reposição da pedra — fixtures artificiais de inventário

`tests/emulator/check_stone_repair.py` passou em dois cenários preparados artificialmente a partir de uma cópia do save de Ararafogo pós-missão: flag da pedra já obtida com bolsa especial vazia; e a mesma flag com os 30 slots ocupados por itens especiais distintos, sem a pedra. No primeiro, o cuidador repôs uma unidade. No segundo, recusou sem modificar a bolsa; após liberar exatamente um slot na fixture, repôs uma unidade sem perder os outros 29 itens. Repetir a interação não duplicou a pedra. Save normal e Continue em outro processo preservaram bolsa completa e progresso nos dois casos; o save original foi preservado.

Esses resultados **não são gameplay natural**: os cenários usam escrita de memória para preparar somente o bolso de itens especiais. O runner ganhou `write32` opt-in por `--test-writes enabled`, limitado a EWRAM alinhada, com resposta e logs explícitos de teste. Os guards sem opt-in, para endereço de ROM e para endereço desalinhado passaram. A preparação usa quantidades cifradas pela chave real do save; ações do cuidador e salvamento usam os controles normais. Os processos de Continue são abertos com escritas desabilitadas. Nenhuma flag, resultado do script ou concessão de item foi forçada após preparar os bolsos.

Validações: `make -j4 firered_rev1` incremental PASS, SHA-1 inalterado `2cd252b4dbb1926e28e89944333d5c7b033fa304`, símbolos regenerados; runner recompilado com `-Wall -Wextra -Werror`; teste completo PASS em `tests/emulator/results/stone-repair-20261111-v2/`; `py_compile` e `git diff --check` PASS. Relatório: `docs/stone-repair-validation.json`. Instruções em `tests/emulator/README.md`. A primeira tentativa do teste não confirmou a sobrescrita do save existente e Continue retornou à posição antiga; foi corrigida a sequência de entradas, sem alteração no jogo. Nenhuma ROM ou save é publicada.

Próximo passo concreto: testar a aquisição no objeto da pedra com a bolsa cheia, ainda não coberta. Também seguem pendentes missão atual de Capivágua, equipe cheia/envio de captura ao PC, derrota dos outros parceiros e save/Continue diretamente no bosque. A validação atual cobre o cuidador em estados artificiais, não a possibilidade de alcançar naturalmente uma bolsa cheia ou perder a pedra.

## Captura natural e persistência

`tests/emulator/check_capture.py` passou desde um jogo novo: Capivágua recebeu as cinco cápsulas do guia, caminhou até a grama da Route1 e encontrou Tatupedra de nível 3. Usando Tackle, reduziu o HP selvagem a 4 sem derrotá-lo; uma cápsula capturou o animal (`B_OUTCOME_CAUGHT = 7`). A equipe passou de um para dois animais e a bolsa de cinco para quatro cápsulas. O teste salvou pelo menu SALVAR, fechou o processo e abriu Continue em outro, confirmando equipe, nome/nível da captura, cápsulas, flags `01`, ausência de pedra e posição (15,14) na Route1.

Validação: build incremental `make -j4 firered_rev1` PASS, SHA-1 preservado `2cd252b4dbb1926e28e89944333d5c7b033fa304`, símbolos regenerados do ELF; teste completo PASS em `tests/emulator/results/capture-20261111/`; `py_compile` e `git diff --check` PASS. Relatório em `docs/capture-validation.json`, instruções em `tests/emulator/README.md`. Nenhum código ou asset do jogo foi alterado. Somente teste, documentação e relatório JSON são publicados; ROM, saves, logs e capturas permanecem ignorados pelo Git.

O cenário usa somente entradas normais e leituras, sem injetar criaturas, itens, HP, resultado ou RNG e sem savestates no teste final. A sequência e suas pausas foram gravadas para este build; valida um encontro, não a taxa de captura. Tentativas exploratórias de lançamento podem falhar normalmente e não são tratadas como sucesso. Não foram validados outros animais selvagens, equipe cheia/envio ao PC ou todos os ramos de falha. A identidade persistida é conferida por nome/nível não cifrados, após verificar a espécie selvagem e o resultado da batalha.

Próximo passo concreto: mochila cheia ou reposição da pedra ausente. Também seguem pendentes missão atual de Capivágua, derrota dos outros parceiros e save/Continue diretamente no bosque. Os relatos abaixo são histórico dos respectivos testes/builds.

## Correção — ponte persistente e revisitas à pedra

O teste novo `check_stone_revisit.py` reproduziu um defeito no build `8c41ff7ada0ebf8b5791d1871eee3569cec8fcf9`: após Continue na vila e retorno ao bosque, flags `0F` e item 361 persistiam, mas o jogador parava em (11,11), diante da ponte fechada. A restauração dos tiles estava em `MAP_SCRIPT_ON_TRANSITION`, que roda antes de `InitMap` reinicializar o grid. Foi movida para `MAP_SCRIPT_ON_LOAD`, após a inicialização dos tiles, mantendo a condição da flag e o bloqueio antes da vitória.

Build corrigido: SHA-1 `2cd252b4dbb1926e28e89944333d5c7b033fa304`. Os objetos `data/maps.o` e `data/map_events.o` foram regenerados explicitamente e `make -j4 firered_rev1` passou; símbolos atualizados pelo ELF. A missão completa e save/Continue foram repetidos com Ararafogo e Tatupedra no novo build, ambos PASS (`docs/mission-current-validation.json`). `check_stone_revisit.py` também passou nos dois ramos: usa cópias desses saves nativos, confirma a travessia da ponte ao reentrar no bosque e examina todos os 30 slots de itens especiais, decifrando a quantidade com a chave de SaveBlock2. A pedra permaneceu em um único slot, com quantidade 1, antes e depois de três tentativas de interação no antigo local e três interações com o cuidador. As flags continuaram `0F`, a equipe permaneceu com um parceiro e os arquivos de save originais não foram alterados.

Relatório: `docs/stone-revisit-validation.json`. Instruções reproduzíveis em `tests/emulator/README.md`; a entrada `--mission-results` deve apontar para os resultados de `check_mission.py` do mesmo hash de ROM. `py_compile` e `git diff --check` passaram. Resultados locais: `tests/emulator/results/mission-bridge-fix-20261110/` e `stone-revisit-fixed-20261110/`, ignorados pelo Git. Somente fontes, testes, documentação e relatórios JSON são publicados; nenhuma ROM ou save.

Próximo passo concreto: captura ou mochila cheia. Permanecem sem validação: reposição da pedra quando ausente, aquisição com bolsa cheia, missão atual de Capivágua, derrota dos demais parceiros e save/Continue feito diretamente dentro do bosque. A revisita atual comprova entrada no bosque após Continue salvo na vila; não é uma validação de todos os caminhos de carregamento. Os relatos abaixo são histórico dos respectivos builds.

## Missão vitoriosa — Ararafogo e Tatupedra

`tests/emulator/check_mission.py` passou com os dois parceiros, desde jogos novos, usando somente entradas normais e leituras de memória. O controle recusou ativação antes da vitória; cada parceiro venceu o agente com o segundo ataque (`MOVE_EMBER`/`MOVE_MUD_SLAP`), liberou o controle, atravessou a ponte, recebeu a Pedra das Águas e voltou ao guia na vila. O save normal pelo menu SALVAR foi fechado e reaberto em outro processo para cada parceiro. Continue preservou parceiro, índice escolhido, equipe, flags `0F`, item 361 e posição (8,9) na vila. Relatório: `docs/mission-current-validation.json`.

Validações desta execução: `make -j4 firered_rev1` incremental PASS e símbolos regenerados do ELF; ROM SHA-1 `8c41ff7ada0ebf8b5791d1871eee3569cec8fcf9`, sem alteração do jogo; `py_compile` do novo teste e `git diff --check` PASS. O cenário tem limite de 300 ciclos de entrada na batalha e exige `B_OUTCOME_WON = 1`; uma derrota falha o teste. A escolha do ataque usa o handler único `HandleInputChooseMove` e o cursor resolvidos pelo ELF, evitando nomes de funções estáticas duplicados. Instruções em `tests/emulator/README.md`; resultados completos em `tests/emulator/results/mission-20261110/`, ignorados pelo Git. Estados do emulador foram usados somente na exploração local; os dois casos finais passaram integralmente sem savestates, injeção de atributos, HP ou flags. Nenhuma ROM ou save é publicado.

Próximo passo concreto: validar captura e casos de inventário (mochila cheia e quantidade/duplicação da pedra). Esses casos não foram cobertos pelo teste atual: `keyitem` confere o ID do primeiro slot de itens especiais, não sua quantidade. A missão completa e o save após a pedra com Capivágua ainda têm evidência apenas do build anterior; repetir esse ramo no build atual é outra pendência. Derrota com os demais parceiros, reconstrução da ponte após Continue, arte amazônica e expansão dos habitats seguem pendentes.

## Retomada — save normal após derrota

O teste de derrota/recuperação que estava pronto localmente foi preservado e ampliado antes da publicação. `tests/emulator/check_defeat_recovery.py` agora salva pelo menu SALVAR depois da recuperação com Ararafogo, encerra o processo e usa Continue em outro processo. A execução final passou desde um jogo novo, sem savestates ou escrita de memória: derrota `B_OUTCOME_LOST = 2`, casa em (8,5), HP cheio, parceiro e equipe preservados, flags `01` e nenhum item da pedra. Continue preservou esses dados e o HP; caminhar novamente até o controle confirmou o bloqueio e a liberação de movimento após fechar o diálogo.

Validação desta retomada: `make -j4 firered_rev1` incremental PASS, SHA-1 `8c41ff7ada0ebf8b5791d1871eee3569cec8fcf9`; runner recompilado com `-Wall -Wextra -Werror` e símbolos regenerados do ELF; teste completo PASS em `tests/emulator/results/defeat-save-20261110/`; `py_compile` e `git diff --check` PASS. Relatório atualizado em `docs/defeat-recovery-validation.json` e instruções em `tests/emulator/README.md`. Nenhum código ou asset do jogo foi alterado. Saves, ROM, logs e capturas continuam ignorados; somente teste, documentação e relatório JSON são publicados.

Próximo passo concreto: missão vitoriosa com Ararafogo e Tatupedra, incluindo save/Continue após a pedra. O percurso `reach_control` já está documentado no teste de derrota; o uso repetido do primeiro ataque é proposital para perder e não certifica uma estratégia de vitória. Captura, inventário cheio, duplicação da pedra, derrota com os outros parceiros e textos herdados em inglês continuam pendentes. Os relatos de execuções anteriores abaixo são histórico; a limitação antiga de não testar save após derrota foi resolvida apenas para Ararafogo.

## Segunda execução diária — 9 de novembro de 2026

Avanço na pendência 1: novo teste `tests/emulator/check_defeat_recovery.py`, executado desde um jogo novo com Ararafogo. O percurso exploratório perdeu usando o primeiro ataque; esse cenário virou uma regressão de derrota/recuperação, sem alterar atributos, HP ou flags por injeção. A missão vitoriosa com os demais parceiros não foi concluída nesta execução.

Resultado final PASS (`docs/defeat-recovery-validation.json`): o rio e o controle estavam bloqueados antes da batalha; a derrota teve `B_OUTCOME_LOST = 2`; o jogador retornou à casa em (8,5), com HP completo, parceiro/equipe preservados, flags `01` e nenhum item da pedra. Após concluir as telas e o diálogo automático de recuperação, foi possível sair da casa, caminhar de volta ao rio, confirmar que a barreira/controle continuavam bloqueados e mover-se depois de fechar o diálogo. Isso cobre somente derrota com Ararafogo, sem save/Continue após a derrota.

Compilação incremental `make -j4 firered_rev1` PASS; SHA-1 da ROM permaneceu `8c41ff7ada0ebf8b5791d1871eee3569cec8fcf9`. Runner recompilado com `-Wall -Wextra -Werror`, símbolos regenerados do ELF atual; `py_compile` do teste e `git diff --check` passaram. Não houve mudança no código ou na arte do jogo. Logs e capturas ficaram em `tests/emulator/results/defeat-recovery-20261109-v6/`, ignorados pelo Git; somente o relatório JSON é versionado.

As tentativas iniciais ajustaram o teste, não o jogo: o mapa da casa já aparece na memória durante a tela preta de retorno; é necessário esperar também o fim da tarefa de retorno, do script e do bloqueio de controles. O teste verifica esses estados por símbolos do ELF, com limite de espera, em vez de contar páginas. O respawn (8,5) difere do início de jogo; a saída ativa é o tile de seta sul em (4,8), enquanto (5,8) é piso comum. A execução final, em pasta nova, percorreu tudo com entradas normais. A recuperação ainda exibe textos herdados em inglês, pendentes de adaptação de linguagem.

Próximo passo: missão vitoriosa com Ararafogo e Tatupedra no build atual, incluindo save/Continue após a pedra. `reach_control` e `position` no teste novo documentam um percurso sem grama até o agente/controle e podem apoiar esse teste; a estratégia de primeiro ataque do cenário de derrota não deve ser confundida com uma estratégia de vitória. Captura, inventário cheio, duplicação da pedra e recuperação com os outros parceiros continuam pendentes.

## Execução diária — 9 de novembro de 2026

Avanço pequeno na pendência 2: `tests/emulator/check_partner_saves.py` agora valida save normal na vila depois de receber parceiro e suprimentos, nos três ramos (Capivágua, Ararafogo e Tatupedra). Cada caso começa sem save existente, salva pelo menu SALVAR, encerra o emulador e carrega Continue em outro processo. Parceiro escolhido, índice, tamanho da equipe, flags e localização persistiram; repetir a interação com o guia após Continue não concedeu outro parceiro. Relatório: `docs/partner-save-validation.json`. Instruções reproduzíveis em `tests/emulator/README.md`.

Validações executadas nesta sessão Linux:

- Compilador agbcc construído e instalado localmente; `make -j4 firered_rev1` passou a partir da cópia sem artefatos de build. ROM SHA-1 `8c41ff7ada0ebf8b5791d1871eee3569cec8fcf9`, igual ao registro anterior. Nenhum código ou asset do jogo foi alterado.
- `check_starters.py`: três parceiros PASS (escolha/cancelamento, concessão única e suprimentos).
- `check_partner_saves.py`: três parceiros PASS, seis processos, save nativo/Continue e nova interação com o guia. Os arquivos nativos tinham 131088 bytes: 128 KiB de flash mais o rodapé RTC de 16 bytes do mGBA. O teste aceita os formatos com/sem esse rodapé.
- `python3 -m py_compile tests/emulator/check_partner_saves.py` e `git diff --check` passaram.

Durante o desenvolvimento do teste, a primeira asserção de tamanho ignorava o rodapé RTC; outra tentativa revelou que o diálogo do guia ainda estava aberto quando se pressionava Start no ramo Ararafogo. O teste agora fecha esse diálogo com B antes de abrir o menu. A execução final usou uma pasta nova e passou integralmente. Isso não era falha de persistência do jogo.

Ambiente desta execução: Debian 13, sem sudo e sem instalador de pacotes privilegiado. Binutils ARM, headers/libpng e mGBA foram extraídos de pacotes oficiais Debian para `/workspace/work/deps/root`, fora do Git; foram usados PATH, CPATH, LIBRARY_PATH e PKG_CONFIG_SYSROOT_DIR/PKG_CONFIG_LIBDIR apontando para essa árvore. O runner foi ligado ao mGBA 0.10.5 com rpath local. Essa preparação não valida o script Windows/WSL nem instala dependências em futuras máquinas. ROM, saves, logs e screenshots de teste permanecem ignorados pelo Git.

Próximo passo concreto: executar a missão completa no build atual com Ararafogo e Tatupedra (agente, controle, pedra e retorno), incluindo save/Continue depois da pedra. Derrota/recuperação, captura, inventário cheio, duplicação da pedra e acabamento visual continuam pendentes; os testes novos cobrem somente a vila após escolher o parceiro.

## Intro amazônica — atualização atual

A abertura agora usa uma capa própria em 240×160, com rio, palafita, capivara e arara, e o título Bichos do Brasil: As Cinco Pedras. A sequência original Game Freak/Nidorino é pulada depois da tela legal. Bia tem retrato próprio e apresenta Capivágua, os cinco habitats, as pedras e as Terras Raras. Tio Sam tem retrato próprio, identidade fixa e explicação da ameaça; não há mais pedido para escolher o nome do rival. Aparência e nome do jogador continuam selecionáveis. Os retratos e sprites do jogador ainda são provisórios da base, assim como parte da interface e a música.

Build Linux/mGBA atual: SHA-1 `8c41ff7ada0ebf8b5791d1871eee3569cec8fcf9`. Passaram as duas aparências, nome personalizado, recusa/correção do nome, nomes padrão em branco, entrada no térreo da casa e salvamento pelo menu seguido de Continue em outro processo. Os três parceiros passaram novamente escolha, cancelamento, concessão única e suprimentos. Consulte `docs/intro-validation.json`, `docs/intro-starter-regression-results.json` e `docs/screenshots/intro/`. O teste atual de save é na casa, antes do parceiro; a missão completa registrada abaixo pertence ao build anterior e não foi repetida neste build.

As fontes de arte estão em `assets/amazon/intro/`. Para reconverter, instale Pillow 12.1 ou posterior e execute `python3 tools/build_intro_assets.py`; depois compile normalmente. Os arquivos convertidos já estão versionados, então Pillow não é exigido para simplesmente compilar. O novo fluxo automatizado está em `tests/emulator/intro_flow.py` e é compartilhado pelos testes da intro e dos parceiros.

## Objetivo e decisões aprovadas

ROM hack de FireRed Rev1 com identidade brasileira. Cinco habitats, uma pedra rara em cada, abrindo o caminho para Terras Raras com animais pré-históricos e seres fantásticos. Tio Sam é um magnata fictício que quer explorar os habitats e controlar essas criaturas. Começar um jogo novo é obrigatório. O jogador escolhe Capivágua (água), Ararafogo (fogo) ou Tatupedra (terra). Os animais substituem espécies originais; não são adicionados ao elenco Pokémon. Pedras são itens especiais na mochila.

## Pastas e restauração

Base: https://github.com/pret/pokefirered commit ce6406d8c2eaf46d543c8a2606de0c3cb1951982. Aplique source.patch conforme README.md. Ele inclui mudanças binárias e os dois arquivos novos do ícone da pedra. O projeto auxiliar, artes e documentos estão em project/. A pasta pokefirered só será criada ao clonar a base. Não há ROM comercial neste pacote. SHA-1 da ROM base fornecida pelo usuário: dd5945db9b930750cb39d00c84da8571feebf417.

## Implementado e compilado

- Casa brasileira original, começo no térreo e checkpoint de recuperação.
- Vila, Route1 e ViridianForest conectados; terreno e parte da aparência ainda provisórios.
- Guia com escolha, prévia, confirmação e entrega única do parceiro; cinco cápsulas uma única vez.
- Três criaturas com desenhos próprios frente/costas/ícones, nomes, tipos, atributos e ataques. Evoluções originais desativadas.
- Agente no bosque com duas criaturas de nível 4; controle só funciona após a vitória.
- Barreira no rio, passagem liberada pelo controle, Pedra das Águas obtida uma vez como item 361 reaproveitado (nome da bolsa P. das Águas).
- Cura gratuita e reparo de inconsistência da pedra pelo cuidador da vila.
- Diálogo de retorno reconhece a primeira pedra e informa que faltam quatro.

## Verificado no emulador

Os três menus/prévias e as escolhas de parceiros foram conferidos em versões anteriores da mesma série. Na versão atual, um jogo novo com Capivágua venceu o agente; o controle recusou ativação antes da batalha, abriu a passagem após a vitória, a pedra entrou na mochila e o jogador voltou à vila com reconhecimento no diálogo. O jogo foi salvo pelo menu, o processo encerrado, e um processo novo reconheceu Continue e carregou o save. Depois de sair da retrospectiva do jogo, a leitura da memória confirmou flags 0x0F (suprimentos, agente, controle e pedra), item 361 na mochila e uma criatura na equipe. Consulte mission-validation.json para as leituras de progresso e os limites.

## Pendências reais

1. Ampliar os cenários de captura (outras espécies/equipe cheia). A coleta pelo objeto com bolsa cheia passou em fixture artificial: recusa preservou objeto/flags; liberar um slot permitiu coletar sem perda dos outros itens. Reposição pelo cuidador, recusa com bolso cheio e retomada após liberar um slot passaram em fixtures artificiais, não em gameplay natural. Uma captura natural de Tatupedra com Capivágua e consumo de cápsula passou, incluindo save/Continue. Quantidade unitária e ausência de duplicação após revisitar o local/curador foram conferidas com Ararafogo e Tatupedra. Missão vitoriosa e save/Continue validados com os três parceiros no build 2cd252b4dbb1926e28e89944333d5c7b033fa304. Derrota/recuperação, save/Continue e manutenção do bloqueio após perder foram revalidados para os três parceiros no build dos textos em português b89c8c560eae9d999b68fd22b6ace17409b2f913.
2. Ampliar outros caminhos de save/carregamento: o ciclo pós-missão na vila já passou com os três parceiros no build 2cd252b4dbb1926e28e89944333d5c7b033fa304. Save/Continue diretamente no bosque passou na fixture artificial de coleta com bolso cheio e posterior liberação de um slot. A reconstrução da ponte ao entrar novamente no bosque após Continue foi corrigida e validada com Ararafogo e Tatupedra. Os ciclos após a pedra com Ararafogo e Tatupedra passaram, além dos ciclos na casa, após derrota com Ararafogo e na vila após escolher cada um dos três parceiros. Usar SALVAR e persistência nativa via VFile; não usar o antigo flushsave removido.
3. Adaptar caminhos absolutos /workspace dos auxiliares para o disco G/WSL; documentar um build limpo reprodutível.
4. Completar a identidade amazônica: árvores, água, palafitas/doca, personagem, NPCs, interiores e cenário de batalha. Ainda há bastante arte/interface/áudio do FireRed.
5. A grade de água usa um tile provisório; criar arte de rio/ponte/controle/objeto da pedra. O ícone da mochila da pedra já é próprio.
6. Conferir descrições, compatibilidade de TM/tutores e ícones das três criaturas no jogo. A paleta alternativa repete a normal por enquanto.
7. Aplicar o patch IPS final com Floating IPS independentemente e comparar o hash. A ferramenta CLI foi compilada na nuvem, mas essa conferência final da missão ainda não foi executada.
8. Somente depois expandir aos outros habitats e às Terras Raras.

## Fontes de planejamento

project/docs/egm/amazon-expedition.md e amazon-implementation-contract.md. São documentos de referência, não prova de implementação completa. Leia também os relatórios EGM; alguns pontos antigos foram corrigidos posteriormente. Não reiniciar o questionário de decisões já aprovadas.

## Ambiente local

Usar G:\duolingo\BichosDoBrasil. No WSL, normalmente /mnt/g/duolingo/BichosDoBrasil. Seguir INSTALL.md do pret/pokefirered para instalar binutils ARM, agbcc e libpng. Agbcc usado na nuvem: da598c1d918402c42c0c0d7128ba14567f3175e9. Build alvo make -j4 firered_rev1. Regenerar explicitamente os objetos data/maps.o e data/map_events.o quando mudar os binários de mapa, pois já houve reaproveitamento de mapas antigos pela compilação. A toolchain Linux da nuvem não está incluída neste ZIP.

## Última validação de retomada

restart-check.txt registra a execução em processo novo e as leituras de progresso depois da retrospectiva. A opção Continue e a preservação da pedra/objetivo foram confirmadas. A função experimental progress do runner usa endereços de símbolos da compilação atual e deve ser resolvida pelo ELF novamente após outro build. Nenhum save ou ROM comercial foi incluído no pacote.

## Retomada e teste de regressão dos parceiros

O código do GitHub foi recompilado em um ambiente Linux novo. A ROM reproduziu exatamente o SHA-1 registrado (b9f6a5f93f524a6d36543d1020fdf3125b08b29e). O runner agora lê os símbolos do build atual, segue o ponteiro de save após transições e fecha o core mesmo em caminhos de erro. O fluxo normal não usa mais o clone/truncamento experimental de flushsave.

Foram executados três jogos novos automatizados, um por parceiro: escolha/cancelamento, concessão única, índice correto de parceiro, entrega de suprimentos e repetição da interação passaram. Veja docs/starter-regression-results.json e tests/emulator/README.md. Isso não é a execução integral da missão com cada parceiro nem uma nova validação de save normal; essas pendências continuam.
