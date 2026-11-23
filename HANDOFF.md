# Instrução atual para esta versão GitHub

O projeto está completo em termos de arquivos-fonte neste repositório. Use pokefirered/ e agbcc/ diretamente. Não clone uma segunda base e não aplique source.patch. As menções a ZIP, source.patch e project/ abaixo são históricas. Nesta estrutura project/docs = docs, project/tools = tools, project/assets = assets e project/tests = tests.

# ATENCAO: PACOTE DE CODIGO COMPLETO

A restauracao ja foi feita na nuvem. O conteudo abaixo conserva o historico e as pendencias, mas suas instrucoes de clonar e aplicar source.patch estao SUPERADAS: use diretamente a pasta pokefirered/ deste pacote e LEIA-PRIMEIRO.md. Nao repita a aplicacao do patch.

# Bichos do Brasil — ponto de retomada

## Plano funcional de 20 dias — rotina 1

Meta de planejamento até 5 de dezembro de 2026: uma campanha mínima jogável de ponta a ponta. O prazo é alvo, não garantia. Prioridade: progressão, habitats, missões, batalhas, cinco pedras e desfecho; polimento visual e traduções secundárias ficam depois.

- Dias 1–3: concluir e estabilizar o segundo habitat/Campo Cerrado e a Pedra das Raízes.
- Dias 4–7: terceiro habitat, missão, batalha e terceira pedra.
- Dias 8–11: quarto habitat, missão, batalha e quarta pedra.
- Dias 12–15: quinto habitat, missão, batalha e quinta pedra.
- Dias 16–17: acesso às Terras Raras, confronto e desfecho mínimo.
- Dias 18–20: percurso integral com os três parceiros, balanceamento essencial, save/Continue e correções bloqueadoras.

Progresso ao fim da rotina 16: os cinco habitats, as cinco pedras, o acesso às Terras Raras, o confronto com Tio Sam e um desfecho com santuário persistente formam uma campanha funcional com os três parceiros. A cadeia integral permanece validada desde jogo novo e por save/Continue após cada etapa. Derrota, recuperação, persistência, retorno e nova tentativa passaram nos cinco agentes posteriores à primeira missão e no chefe, nos três ramos. Equipes sintéticas de dois membros concluíram a campanha nos três ramos; HP, veneno e PP dos dois membros foram restaurados depois de cada recompensa. Uma equipe obtida naturalmente — Capivágua e Tatupedra capturado — também concluiu a campanha, incluindo cura, troca obrigatória, cinco pedras e preservação de identidade. Cerrado, Caatinga, Mata Atlântica, Pantanal e chefe têm fauna brasileira própria; o ponto imediato da missão do Pantanal tem uma ilha verde cercada por água. Restam substituir o restante dos mapas/arte provisórios, ampliar as combinações naturais e dar acabamento visual ao encerramento. A meta de 5 de dezembro continua plausível, mas não é garantia de jogo completo.

## Captura natural encadeada à campanha — rotina 16

`check_capture.py` agora registra a identidade estável dos membros da equipe. O novo `check_captured_first_mission.py` copia o save nativo da captura, volta pela Route 1, usa a cura gratuita do cuidador, segue ao bosque e completa agente, controle e Pedra das Águas. A saída é compatível com os testes posteriores. Do Cerrado às Terras Raras, cada recompensa e cada processo novo de Continue compara personalidade, ID do treinador, espécie e nome dos dois animais antes de avançar.

Capivágua capturou naturalmente Tatupedra nível 3 com uma das cinco cápsulas, sem escrita de memória ou savestate. A dupla voltou à vila, teve HP/status/PP restaurados pelo cuidador e venceu o primeiro agente em 107 ciclos, com uma troca obrigatória real depois que o líder desmaiou. Depois venceu Cerrado, Caatinga, Mata Atlântica, Pantanal e Tio Sam em 42, 38, 41, 45 e 45 ciclos, recebeu as cinco pedras e visitou o santuário antes e depois de Continue. Foram sete checkpoints de save/Continue; as duas identidades e quatro cápsulas permaneceram corretas. ROM inalterada, SHA-1 `d0955a510c864327d5c57ccc07eb9fdf2da4cd98`. Relatório: `docs/natural-two-member-campaign-validation.json`.

Também passaram uma campanha padrão de um membro e a regressão de captura com equipe cheia/envio ao PC. Tentativas intermediárias não foram aceitas: o leitor inicialmente recusou o glifo `Á`; o handler de troca possuía três símbolos estáticos homônimos e precisou ser tratado como conjunto; sem visitar o cuidador, o desgaste real da captura levou os dois membros à derrota; e o save existente exigia confirmação adicional de sobrescrita. O fluxo final usa o cuidador e a confirmação normais, sem forçar resultado. Limites: uma única dupla e encontro determinístico, sem estatística de captura ou balanceamento final. Próximo passo funcional: validar derrota, recuperação e revanche do chefe com essa equipe natural de dois membros, preservando ambas as identidades e as cinco pedras.

## Representação visual do Santuário das Cinco Pedras — rotina 14

O encerramento agora troca o marco superior de Cheias por um objeto original de 16×16: cinco gemas, um núcleo verde e um pedestal. O gráfico próprio tem ID 153, reutiliza sem alterar a paleta nativa `npc_green.pal` e é produzido de modo determinístico por `tools/build_rare_sanctuary_asset.py`; fonte e instruções ficam em `assets/amazon/rare-sanctuary/`. Antes do desfecho aparece a rocha de Cheias em `(5,6)`; ao concluir a campanha ela é removida e o santuário aparece na mesma posição. O ponto central interativo `(5,8)` continua sendo piso passável e persiste após save/Continue.

Build Linux PASS, SHA-1 `d0955a510c864327d5c57ccc07eb9fdf2da4cd98`. Foram regeneradas três campanhas completas desde jogos novos: 18 batalhas, cinco pedras, desfecho, seis visitas ao santuário e save/Continue após cada etapa passaram. Também passaram as três derrotas finais com HP=1 preparado, recuperação em casa, preservação das pedras, Continue, retorno por todos os habitats e revanche. Captura revisada em `docs/screenshots/rare-sanctuary-visual/preview.png`; relatório em `docs/rare-sanctuary-visual-validation.json`.

Uma primeira versão em `(5,8)` foi rejeitada nos testes: o objeto bloqueava a única saída central e prendia o jogador depois da interação. A versão publicada usa `(5,6)` e passou pelo eixo integral. Limites: quatro rochas, mapa, prédio, música e créditos continuam herdados ou provisórios; não é um encerramento final polido. Próximo passo funcional: validar uma equipe com mais de um membro durante a campanha e comprovar recuperação de status e PP entre habitats, antes de novo polimento visual.

## Equipe de dois membros e recuperação completa — rotina 15

Os testes do Cerrado, Caatinga, Mata Atlântica e Pantanal agora aceitam `--recovery-fixture`. Na primeira etapa, a fixture opt-in clona byte a byte o parceiro válido no segundo slot. Antes de cada percurso de habitat, reduz o HP dos dois membros em um ponto, aplica veneno ao segundo e reduz PP dentro do sub-bloco cifrado, recalculando seu checksum. Não escreve flags, pedras, recompensas, adversários nem resultados. Batalhas, scripts de recompensa, save e Continue continuam por entradas normais; o processo novo de Continue roda sem permissão de escrita.

Capivágua, Ararafogo e Tatupedra passaram pelos quatro habitats com dois membros: 12 recompensas restauraram HP, status e todos os PP dos dois slots, totalizando 24 recuperações de membros, e os 12 estados persistiram após Continue. As três equipes seguiram sem novas escritas até Tio Sam e o santuário, preservando as cinco pedras; uma cadeia padrão de Capivágua sem fixture também passou como regressão. A ROM não mudou e conserva SHA-1 `d0955a510c864327d5c57ccc07eb9fdf2da4cd98`. Relatório em `docs/team-recovery-validation.json`; instruções em `tests/emulator/README.md`.

Duas primeiras tentativas foram rejeitadas por erros do verificador: ele assumiu passo de 9 bytes para `gBattleMoves`, mas o `agbcc` alinha a estrutura em 12; depois, interpretou ao contrário algumas permutações dos sub-blocos cifrados, detectado por Ararafogo. Ambos foram corrigidos e todos os ramos foram refeitos em pastas novas. Limites: o segundo membro é uma cópia sintética, não uma captura natural; não foram testados troca ou desmaio deliberado durante a batalha, seis membros, PP Up ou status além de veneno. Próximo passo funcional: encadear a captura natural já validada a uma campanha de dois membros, preservando espécies e identidade até o desfecho; depois cobrir troca/desmaio sem depender de clone.

## Santuário restaurado e encerramento persistente — rotina 13

O texto depois da batalha final agora explica que as cinco pedras formaram um santuário vivo, devolveram equilíbrio aos cinco habitats e reconheceram o jogador como guardião. Quando Tio Sam desaparece, o mesmo ponto `(5,8)` passa a funcionar como marco permanente do Santuário das Cinco Pedras. Isso substitui na prática o antigo diálogo `CampaignDone`, que era inalcançável porque o flag de conclusão removia o objeto de Tio Sam. Entrada `(5,9)`, batalha, cinco rochas e flags foram preservadas.

Build PASS, SHA-1 `e43bb5b13aaaa3964c3ccda86f3c44cbf580580f`. As três campanhas completas foram regeneradas desde jogos novos: 18 vitórias, cinco pedras, seis visitas ao santuário (uma antes e outra depois de Continue em cada ramo), flags finais `[255,0,224,7]` e save/Continue após todas as etapas passaram. As derrotas, recuperações, Continue e revanches contra Tio Sam também passaram nos três parceiros. Capturas revisadas em `docs/screenshots/rare-sanctuary-ending/preview.png`; relatório em `docs/rare-sanctuary-ending-validation.json`.

O compilador legado rejeitou `ã`; a redação no jogo usa `SANTUARIO` e `GUARDIAO`, sem mudar o sentido. Duas primeiras sequências de teste foram rejeitadas porque tentavam apenas virar o personagem com um toque e acabavam movendo-o; o helper final chega ao marco por baixo e é determinístico. Limites: ainda não há gráfico próprio de santuário, créditos ou cena final; mapa, rochas, prédio e música continuam herdados. Próximo passo funcional: criar uma representação visual própria para o santuário/cinco pedras sem alterar o eixo testado; depois validar equipe maior e recuperação de status/PP.

## Ilha alagada no ponto da missão do Pantanal — rotina 12

O retângulo imediato da missão na Route 4 deixou de ser somente solo seco: 12 células em `x=4..7`, `y=8..10` usam piso verde normal `0x008`, e seis células laterais em `x=3/8`, `y=8..10` usam água calma `0x12B`. Entrada `(5,9)`, Tuiuiú `(5,8)`, gatilho leste `(6,9)` e os bits preexistentes de colisão/elevação foram preservados. O conversor idempotente é `tools/build_pantanal_checkpoint.py`.

Build PASS, SHA-1 `05db3b2f46980ce51a19783edc532fcf144add8f`; mapa SHA-256 `ef79c728c29b05cad56a0a3e86a63e458d711334d7763cb7334c50930f907d0f`. As três campanhas foram regeneradas desde jogos novos: 18 vitórias, cinco pedras, desfecho e save/Continue após cada etapa passaram. As nove derrotas/revanche de Cerrado a Mata Atlântica, as três do Pantanal e as três do chefe também passaram. Captura revisada em `docs/screenshots/pantanal-checkpoint/preview.png`; detalhes em `docs/pantanal-checkpoint-validation.json`.

Uma primeira versão com `0x00D` foi rejeitada: o metatile é `MB_TALL_GRASS`, produziu encontro aleatório na revanche de Capivágua e fez o ramo voltar para casa. `0x0D1` também foi rejeitado visualmente por repetir bordas horizontais. Nenhum desses candidatos é apresentado como PASS. Limites atuais: apenas o ponto imediato ganhou identidade; penhascos, prédio, NPCs, música e o restante da Route 4 continuam herdados. Próximo passo funcional: ampliar com segurança a identidade das Terras Raras e melhorar o encerramento, preservando o eixo e repetindo a matriz de vitória/derrota.

## Tuiuiú no Pantanal e Onça-pintada de Tio Sam — rotina 11

O adversário de nível 6 do Pantanal passou a ser `TUIUIU`, no slot técnico `SPECIES_LEDYBA`, com arte original, tipo Normal/Voador, evolução desativada e Tackle no nível atual. O chefe de nível 8 passou a usar `ONCA-PINTA`, no slot `SPECIES_SPINARAK`, com arte original e tipo Sombrio. Tio Sam usa uma equipe de golpes explícitos com somente Ataque Rápido: a prioridade torna determinística a derrota da fixture com 1 HP, enquanto os atributos frágeis permitem que os três parceiros vençam com HP normal. Os conversores idempotentes são `tools/build_tuiuiu_asset.py` e `tools/build_oncapinta_asset.py`.

Build PASS, SHA-1 `df1c09b9278833fa62d3914e170e7af7b137329d`. Três campanhas foram regeneradas desde jogos novos: 18 vitórias, cinco pedras, desfecho e save/Continue após cada etapa passaram. O Tuiuiú foi vencido em 38, 42 e 39 ciclos; a Onça-pintada, em 51, 45 e 46 ciclos para Capivágua, Ararafogo e Tatupedra. As nove derrotas/revanche intermediárias, as três do Pantanal e as três do chefe passaram no mesmo hash. Capturas revisadas: `docs/screenshots/tuiuiu/preview.png` e `docs/screenshots/oncapinta/preview.png`; relatórios: `docs/tuiuiu-validation.json` e `docs/oncapinta-validation.json`.

Foram rejeitados dois equilíbrios da Onça que derrotavam Capivágua com HP cheio e uma versão de Tuiuiú que alterava a sequência aleatória e deixava Ararafogo vencer a antiga batalha final com 1 HP. Esses estados não são apresentados como PASS. Limites: aparições herdadas de Ledyba e Spinarak também exibem as novas espécies; cry, Pokédex, paletas alternativas, mapas, NPCs e músicas continuam herdados/provisórios. Próximo passo funcional: substituir primeiro o mapa/cenário provisório do Pantanal sem mover o eixo validado; depois refinar as Terras Raras e o encerramento.

## Mico-leão na Mata Atlântica — rotina 10

O adversário de nível 5 da Mata Atlântica deixou de reutilizar o Lobo-guará e passou a ser `MICO-LEAO`, com arte original de frente/costas, ícone, pegada e paleta. O slot técnico é `SPECIES_HOOTHOOT`; a espécie é Normal, não evolui e no nível 5 conhece Tackle e Growl. O nome fica sem o til porque o compilador legado rejeitou `Ã`; os dez caracteres cabem com segurança na interface. O conversor idempotente `tools/build_micoleao_asset.py` e a referência `assets/amazon/creatures/micoleao-source.png` reproduzem os assets.

Build PASS, SHA-1 `ab709422a13713f62e58ed68e48e40074cac2000`. Três campanhas foram regeneradas desde jogos novos: 18 vitórias, cinco pedras, desfecho e save/Continue depois de cada etapa passaram. O Mico-leão foi vencido por Capivágua, Ararafogo e Tatupedra em 63, 48 e 52 ciclos. As nove derrotas/revanche intermediárias, as três do Pantanal e as três do chefe também passaram no mesmo hash. Arte, nome e enquadramento foram revisados no emulador em `docs/screenshots/micoleao/preview.png`; relatório: `docs/micoleao-validation.json`.

O teste da Mata Atlântica agora captura a primeira seleção de golpe. Limites: a única equipe herdada que usava Hoothoot também passa a mostrar Mico-leão; cry, textos/categoria de Pokédex e paleta alternativa ainda são herdados/provisórios. O mapa, NPC e música da Mata Atlântica continuam herdados. O próximo marco funcional foi cumprido na rotina 11 com Tuiuiú e Onça-pintada.

## Asa-branca na Caatinga — rotina 10

O adversário de nível 4 da Caatinga deixou de reutilizar o Lobo-guará e passou a ser `ASA-BRANCA`, com arte original de frente/costas, ícone, pegada e paleta. O slot técnico é `SPECIES_PIDGEY`; a espécie é Normal/Voador, não evolui e no nível 4 conhece Tackle. O conversor idempotente `tools/build_asabranca_asset.py` e a referência `assets/amazon/creatures/asabranca-source.png` reproduzem os assets. A paleta alternativa ainda repete a normal.

Build PASS, SHA-1 `1f5de62e9b6fa3996ca197ee148dbe12583eb1c7`. Três campanhas foram regeneradas desde jogos novos: 18 vitórias, cinco pedras, desfecho e save/Continue depois de cada etapa passaram. A Asa-branca foi vencida por Capivágua, Ararafogo e Tatupedra em 39, 38 e 31 ciclos. As nove derrotas/revanche intermediárias, as três do Pantanal e as três do chefe também passaram no mesmo hash. Arte, nome e enquadramento foram revisados no emulador em `docs/screenshots/asabranca/preview.png`; relatório: `docs/asabranca-validation.json`.

O teste da Caatinga agora captura a primeira seleção de golpe, preservando uma evidência visual reproduzível. Limites: aparições herdadas de Pidgey fora da missão também mostram Asa-branca; cry, textos/categoria de Pokédex e paleta alternativa ainda são herdados/provisórios. O mapa, NPC e música da Caatinga continuam herdados. O próximo marco funcional foi cumprido na mesma rotina com o Mico-leão da Mata Atlântica.

## Lobo-guará no Campo Cerrado — rotina 9

O adversário de nível 3 do Cerrado deixou de ser Caterpie e passou a ser `LOBO-GUARÁ`, com arte original de frente/costas, ícone, pegada e paleta. O slot técnico continua `SPECIES_CATERPIE`, preservando o limite de espécies e a compatibilidade dos saves; evolução foi desativada, o tipo passou a Normal e os golpes no nível 3 são Tackle e Growl. O conversor idempotente `tools/build_loboguara_asset.py` e a referência `assets/amazon/creatures/loboguara-source.png` reproduzem os assets. A paleta alternativa ainda repete a normal.

Build PASS, SHA-1 `659e499081659d665939ba636ba66c95d2a96b1c`. Três campanhas foram regeneradas desde jogos novos: 18 vitórias, cinco pedras, desfecho e save/Continue depois de cada etapa passaram. O Lobo-guará do Cerrado foi vencido por Capivágua, Ararafogo e Tatupedra em 38, 37 e 31 ciclos. As nove derrotas/revanche intermediárias, as três do Pantanal e as três do chefe também passaram no mesmo hash. Arte e enquadramento foram revisados no emulador em `docs/screenshots/loboguara/preview.png`; relatório: `docs/loboguara-validation.json`.

Trocar o slot de Caterpie tornou a antiga equipe final forte demais. Foram rejeitadas composições que bloquearam parceiros ou eliminaram o ramo reproduzível de derrota. Tio Sam usa provisoriamente um Weedle nível 8: os três parceiros vencem com HP normal e perdem com a fixture de HP=1, recuperam e vencem a revanche. Limites: aparições herdadas de Caterpie fora do Cerrado também mostram Lobo-guará; cry, textos/categoria de Pokédex e paleta alternativa ainda são herdados/provisórios. Próximo passo funcional: criar uma espécie própria da Caatinga em outro slot controlado e repetir a mesma matriz de vitória/derrota antes de avançar aos demais habitats.

## Derrota e revanche nos agentes intermediários — rotina 8

O teste parametrizado `tests/emulator/check_intermediate_habitat_defeat.py` cobre Cerrado, Caatinga e Mata Atlântica com Capivágua, Ararafogo e Tatupedra. Cada um dos nove cenários copia o save nativo anterior ao habitat, prepara somente o HP atual do primeiro parceiro em 1, perde normalmente para o agente, confirma que flags e pedra pendente não foram concedidas, conclui a recuperação em casa e salva pelo menu. Um processo novo abre Continue com escritas desativadas, refaz o percurso real, vence o mesmo agente e exige a pedra correta e HP total.

Os nove cenários passaram no build SHA-1 `0a1b55c94bebf8d1d0560ff283e4388f3594fe75`. Antes/depois: Cerrado `[15,0,0]` → `[63,0,0]` e item 362; Caatinga `[63,0,0]` → `[255,0,0]` e item 363; Mata Atlântica `[255,0,0]` → `[255,0,96]` e item 364. Os saves de origem foram conferidos por hash e preservados. Relatório: `docs/intermediate-habitat-defeat-validation.json`; captura revisada: `docs/screenshots/intermediate-defeats/preview.png`.

Limites: HP=1 é uma fixture artificial e não prova desgaste natural, equipe com vários membros, status ou PP. O teste exercita batalha, derrota, retorno, cura, persistência, percurso e revanche pelas regras normais; não testa bolso especial cheio. Próximo passo funcional: substituir oponentes neutros provisórios por fauna coerente com cada habitat, mantendo a curva viável para os três parceiros; em paralelo, ampliar o cenário próprio das Terras Raras sem mover o eixo validado.

## Solo seco sob o círculo final — rotina 7

O corredor imediato das Terras Raras deixou de parecer uma passagem sobre água. As 21 células de `x=4..6`, `y=5..11` agora usam o metatile seco `0x0D9`, já disponível no tileset compartilhado com a Route 4/Pantanal. O conversor idempotente `tools/build_rare_lands_ground.py` altera somente o ID visual e preserva os bits de colisão e elevação de cada célula. Entrada `(5,9)`, Tio Sam `(5,8)`, cinco marcos, scripts e eixo vertical permaneceram nas mesmas coordenadas.

Build PASS, SHA-1 `0a1b55c94bebf8d1d0560ff283e4388f3594fe75`. A campanha inteira foi refeita desde jogos novos com Capivágua, Ararafogo e Tatupedra: 18 vitórias, cinco pedras, 15 interações nos marcos, desfecho e save/Continue depois de cada etapa passaram sem escrita de memória ou savestate. As três derrotas/revanche no Pantanal e as três no chefe também passaram; somente essas regressões preparam HP=1 artificialmente. Relatório: `docs/rare-lands-ground-validation.json`; captura revisada: `docs/screenshots/rare-lands-ground/preview.png`.

Limites: é uma faixa estreita que reutiliza textura herdada, não arte própria das Terras Raras. Água, prédio, penhasco, música e rochas continuam provisórios. Próximo passo funcional: ampliar a identidade visual do entorno imediato sem mover o eixo validado; depois substituir o cenário herdado da Mata Atlântica e do Pantanal. Derrotas no Cerrado, Caatinga e Mata Atlântica também permanecem sem regressão dedicada.

## Círculo das cinco pedras nas Terras Raras — rotina 6

O corredor do confronto ganhou cinco marcos de rocha ao redor de Tio Sam e do ponto de entrada, sem alterar as coordenadas `(5,9)` do jogador, `(5,8)` do chefe ou o eixo vertical usado pela campanha. Cada marco representa uma pedra e possui texto próprio sobre Águas, Raízes, Seca, Mata e Cheias. Os gráficos de rocha são herdados e provisórios, mas a composição cria uma identidade legível para o encerramento e permanece depois da vitória.

Build PASS, SHA-1 `e493f7397a77808d960c77f5aa731456719a21c7`. A campanha foi regenerada desde jogo novo para os três parceiros: 18 vitórias, cinco pedras, HP restaurado, desfecho e save/Continue voltaram a passar. `check_campaign_ending.py` agora interage com os dois marcos inferiores antes da batalha e com os três superiores depois dela; foram 15 interações no total, todas liberando os controles. A posição final `(5,7)`, as cinco pedras e flags `[255, 0, 224, 7]` persistiram após Continue. As seis regressões de derrota/retentativa do Pantanal e do chefe também passaram no novo hash. Relatório: `docs/rare-stone-circle-validation.json`; captura revisada: `docs/screenshots/rare-stone-circle/preview.png`.

Limites: o mapa, água, prédio, música e gráfico das rochas continuam herdados da base; não é um cenário final nem arte original das pedras. Os marcos usam uma única aparência e os textos não mudam antes/depois do desfecho. Próximo passo funcional: substituir gradualmente o entorno imediato do círculo por terreno de Terras Raras, preservando o eixo `(5,6..9)` e repetindo os testes de final e derrota; depois tratar Mata Atlântica e Pantanal.

## Derrota, recuperação e nova tentativa no chefe — rotina 5

Foi criado `tests/emulator/check_campaign_final_defeat.py` para validar o ramo de falha sem tornar o chefe artificialmente mais forte. O teste copia o save nativo de cinco pedras e altera somente o HP atual do primeiro parceiro para 1, por escrita opt-in no campo não cifrado. Flags, pedras, parceiro, oponentes e resultado não são injetados. A batalha acontece por controles normais e exige `B_OUTCOME_LOST`; depois, o jogo deve retornar à casa, recuperar HP, manter as cinco pedras e conservar os bytes de flags anteriores ao final `[255, 0, 224, 1]`.

Capivágua, Ararafogo e Tatupedra passaram. Cada ramo fez save normal sobrescrevendo a cópia, abriu Continue em outro processo com escritas desativadas, refez o percurso pela Floresta Amazônica, Campo Cerrado, Caatinga, Mata Atlântica e Pantanal e voltou às Terras Raras. A segunda tentativa venceu Tio Sam normalmente e terminou com flags `[255, 0, 224, 7]`. Os ciclos até a derrota foram 19, 20 e 18; a vitória posterior exigiu 98, 70 e 109 ciclos. Saves de origem permaneceram inalterados. Build sem mudança, SHA-1 `a3ac6c681a92b84b7d34863932930dca787c2155`. Relatório: `docs/campaign-final-defeat-validation.json`; captura revisada: `docs/screenshots/final-defeat/preview.png`.

O mesmo princípio foi aplicado ao agente do Pantanal antes da quinta pedra. Nos três ramos, a tentativa de cápsula contra o treinador consumiu um turno normal e levou à derrota com HP=1. Os bytes permaneceram `[255, 0, 96, 0]`, as quatro pedras anteriores foram preservadas e agente/recompensa continuaram pendentes. Depois de save/Continue, o jogador refez os habitats anteriores, venceu o agente e recebeu a Pedra das Cheias, chegando a `[255, 0, 224, 1]` com HP restaurado. Relatório: `docs/fifth-habitat-defeat-validation.json`.

Limites: o HP=1 é uma fixture artificial e não comprova dano acumulado naturalmente; apenas as batalhas, retornos, curas, persistência e novas tentativas usam as regras normais. Os testes não cobrem derrota no Cerrado, Caatinga ou Mata Atlântica, equipe com vários membros, status/PP ou bolso cheio. Próximo passo funcional: iniciar a substituição do cenário provisório de Terras Raras sem alterar coordenadas do fluxo validado; depois repetir as regressões de vitória e derrota afetadas.

## Recuperação entre habitats e curva de batalhas — rotina 4

As recompensas do Campo Cerrado, Caatinga, Mata Atlântica e Pantanal agora restauram a equipe antes da etapa seguinte. Isso remove o desgaste acumulado que obrigava todos os agentes posteriores a permanecer no nível 2. Os quatro agentes passaram a usar adversários neutros provisórios nos níveis 3, 4, 5 e 6; Tio Sam passou de um único adversário de nível 2 para dois de nível 7. A primeira missão mantém o confronto próprio já existente.

Build PASS, SHA-1 `a3ac6c681a92b84b7d34863932930dca787c2155`. A campanha foi regenerada desde jogo novo para Capivágua, Ararafogo e Tatupedra. Os 18 confrontos, cinco pedras, desfecho e save normal/Continue em processos novos passaram novamente, sem escrita de memória ou savestate. Os testes de cada habitat agora leem o HP real da equipe e exigem recuperação total: os 12 checkpoints ficaram em HP máximo. O chefe exigiu 110, 61 e 98 ciclos de entrada para Capivágua, Ararafogo e Tatupedra, respectivamente, contra 37–59 nos agentes balanceados mais longos, sem bloquear nenhum ramo. Relatórios atualizados: `docs/mission-current-validation.json` até `docs/campaign-ending-validation.json`.

Limites: a curva ainda usa Caterpie/Weedle e estratégia automatizada do primeiro golpe; portanto comprova progressão e ausência de bloqueio, não dificuldade final ou identidade temática. Derrota e recuperação não foram testadas nos cinco confrontos novos, e os mapas/arte permanecem provisórios. Durante a rotina, variantes ofensivas de nível 8 e com Rattata foram rejeitadas porque bloquearam Capivágua e/ou Ararafogo; tentativas passivas também não produziram uma derrota reproduzível no chefe aceito e não foram apresentadas como PASS. Próximo passo funcional: criar um teste reproduzível de derrota no confronto final, comprovando que as flags de conclusão não são concedidas e que o jogador pode se recuperar sem corromper as cinco pedras; depois refinar espécies e golpes mantendo os três ramos viáveis.

## Terras Raras e desfecho mínimo — rotina 3

A saída leste do Pantanal agora exige a Pedra das Cheias e leva à antiga Cerulean City, apresentada como Terras Raras. Tio Sam aparece como chefe próprio, inicia o sexto confronto da campanha e, depois da vitória, reconhece a reunião das cinco pedras e abandona o plano. Flags separadas registram a derrota do chefe e a conclusão da campanha; o personagem desaparece e o estado final persiste. O encerramento deixa explícito que se trata do fim da campanha atual, sem alegar créditos ou acabamento final.

Build PASS, SHA-1 `132a2eaddc09e0e8561fd5df9322945f17ccfcae`. A cadeia completa foi regenerada desde jogo novo para Capivágua, Ararafogo e Tatupedra: seis confrontos por parceiro, cinco itens especiais distintos (361–365), transição para Terras Raras, desfecho e save normal/Continue em processos novos, totalizando 18 vitórias testadas sem escrita de memória ou savestate. O estado final conservou as cinco pedras e os bytes de flags `[255, 0, 224, 7]` nos três ramos. Teste novo: `tests/emulator/check_campaign_ending.py`; relatório: `docs/campaign-ending-validation.json`; captura revisada: `docs/screenshots/campaign-ending/preview.png`.

Limites: Terras Raras reutiliza mapa, música e arte da base; a transição é provisória, Tio Sam usa um adversário neutro de nível 2 e o encerramento é somente textual, sem cena ou créditos. Não foram testados derrota no chefe, retorno a habitats anteriores, bolso cheio nas etapas novas nem balanceamento além da ausência de bloqueio para os três parceiros. Próximo passo funcional: executar regressão integral adicional, fortalecer o balanceamento sem bloquear nenhum parceiro e substituir primeiro as apresentações provisórias de Terras Raras e dos habitats quatro/cinco.

## Mata Atlântica, Pantanal e cinco pedras — rotina 3

A Caatinga ganhou uma saída provisória a leste para a antiga Route 3, agora apresentada como Mata Atlântica. Um quarto agente concede a Pedra da Mata, item especial 364, após batalha própria. A saída seguinte leva à antiga Route 4, agora apresentada como Pantanal, onde um quinto agente concede a Pedra das Cheias, item especial 365. Ambas as etapas têm flags separadas para batalha e recompensa, impedem duplicação, preservam a recompensa se o bolso estiver cheio e removem o agente depois da entrega. A mensagem final confirma que as cinco pedras foram reunidas e orienta buscar as Terras Raras.

Build PASS no checkpoint das cinco pedras, SHA-1 `e0153bb4a31deb6b78445da706011319eaa7ed1a`; a validação final da mesma cadeia foi repetida no build `132a2eaddc09e0e8561fd5df9322945f17ccfcae`. A campanha foi regenerada desde jogo novo para Capivágua, Ararafogo e Tatupedra. As cinco batalhas, os cinco itens distintos (361–365) e os saves normais/Continue em processos novos passaram nos três ramos, sem escrita de memória ou savestate. O primeiro balanceamento do quarto agente com criatura de água fez Ararafogo perder e foi rejeitado; a versão final usa adversários neutros provisórios de nível 2 e todos os ramos passaram. Testes novos: `tests/emulator/check_fourth_habitat.py` e `check_fifth_habitat.py`. Relatórios: `docs/fourth-habitat-validation.json` e `docs/fifth-habitat-validation.json`. Capturas revisadas em `docs/screenshots/fourth-habitat/preview.png` e `docs/screenshots/fifth-habitat/preview.png`.

Limites: Mata Atlântica e Pantanal ainda reutilizam mapas, música, NPCs e cenário rochoso da base; as transições são gatilhos provisórios e o balanceamento é apenas o mínimo necessário para não bloquear nenhum parceiro. Não foram testados derrota nas duas novas batalhas, bolso especial cheio, retorno entre habitats, encontro final ou desfecho. Próximo passo funcional: abrir a saída leste do Pantanal para as Terras Raras, criar o confronto com Tio Sam e um encerramento mínimo que exija as cinco pedras.

## Caatinga e Pedra da Seca — rotina 2

O bloqueio herdado ao norte do Campo Cerrado foi substituído por uma trilha curta e uma transição provisória reproduzível para a antiga Pewter City, agora apresentada como Caatinga. O agente do Cerrado recebe ID local e desaparece depois da recompensa, evitando bloquear o caminho. Na Caatinga, um terceiro agente do Tio Sam inicia uma batalha própria e concede a Pedra da Seca, item especial 363, somente depois da vitória. Flags separadas registram batalha e recompensa; mochila cheia preserva a entrega para uma nova tentativa. A mensagem confirma três de cinco pedras e orienta seguir ao leste.

Build PASS, SHA-1 `fe3e29d7190ccdc9ff968cc9496a0fac8d551710`. A campanha foi repetida desde jogo novo com Capivágua, Ararafogo e Tatupedra: primeira missão, Pedra das Águas, Campo Cerrado, Pedra das Raízes, transição para a Caatinga, terceira batalha, Pedra da Seca, save normal e Continue em processo novo, tudo PASS. Cada caso terminou com flags `0xFF` e uma unidade dos itens 361, 362 e 363, sem escrita de memória ou savestate. Relatórios resumidos: `docs/mission-current-validation.json`, `docs/second-habitat-validation.json` e `docs/third-habitat-validation.json`. Teste novo: `tests/emulator/check_third_habitat.py`; ajuste reproduzível da trilha: `tools/open_third_habitat_route.py`. Capturas reais revisadas em `docs/screenshots/third-habitat/preview.png`.

Limites: Caatinga, NPC, música e cenário ainda reutilizam arte da base; a transição do Cerrado é um gatilho provisório e a batalha usa um Ararafogo nível 2 antes do balanceamento. Não foram validados derrota na terceira batalha, bolso de itens especiais cheio, retorno ao Cerrado, saída leste nem habitat quatro. Próximo passo funcional: transformar a saída leste da Caatinga em acesso sequencial à Mata Atlântica, com quarta missão, batalha e quarta pedra.

## Campo Cerrado e Pedra das Raízes

A saída norte da floresta foi aberta em dois quadrados e conectada ao antigo Route 2, agora apresentado como Campo Cerrado. A conexão inversa volta à floresta. O mapa e a arte seguem provisórios, mas já há progressão real: depois da Pedra das Águas, o jogador encontra um segundo agente do Tio Sam, vence uma batalha e recebe a Pedra das Raízes como item especial distinto. Flags próprias impedem repetição da batalha e duplicação da pedra; mochila cheia permite retornar para receber a recompensa. A mensagem orienta seguir ao norte. O retorno à comunidade depois da primeira pedra agora recupera a equipe antes da segunda expedição.

Build PASS, SHA-1 `3acf79cee5b75e2db85e2964663952dcbd6775a9`, registrado em `SOURCE_STATE.json`, com mapas/eventos e símbolos regenerados. A primeira missão foi repetida desde jogos novos com Capivágua, Ararafogo e Tatupedra: batalha, ponte, Pedra das Águas e save/Continue PASS (`docs/mission-current-validation.json`). Em seguida, os três saves nativos percorreram a nova conexão, venceram o agente do Cerrado, mantiveram uma unidade de cada pedra e fizeram save normal/Continue em novo processo. Flags passaram de `0x0F` para `0x3F`; nenhuma escrita de memória ou savestate foi usada (`docs/second-habitat-validation.json`).

Capturas reais revisadas em `docs/screenshots/second-habitat/preview.png`; a mensagem da recompensa foi quebrada manualmente em linhas e não apresentou corte. O teste reproduzível está em `tests/emulator/check_second_habitat.py`; o ajuste binário da saída pode ser repetido por `tools/open_second_habitat_route.py`. `py_compile` e `git diff --check` PASS. Resultados completos ficam ignorados em `tests/emulator/results/routine-01-final2-*`. Nenhuma ROM ou save publicada.

Limites: o Campo Cerrado reutiliza mapa, cenário, NPC e música provisórios; o agente usa um Tatupedra nível 2 para garantir o fluxo mínimo antes do balanceamento. Não foram testados mochila especial cheia, derrota nessa segunda batalha, retorno ao sul depois da recompensa nem a continuação ao norte. Próximo passo funcional: transformar a saída norte do Campo Cerrado em acesso sequencial ao terceiro habitat, criar sua missão e terceira pedra, e estender o teste de campanha.

## Chão de terra no posto e cuidador

Criada uma pequena área de terra batida com arte original: 17 quadrados em x=10..14/y=15..17 e ligação ao norte em (11,13)/(11,14). O metatile novo 0x2F3 usa quatro tiles próprios e quatro cores da paleta 7 existente, sem alterar paletas, objetos, scripts ou coordenadas dos serviços. Todos os bits de colisão/altura do mapa foram comparados com a versão anterior e preservados. Arte e conversor reproduzível em `assets/amazon/village-ground/` e `tools/build_village_ground_asset.py`; reconversão byte a byte idêntica.

Build PASS após regenerar mapas/eventos, SHA-1 `68e8475e49945a4b44561bf9719ea61595cbcc54`, símbolos e `SOURCE_STATE.json` atualizados. Captura com equipe cheia regenerada e PASS (`docs/full-party-capture-validation.json`). `check_village_pc.py` agora percorre o contorno e a ligação ao norte e atende o cuidador: coordenadas alcançadas, controles liberados, HP completo nos seis slots, identidades/caixa e progresso preservados. Não foi injetado dano para esse atendimento. O restante da interface também passou: bloqueio antes da escolha, limites de equipe, depósito, Resumo, cancelamento de Libertar, retirada, save normal e Continue em novo processo. Contagens 6/1 → 5/2 → 6/1, sete animais preservados e origem intacta (`docs/village-pc-validation.json`).

Capturas reais revisadas em `docs/screenshots/village-ground/preview.png`: textura e paleta corretas, serviços visíveis. `py_compile` do conversor/teste e `git diff --check` PASS. Logs e saves de teste em `tests/emulator/results/ground-capture-01/` e `ground-pc-01/`, ignorados. Nenhuma ROM ou save publicada. O aviso herdado do conversor de tiles sobre o limite 76 é ignorado pelo próprio conversor diante dos tiles adicionais; a inclusão foi conferida no emulador.

Limites: origem de equipe cheia artificial; sem escrita de memória/savestates no teste de percurso/interface. Missão completa, derrota e libertação efetiva não foram reexecutadas; seus relatórios mantêm os hashes anteriores. Contorno do terreno ainda reto e vila/campanha incompletas. Próximo passo concreto: criar transições de terra para grama nas bordas dessa área, preservando colisões e validando novamente o acesso ao cuidador e terminal.

## Terminal próprio do posto de parceiros

A placa provisória foi substituída por um terminal original de madeira e tela verde, com detalhe de folhas. O gráfico tem ID próprio 152, quadro de 16×16 e usa a paleta NPC_GREEN existente no slot nativo 3. Nenhuma paleta compartilhada ou placa genérica foi alterada. O objeto permanece em (13,16), com o mesmo script e acesso por (13,15). Arte-fonte e instruções em `assets/amazon/storage/`; conversor determinístico `tools/build_storage_terminal_asset.py`. A redução simplifica os detalhes da arte-fonte.

Build PASS após regenerar explicitamente mapas/eventos: SHA-1 `fafcb6a2168cd7b0f7b7db3bf24359b0d161f31f`, registrado em `SOURCE_STATE.json`, com símbolos regenerados. Captura com equipe cheia regenerada e PASS (`docs/full-party-capture-validation.json`). Interface do posto PASS: bloqueio antes da escolha, recusa de guardar último parceiro/retirar com equipe cheia, depósito, Resumo, cancelamento de Libertar, retirada e save normal/Continue. Contagens 6/1 → 5/2 → 6/1; identidade, espécie, experiência/checksum, cápsulas e flags preservadas; save de origem intacto (`docs/village-pc-validation.json`).

Capturas reais revisadas em `docs/screenshots/storage-terminal/preview.png`: transparência, paleta e separação visual do jogador/cuidador adequadas nos pontos testados. A reconversão do PNG produziu bytes idênticos; `py_compile` do conversor e `git diff --check` PASS. Logs/PPM em `tests/emulator/results/terminal-capture-01/` e `terminal-pc-01/`, ignorados. Nenhuma ROM ou save publicada.

Limites: equipe cheia de origem artificial; teste da interface sem escrita de memória/savestates. Não reexecutados missão completa, derrota ou libertação efetiva; seus relatórios conservam os próprios hashes. A vila e outros habitats ainda usam cenário provisório. Próximo passo concreto: criar um pequeno caminho de chão próprio ao redor do posto e do cuidador, preservando coordenadas, colisões e acesso aos serviços; validar o percurso no emulador.

## Libertação efetiva em cópia isolada

Foram traduzidas somente as mensagens de sucesso e despedida da libertação em `src/strings.c`, preservando o placeholder do nome e as regras existentes. Build PASS: SHA-1 `a7583c0fdb6f030f180cd7057471848931b35f27`, registrado em `SOURCE_STATE.json`, com símbolos regenerados. A captura de origem foi regenerada neste build e passou (`docs/full-party-capture-validation.json`).

`check_village_release.py` passou operando em uma cópia nativa do save: guardou um Capivágua, cancelou Libertar sem alterar os animais, reabriu e selecionou SIM explicitamente para libertar Tatupedra da caixa. O slot de 80 bytes foi zerado; os outros cinco animais da equipe e o Capivágua na caixa preservaram identidade, espécie, experiência/checksums válidos. As contagens passaram de 5/2 para 5/1 entre equipe/PC, remoção intencional de exatamente um animal. Quatro cápsulas, flags `01` e posição foram preservadas. Save normal/Continue na cópia manteve o resultado, e o hash do save de origem permaneceu igual.

Relatório: `docs/village-release-validation.json`; capturas das confirmações, sucesso e despedida revisadas manualmente, sem corte observado para o nome testado, em `docs/screenshots/release/preview.png`. Logs/PPM em `tests/emulator/results/village-release-01/`, com origem `release-pt-capture-01/`, ignorados. `py_compile` e `git diff --check` PASS. Nenhuma ROM ou save é publicada.

Limites: equipe cheia de origem artificial; sem escrita de memória ou savestates no teste da interface. Não cobre libertação da equipe, recusa por ovo/HM, todos os nomes ou todos os caminhos. Esses avisos, títulos gráficos e conteúdo do resumo ainda podem conter textos herdados. Os relatórios de interface anteriores mantêm seus hashes e não foram apresentados como reexecutados neste build. Próximo passo concreto: criar um sprite próprio para o posto de parceiros, substituindo a placa provisória. O acabamento amazônico e os demais habitats continuam pendentes.

## Ações das caixas em português

Foram traduzidos em `src/strings.c` os rótulos Guardar, Retirar, Resumo, Marcar, Libertar e Cancelar, a indicação do parceiro escolhido, a pergunta de caixa de destino, a confirmação de saída e a pergunta de Libertar. Placeholders, ordem das opções e regras de armazenamento foram preservados. Não é uma tradução completa do PC: títulos gráficos, nomes das caixas, conteúdo do resumo e mensagens de libertação efetiva ainda contêm texto herdado.

Build PASS: SHA-1 `cd757ce280f4f57251e25987bab5d7788b59994d`, registrado em `SOURCE_STATE.json`, com símbolos regenerados. A captura de origem foi regenerada neste build e passou. O teste de interface passou com abertura/retorno do Resumo e abertura/cancelamento de Libertar por B, preservando dados antes da retirada. Guardar, retirar e save normal/Continue mantiveram contagens 6/1 → 5/2 → 6/1, sete animais, espécie, experiência, identidade/checksum, cápsulas e flags. Nenhum animal foi libertado.

Relatórios atualizados: `docs/full-party-capture-validation.json` e `docs/village-pc-validation.json`. Capturas revisadas manualmente em `docs/screenshots/box-actions/preview.png` e `docs/screenshots/village-pc/preview.png`, sem cortes observados nas páginas conferidas. Logs/PPM em `tests/emulator/results/box-actions-pt-capture-01/` e `village-pc-box-actions-01/`, ignorados. `py_compile` e `git diff --check` PASS. Nenhuma ROM ou save é publicada.

Limites: a origem da equipe cheia segue artificial, sem escritas/savestates no teste de interface. A visita ao Resumo não traduz nem valida todas as suas páginas. O teste cancela Libertar; não cobre a confirmação positiva, PC cheio, operações de mover parceiros/itens, marcas ou todos os nomes possíveis. Próximo passo concreto: traduzir as mensagens de libertação efetiva e validar a confirmação em uma cópia isolada do save, preservando a origem. O acabamento amazônico e os demais habitats continuam pendentes; fixtures anteriores precisam ser regeneradas para o hash atual.

## Menu principal do PC em português

Foram traduzidos em `src/strings.c` os cinco rótulos (Retirar parceiros, Guardar parceiros, Mover parceiros, Mover itens e Sair), suas descrições e os avisos de equipe cheia/último parceiro. As regras e a ordem das opções foram preservadas. A descrição de saída é genérica para não depender da vila em futuros pontos de acesso.

Build PASS: SHA-1 `55d4f85f0bf1c525102c96e3ecfeb61effbf5f6b`, registrado em `SOURCE_STATE.json`, com símbolos regenerados. A captura de origem com equipe cheia foi repetida neste build e passou. `check_village_pc.py` ganhou a recusa de guardar o último parceiro, obtido por controles normais em jogo novo, e capturas das cinco opções. Esse ramo não usa preparação artificial. A sequência de origem artificial com seis membros também passou: recusa de retirada, depósito, retirada de Tatupedra e save/Continue, preservando as contagens 6/1 → 5/2 → 6/1, identidade, espécie, experiência, checksum, cápsulas e flags.

Relatórios atualizados: `docs/full-party-capture-validation.json` e `docs/village-pc-validation.json`. Capturas das cinco descrições e dos dois avisos revisadas manualmente, sem cortes observados, em `docs/screenshots/village-pc/preview.png`. Resultados completos em `tests/emulator/results/pc-menu-pt-capture-01/` e `village-pc-pt-01/`, ignorados. `py_compile` e `git diff --check` PASS. Nenhuma ROM ou save é publicada.

Escopo: apenas o menu principal e os dois avisos de limite. As ações dentro das caixas, nomes de caixas, telas de resumo e parte da interface continuam herdadas/em inglês. Capturar a descrição de Mover parceiros/itens não testa suas operações. O ramo de seis membros continua vindo de fixture artificial, sem escritas no teste de interface; não valida obtenção natural dos seis animais ou PC cheio. Próximo passo concreto: traduzir as ações Guardar/Retirar/Resumo e a confirmação de saída dentro das caixas. O acabamento amazônico e os demais habitats permanecem pendentes; fixtures anteriores exigem regeneração para o hash atual.

## Posto de parceiros — acesso e retirada pelo PC

Não havia acesso ao armazenamento no percurso atual. Foi adicionado um posto em (13,16), perto do cuidador da vila, usando provisoriamente o sprite de placa. Antes da escolha do parceiro, orienta procurar a guia. Depois, abre diretamente o armazenamento nativo, sem os menus de Professor Oak/Bill da base. Ao sair, restaura o contexto de ajuda do mapa e libera os controles. O cuidador e sua cura/reposição não foram alterados.

Build PASS: SHA-1 `c6fa4ebc601246fe80bdfc59757b0c0dd7f7f18c`, registrado em `SOURCE_STATE.json`; mapas/eventos regenerados explicitamente e símbolos atualizados. A fixture de captura com equipe cheia foi regenerada neste build e passou (`docs/full-party-capture-validation.json`). `check_village_pc.py` passou com bloqueio antes do parceiro, recusa de WITHDRAW com seis membros, STORE de um Capivágua na caixa e WITHDRAW de Tatupedra nível 3 para a equipe. As contagens foram 6/1 → 5/2 → 6/1 entre equipe/PC, preservando os sete animais, espécie, experiência, identidade e checksums válidos. As quatro cápsulas e flags `01` permaneceram intactas.

Save normal/Continue em outro processo preservou equipe e caixa; o save de origem foi copiado e não alterado. A origem tem equipe cheia preparada artificialmente, mas **o teste de interface não habilita escrita de memória nem usa savestates**: todas as transferências foram feitas pelos controles. Relatório: `docs/village-pc-validation.json`. Capturas revisadas em `docs/screenshots/village-pc/preview.png`; logs/PPM em `tests/emulator/results/village-pc-ui-02/`, ignorados, com origem `pc-ui-capture-fixture-02/`. `py_compile` e `git diff --check` PASS. Nenhuma ROM ou save é publicada.

Os estados do emulador foram usados apenas na exploração local; o teste final é reproduzível por save nativo e exige fixture do mesmo hash de ROM. Não valida PC cheio, todas as caixas/opções ou aquisição natural de seis membros. Placa, nomes e mensagens internas do armazenamento ainda são provisórios/herdados, em inglês. Próximo passo concreto: localizar o menu principal do PC e os avisos de equipe cheia/último parceiro. O acabamento amazônico e os demais habitats continuam pendentes; relatórios anteriores mantêm os hashes dos seus builds.

## Captura com equipe cheia — envio ao PC

`check_capture.py --full-party-fixture` passou desde jogo novo com Capivágua. Depois da concessão real do parceiro e cinco cápsulas, o teste preparou uma equipe cheia copiando os 100 bytes válidos do parceiro nos cinco slots de reserva e ajustando a contagem para seis. Essa preparação é artificial e explicitamente habilitada no runner; não houve escrita no PC, no encontro selvagem, nas cápsulas, HP, RNG ou resultado da captura.

Tatupedra de nível 3 foi encontrado e enfraquecido por controles normais, capturado com uma cápsula (`B_OUTCOME_CAUGHT = 7`) e enviado ao primeiro slot da caixa 1. Os 420 slots do PC estavam vazios antes; depois, somente o primeiro estava ocupado, com espécie 1, nome TATUPEDRA, experiência 27 e checksum válido após decifrar os dados. A equipe continuou com seis animais; os cinco slots de reserva permaneceram byte a byte idênticos, e a identidade e a espécie do líder foram preservadas, com checksum válido. O consumo foi de cinco para quatro cápsulas. Save normal/Continue em outro processo sem escritas preservou equipe, PC, cápsulas e progresso.

O modo normal de captura também foi repetido, pois a condição de término da captura no teste compartilhado passou a exigir outcome 7 e retorno ao campo: PASS sem fixture, com criatura adicionada à equipe e persistência. Relatórios atuais: `docs/full-party-capture-validation.json` e `docs/capture-validation.json`. Build incremental PASS, SHA-1 inalterado `d99fc62a68c07488568c23e5c560d4774762572f`, símbolos regenerados; `py_compile` e `git diff --check` PASS. Resultados locais em `tests/emulator/results/full-party-capture-02/` e `capture-default-regression-01/`, ignorados. Nenhum código ou asset do jogo foi alterado; nenhuma ROM ou save é publicada.

Limites: não houve obtenção natural dos seis membros da equipe, retirada pela interface do PC, PC cheio ou validação estatística de captura. A prova de armazenamento usa os layouts fixados de PokemonStorage/BoxPokemon e verifica espécie, nome, experiência e checksum, não só um apelido em memória. Próximo passo concreto: conferir o acesso ao PC na vila e a retirada do animal armazenado. O acabamento visual amazônico e os demais habitats continuam pendentes.

## Diálogo normal da mãe alinhado à guia

As duas variantes de aparência agora recebem a orientação de procurar a guia na vila para escolher o parceiro, substituindo a referência ao professor/laboratório herdada da base. A condição de descanso foi corrigida de `FLAG_BEAT_RIVAL_IN_OAKS_LAB` para `FLAG_AMAZON_PARTNER_CHOSEN`: depois da escolha real do parceiro, a mãe usa o diálogo e a rotina de cura já existentes. Antes da escolha, continua apenas orientando, sem conceder criaturas ou itens.

Build PASS: SHA-1 `d99fc62a68c07488568c23e5c560d4774762572f`, registrado em `SOURCE_STATE.json`, com símbolos regenerados. `check_mom_dialogue.py` passou nas duas aparências desde jogos novos: conversa inicial sem alterar progresso, saída da casa, concessão real de Capivágua e cinco cápsulas pela guia, retorno normal e descanso com HP restaurado para 21/21 e 22/22, cápsulas preservadas e movimento liberado. A cura foi testada com **HP=1 preparado artificialmente** depois da escolha; nenhuma flag, criatura ou item foi injetado. Isso não comprova dano natural de batalha, status/PP ou todos os tamanhos de equipe, e não inclui novo ciclo de save.

Relatório: `docs/mom-dialogue-validation.json`. Capturas das duas aparências revisadas manualmente, sem corte observado nas páginas conferidas: `docs/screenshots/mom-dialogue/preview.png`. A primeira rota de teste precisou considerar que a entrada deixa o jogador em (5,8); a sequência final também para assim que o diálogo libera o controle, evitando iniciar outra conversa por A extra. Execução final PASS em `tests/emulator/results/mom-dialogue-20261113-v3/`; `py_compile` e `git diff --check` PASS. Logs e PPM completos ficam ignorados. Nenhuma ROM ou save é publicada.

Os relatórios anteriores continuam identificados pelos hashes dos respectivos builds; fixtures que exigem o hash atual devem ser regeneradas antes do uso. Próximo passo concreto: validar captura com equipe cheia e envio ao PC. O acabamento visual amazônico e os demais habitats continuam pendentes.

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

1. Ampliar captura/armazenamento (outras espécies e PC cheio). Acesso, depósito e retirada pela interface passaram no posto da vila, a partir de uma equipe cheia artificial. Envio ao PC com equipe cheia artificial passou, incluindo persistência; obtenção natural de seis animais não foi validada. A coleta pelo objeto com bolsa cheia passou em fixture artificial: recusa preservou objeto/flags; liberar um slot permitiu coletar sem perda dos outros itens. Reposição pelo cuidador, recusa com bolso cheio e retomada após liberar um slot passaram em fixtures artificiais, não em gameplay natural. Uma captura natural de Tatupedra com Capivágua e consumo de cápsula passou, incluindo save/Continue. Quantidade unitária e ausência de duplicação após revisitar o local/curador foram conferidas com Ararafogo e Tatupedra. Missão vitoriosa e save/Continue validados com os três parceiros no build 2cd252b4dbb1926e28e89944333d5c7b033fa304. Derrota/recuperação, save/Continue e manutenção do bloqueio após perder foram revalidados para os três parceiros no build dos textos em português b89c8c560eae9d999b68fd22b6ace17409b2f913.
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
