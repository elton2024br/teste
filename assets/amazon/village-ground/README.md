# Chão do posto da vila

`dirt-source.png` é a arte original de terra batida gerada para esta etapa.
O conversor reduz a textura para 16×16 por vizinho mais próximo e usa somente
quatro cores da paleta 7 já existente na vila, sem modificar essa paleta.

Na raiz, com Python 3 e Pillow:

```bash
python3 tools/build_village_ground_asset.py
```

O script pode ser repetido nesta versão: instala quatro tiles a partir do índice
local 208 e o metatile 0x2F3 no tileset secundário de Pallet Town. Preserva os tiles
anteriores e os bits de colisão/altura do mapa. Recusa formatos inesperados.
A área ocupa x=10..14, y=15..17, com ligação em (11,13) e (11,14): 17 quadrados.
Coordenadas e scripts do cuidador e terminal permanecem iguais. O terreno tem
comportamento normal, como a grama curta substituída. O contorno ainda é reto;
não é uma reforma completa da vila ou das trilhas dos demais habitats.

A compilação gera os formatos 4bpp/lz a partir do PNG; esses produtos não são
versionados. O aviso herdado sobre `-num_tiles 76` informa que o conversor ignora
o limite antigo ao encontrar tiles não transparentes; os novos tiles são incluídos.
