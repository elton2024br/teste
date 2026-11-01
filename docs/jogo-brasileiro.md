# Bichos do Brasil: caminho para uma versão baseada em FireRed

## Estado verificado

O projeto atual é um protótipo independente em HTML e JavaScript: batalha, captura e exploração por botões. Ele não carrega ROMs nem possui emulador. A arte gerada é uma proposta visual, não um conjunto de tiles e sprites já pronto para GBA.

A ROM indicada em `G:\duolingo\Pokemon_ FireRed Version` não está disponível no ambiente Linux da nuvem. Não foi aberta, modificada ou validada. O nome do arquivo ou pasta não identifica a edição nem a revisão.

## EGM instalado localmente

Pacote original: https://github.com/google/elephant-goldfish-model

Commit e detalhes em `.agents/egm-installation.json`. O pacote completo está em `.agents/vendor/egm`; sete links em `.agents/skills` permitem descoberta local em uma nova sessão de um host compatível. A configuração global do Codex desta máquina é somente para leitura, portanto não foi registrado globalmente. A descoberta em uma nova sessão e o fluxo completo de revisão ainda não foram testados.

O EGM ajuda a definir requisitos, escrever especificações e revisar decisões. Não contém editor de mapas, emulador ou conversor de ROM. Para uso: começar com `egm-brainstorm`, consolidar com `egm-draft` e avaliar com `egm-review`. As etapas interativas e os revisores independentes são parte do fluxo; ainda não foram executados neste projeto.

## Caminho principal: ROM hack para GBA

Usar FireRed como base preserva exploração por tiles, eventos, batalhas, menus e compatibilidade com emuladores GBA. O desenvolvimento fica em um projeto separado do protótipo web, para não misturar ferramentas e formatos.

1. Receber a ROM e identificar tamanho, cabeçalho, código, revisão e SHA-1, mantendo o original intacto. `tools/inspect_rom.py` faz essa leitura. Um arquivo compactado deve ser extraído primeiro.
2. Avaliar a compatibilidade com https://github.com/pret/pokefirered e seguir seu `INSTALL.md` para a versão identificada. O README oficial declara FireRed inglês com SHA-1 `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` e revisão 1 com `dd5945db9b930750cb39d00c84da8571feebf417`. Uma tradução ou ROM modificada exige avaliação própria; não assumir que os endereços e ferramentas serão iguais.
3. Validar primeiro o build da base sem alterações, comparando a saída com a revisão selecionada. Só depois alterar conteúdo.
4. Criar uma primeira área pequena: Vila Ipê, casa do jogador, casa de cura, rota de mata e um encontro capturável. Incluir diálogos em português e um evento de escolha do parceiro.
5. Produzir arte própria no formato exigido pelo motor: tiles, paletas, sprites de frente e costas, animações, ícones e colisões. A ilustração de apresentação serve como referência; ela não pode ser importada inteira como mapa funcional.
6. Substituir inicialmente três espécies por Capivágua, Ararafogo e Tatufolha, incluindo dados, nomes, ataques e textos. Expandir o elenco e as evoluções depois que o ciclo inicial funcionar.
7. Validar em emulador: movimento, colisões, portas, diálogos, encontro, captura, cura, derrota e salvar/carregar. Uma imagem gerada ou build concluído não comprova esses comportamentos.
8. Entregar as mudanças como patch BPS/IPS associado ao hash exato da base, sem incluir a ROM original na entrega.

## Alternativa: continuar como jogo original de navegador

O protótipo existente pode ganhar mapa com movimento, colisões, NPCs, telas de batalha e salvamento local. Isso mantém execução por navegador e facilita compartilhar, mas exige implementar esses sistemas. A ROM não é necessária para esse caminho e não pode ser carregada diretamente pelo HTML atual.

## Primeiro marco proposto

Uma demonstração com Vila Ipê, um parceiro, uma rota, uma criatura capturável e casa de cura. Critério de conclusão: sair da vila, entrar em uma batalha, capturar, voltar para curar e recuperar o progresso após reiniciar.

A plataforma final (ROM hack ou navegador) ainda precisa ser definida pelo usuário; a referência explícita à ROM orienta a investigação inicial para GBA. Nenhum motor novo foi escolhido ou instalado nesta etapa.

## Como identificar no Windows sem enviar a ROM

Com Python instalado, copie `tools/inspect_rom.py` para o computador e execute, ajustando o caminho se necessário:

```powershell
py tools/inspect_rom.py "G:\duolingo\Pokemon_ FireRed Version"
```

O argumento pode ser uma pasta com arquivos `.gba` ou o caminho completo de um arquivo. A ferramenta imprime somente identificação e hashes; não altera a ROM. Enviar o relatório permite avaliar compatibilidade; enviar o próprio arquivo também permite inspecioná-lo aqui.
