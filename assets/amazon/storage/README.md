# Terminal do posto de parceiros

Arte original gerada para este projeto: terminal de madeira com tela verde,
painel de controles e detalhe de folhas. `terminal-source.png` conserva a fonte
com transparência. A conversão para 16×16 simplifica os detalhes pequenos.

Para reproduzir o sprite indexado, execute na raiz:

```bash
python3 tools/build_storage_terminal_asset.py
```

Requer Python 3 e Pillow. O conversor recorta a área transparente, reduz por
vizinho mais próximo e aproxima as cores à paleta nativa `npc_green.pal`.
O índice zero é transparente. A paleta compartilhada permanece intacta.
O resultado é `pokefirered/graphics/object_events/pics/misc/amazon_storage_terminal.png`;
o build gera o formato 4bpp. O objeto tem identificador próprio (152), quadro
único de 16×16 e ocupa o mesmo ponto (13,16) do posto anterior na vila.
