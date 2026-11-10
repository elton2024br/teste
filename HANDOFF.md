# Instrução atual para esta versão GitHub

O projeto está completo em termos de arquivos-fonte neste repositório. Use pokefirered/ e agbcc/ diretamente. Não clone uma segunda base e não aplique source.patch. As menções a ZIP, source.patch e project/ abaixo são históricas. Nesta estrutura project/docs = docs, project/tools = tools, project/assets = assets e project/tests = tests.

# ATENCAO: PACOTE DE CODIGO COMPLETO

A restauracao ja foi feita na nuvem. O conteudo abaixo conserva o historico e as pendencias, mas suas instrucoes de clonar e aplicar source.patch estao SUPERADAS: use diretamente a pasta pokefirered/ deste pacote e LEIA-PRIMEIRO.md. Nao repita a aplicacao do patch.

# Bichos do Brasil — ponto de retomada

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

1. Testar captura, quantidade/duplicação da pedra e falta de espaço. Missão vitoriosa validada no build atual com Ararafogo e Tatupedra; falta repetir Capivágua neste build. Derrota/recuperação e manutenção do bloqueio após perder estão validadas com Ararafogo; faltam os demais parceiros.
2. Ampliar os testes de save normal após a missão com Capivágua no build atual e conferir a reconstrução da ponte após Continue. Os ciclos após a pedra com Ararafogo e Tatupedra passaram, além dos ciclos na casa, após derrota com Ararafogo e na vila após escolher cada um dos três parceiros. Usar SALVAR e persistência nativa via VFile; não usar o antigo flushsave removido.
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
