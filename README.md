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

Os três parceiros percorreram a campanha mínima na ROM atual: Floresta Amazônica, Campo Cerrado, Caatinga, Mata Atlântica, Pantanal e Terras Raras. As seis batalhas, as cinco pedras distintas, a recuperação entre habitats, o confronto final com dois adversários, o desfecho mínimo e save/Continue passaram nos três ramos (`docs/mission-current-validation.json` até `docs/campaign-ending-validation.json`). Derrota, recuperação, persistência, retorno e nova tentativa também passaram nos agentes do Cerrado, Caatinga, Mata Atlântica, Pantanal e no chefe para os três parceiros, com HP=1 preparado artificialmente (`docs/intermediate-habitat-defeat-validation.json`, `docs/fifth-habitat-defeat-validation.json` e `docs/campaign-final-defeat-validation.json`). As Terras Raras ganharam um círculo interativo com cinco marcos sobre uma faixa de solo seco, ainda usando gráficos provisórios ([capturas](docs/screenshots/rare-lands-ground/preview.png) e [relatório](docs/rare-lands-ground-validation.json)). Veja também a [Mata Atlântica](docs/screenshots/fourth-habitat/preview.png), o [Pantanal](docs/screenshots/fifth-habitat/preview.png), a [derrota/retorno](docs/screenshots/intermediate-defeats/preview.png) e o [desfecho](docs/screenshots/campaign-ending/preview.png). O HANDOFF identifica hashes e limites.

Uma captura natural de Tatupedra com Capivágua e save/Continue passou (`docs/capture-validation.json`), incluindo consumo da cápsula. O envio de uma captura ao PC com equipe cheia passou em preparação artificial (`docs/full-party-capture-validation.json`). O posto perto do cuidador tem um terminal próprio de madeira e tela verde ([arte e conversão](assets/amazon/storage/README.md)) e permite guardar e retirar parceiros. A campanha mínima existe, mas não é uma versão final: os quatro habitats posteriores à floresta inicial e quase todo o cenário das Terras Raras ainda usam mapas e arte provisórios; o chefe, o balanceamento e o encerramento precisam de acabamento.

As mensagens de libertação e despedida foram traduzidas e a confirmação foi testada somente em cópia isolada, preservando o save de origem (`docs/village-release-validation.json`).

A mãe agora orienta procurar a guia antes da escolha e oferece descanso depois de receber o parceiro. Veja as [capturas da conversa](docs/screenshots/mom-dialogue/preview.png) e os limites do teste em `docs/mom-dialogue-validation.json`.

Não há ROM comercial completa nem saves neste repositório. Os pequenos binários multiboot em `pokefirered/data/` pertencem à estrutura da base e são necessários à compilação. Consulte os avisos e licenças dos projetos de origem; os direitos dos componentes de terceiros permanecem com seus titulares.
