# Instrução atual para esta versão GitHub

O projeto está completo em termos de arquivos-fonte neste repositório. Use pokefirered/ e agbcc/ diretamente. Não clone uma segunda base e não aplique source.patch. As menções a ZIP, source.patch e project/ abaixo são históricas. Nesta estrutura project/docs = docs, project/tools = tools, project/assets = assets e project/tests = tests.

# ATENCAO: PACOTE DE CODIGO COMPLETO

A restauracao ja foi feita na nuvem. O conteudo abaixo conserva o historico e as pendencias, mas suas instrucoes de clonar e aplicar source.patch estao SUPERADAS: use diretamente a pasta pokefirered/ deste pacote e LEIA-PRIMEIRO.md. Nao repita a aplicacao do patch.

# Bichos do Brasil — ponto de retomada

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

1. Repetir a missão atual com Ararafogo e Tatupedra; testar derrota/recuperação, captura, tentativas de duplicar a pedra e falta de espaço.
2. Ampliar os testes de save normal. O comando experimental flushsave do runner retorna zero bytes com esta biblioteca mGBA e encerrou com código 11; o save nativo via VFile foi gravado e carregou. Não confundir esse problema do helper com o teste de Continue. Corrigir/remover esse comando, usar a persistência nativa e confirmar o ciclo completo.
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
