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

O primeiro percurso com Capivágua foi testado até vencer o agente, liberar a passagem, receber a Pedra das Águas e retornar à vila. O save normal foi reaberto em outro processo, preservando o item e o progresso. Ainda faltam testes equivalentes com os outros parceiros, derrota, captura, casos de inventário e o acabamento visual amazônico. A campanha dos cinco habitats não está concluída.

Não há ROM comercial completa nem saves neste repositório. Os pequenos binários multiboot em `pokefirered/data/` pertencem à estrutura da base e são necessários à compilação. Consulte os avisos e licenças dos projetos de origem; os direitos dos componentes de terceiros permanecem com seus titulares.
