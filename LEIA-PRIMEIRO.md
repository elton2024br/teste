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

Os três parceiros percorreram a campanha mínima na ROM atual, dos cinco habitats às Terras Raras. As seis batalhas com curva progressiva, as cinco pedras distintas, a recuperação entre habitats, o confronto final, o desfecho e save/Continue passaram nos três ramos (`docs/mission-current-validation.json` até `docs/campaign-ending-validation.json`). Derrota, recuperação, persistência, retorno e nova tentativa passaram no Cerrado, Caatinga, Mata Atlântica, Pantanal e no chefe para os três parceiros com HP=1 artificial (`docs/intermediate-habitat-defeat-validation.json`, `docs/fifth-habitat-defeat-validation.json` e `docs/campaign-final-defeat-validation.json`). A campanha usa Lobo-guará, Asa-branca, Mico-leão, Tuiuiú e Onça-pintada originais como adversários. O ponto imediato da missão do Pantanal agora é uma ilha verde cercada por água, ainda dentro da Route 4 herdada (`docs/pantanal-checkpoint-validation.json`). Nas Terras Raras, uma lagoa substitui o ginásio herdado ao lado do círculo; a resolução revela o santuário com transição e fanfarra e persiste após Continue (`docs/rare-lands-lagoon-validation.json`). Depois do fim, o santuário oferece retorno opcional à vila sem fechar o caminho de revisita (`docs/sanctuary-village-return-validation.json`). O HANDOFF identifica hashes e limites.

Três composições naturais de dois membros concluíram toda a campanha: Capivágua + Tatupedra (`docs/natural-two-member-campaign-validation.json`), Ararafogo + Tatupedra (`docs/natural-ararafogo-two-member-campaign-validation.json`) e Tatupedra + Ararafogo (`docs/natural-tatupedra-two-member-campaign-validation.json`). Todas passaram por cuidador, troca obrigatória na primeira batalha, cinco pedras, Tio Sam, santuário e save/Continue com identidades preservadas. As três também passaram por derrota dos dois membros, recuperação, Continue, retorno e revanche nos quatro habitats posteriores (`docs/natural-team-intermediate-defeat-matrix-validation.json`); o chefe tem evidência nos relatórios anteriores. O círculo final usa marcos próprios para as cinco pedras, incluindo ondas para Cheias antes de sua troca pelo santuário (`docs/rare-stone-markers-validation.json`). O envio de uma captura ao PC com equipe cheia também passou em preparação artificial (`docs/full-party-capture-validation.json`). Equipes sintéticas de dois membros percorreram os quatro habitats posteriores com os três parceiros; as 12 recompensas restauraram HP, veneno e PP de ambos (`docs/team-recovery-validation.json`). A campanha mínima ainda não é uma versão final: os habitats posteriores à floresta inicial e partes do cenário das Terras Raras reutilizam mapas e arte provisórios; balanceamento, outros status e encerramento precisam de acabamento.

O encerramento agora inclui um epílogo curto sobre a recuperação dos cinco habitats, a proteção coletiva das pedras e a continuidade da jornada (`docs/campaign-epilogue-validation.json`). Ao voltar pelo santuário, a guia da vila reconhece o guardião e oferece viagem opcional de volta. Os dois sentidos podem ser recusados, e o caminho normal continua aberto. Epílogo, retorno bidirecional, recepção, travessia completa e derrota/revanche final passaram com os três parceiros no mesmo build.

As mensagens de libertação e despedida foram traduzidas e a confirmação foi testada somente em cópia isolada, preservando o save de origem (`docs/village-release-validation.json`).

A mãe agora orienta procurar a guia antes da escolha e oferece descanso depois de receber o parceiro. Veja as [capturas da conversa](docs/screenshots/mom-dialogue/preview.png) e os limites do teste em `docs/mom-dialogue-validation.json`.

Não há ROM comercial completa nem saves neste repositório. Os pequenos binários multiboot em `pokefirered/data/` pertencem à estrutura da base e são necessários à compilação. Consulte os avisos e licenças dos projetos de origem; os direitos dos componentes de terceiros permanecem com seus titulares.
