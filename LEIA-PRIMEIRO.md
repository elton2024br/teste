# Bichos do Brasil

Aventura GBA em desenvolvimento, com animais brasileiros, cinco habitats e cinco pedras que abrem o caminho para as Terras Raras. O jogador escolhe Capivágua, Ararafogo ou Tatupedra e enfrenta os planos do magnata fictício Tio Sam.

## Continuar no Antigravity

Clone este repositório em `G:\duolingo\BichosDoBrasil` e abra essa pasta no Antigravity. Peça ao agente para ler `AGENTS.md` e `HANDOFF.md` e continuar pelas pendências. O código já está preparado: não é necessário clonar outra base nem aplicar patches.

```powershell
git clone https://github.com/elton2024br/teste.git G:\duolingo\BichosDoBrasil
```

Se a pasta já existir e contiver trabalho, preserve e inspecione antes de clonar ou substituir arquivos.

## Compilar

Use Ubuntu/WSL. Se ainda não houver distribuição instalada, configure-a no Windows primeiro. No terminal Ubuntu:

```bash
cd /mnt/g/duolingo/BichosDoBrasil
bash setup-linux.sh
```

O script instala dependências de compilação, constrói o compilador-fonte incluído em `agbcc/` e compila `pokefirered/`. Confira `logs/` em caso de falha. O script foi conferido sintaticamente; a execução no Windows/WSL ainda deve ser validada. A compilação foi realizada no ambiente Linux anterior.

## Pastas

- `pokefirered/`: fontes do jogo já alterados, baseados em pret/pokefirered.
- `agbcc/`: compilador-fonte usado pela base.
- `assets/`: artes-fonte e conversões atuais.
- `docs/egm/`: decisões e revisões de design.
- `tests/emulator/`: apoio aos testes no mGBA; adapte caminhos e confira as limitações do helper.
- `HANDOFF.md`: estado do desenvolvimento e pendências.

Os caminhos `project/docs`, `project/tools` ou `project/assets` nos documentos do pacote anterior correspondem agora a `docs`, `tools` e `assets` na raiz deste repositório. Caminhos `/workspace` são históricos e precisam de adaptação local.

## Estado real

A intro tem capa amazônica própria, Bia e Tio Sam com novos retratos, apresentação de Capivágua e história das cinco pedras. Escolha de aparência/nome e save/Continue foram testados no mGBA. Veja os [prints da intro](docs/screenshots/intro/preview.png) e o [relatório de validação](docs/intro-validation.json). Parte da interface, personagens e música ainda usa a base original.

Os três parceiros têm validações atuais da primeira missão e do save/Continue após a Pedra das Águas em `docs/mission-current-validation.json`. Campo Cerrado e Caatinga agora formam a segunda e a terceira etapas, com Pedra das Raízes e Pedra da Seca. O percurso das três missões e save/Continue passou com Capivágua, Ararafogo e Tatupedra (`docs/second-habitat-validation.json` e `docs/third-habitat-validation.json`); o HANDOFF identifica os hashes e limites.

Uma captura natural de Tatupedra com Capivágua e save/Continue passou (`docs/capture-validation.json`), incluindo consumo da cápsula. O envio de uma captura ao PC com equipe cheia passou em preparação artificial (`docs/full-party-capture-validation.json`). O posto perto do cuidador tem um terminal próprio de madeira e tela verde ([arte e conversão](assets/amazon/storage/README.md)) e permite guardar e retirar parceiros. O posto e o cuidador compartilham uma pequena área de terra batida ([arte e conversão](assets/amazon/village-ground/README.md)). A campanha ainda precisa dos habitats quatro e cinco, Terras Raras e desfecho; Campo Cerrado e Caatinga ainda usam arte provisória.

As mensagens de libertação e despedida foram traduzidas e a confirmação foi testada somente em cópia isolada, preservando o save de origem (`docs/village-release-validation.json`).

A mãe agora orienta procurar a guia antes da escolha e oferece descanso depois de receber o parceiro. Veja as [capturas da conversa](docs/screenshots/mom-dialogue/preview.png) e os limites do teste em `docs/mom-dialogue-validation.json`.

Não há ROM comercial completa nem saves neste repositório. Os pequenos binários multiboot em `pokefirered/data/` pertencem à estrutura da base e são necessários à compilação. Consulte os avisos e licenças dos projetos de origem; os direitos dos componentes de terceiros permanecem com seus titulares.
