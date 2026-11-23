# Santuário das Cinco Pedras

O pedestal original usa cinco gemas ao redor de um núcleo verde vivo. O
desenho de 16×16 pixels reutiliza a paleta nativa `npc_green.pal`; nenhuma
paleta compartilhada é alterada. O índice zero permanece transparente.

Para reproduzir a fonte e o sprite indexado, execute na raiz:

```bash
python3 tools/build_rare_sanctuary_asset.py
```

O resultado usado pelo jogo fica em
`pokefirered/graphics/object_events/pics/misc/amazon_rare_sanctuary.png`.
O objeto possui ID 153, quadro único e substitui visualmente o marco superior
em `(5,6)` somente depois da conclusão da campanha. O ponto interativo central
em `(5,8)` continua sendo piso passável, evitando bloquear o eixo da campanha.
