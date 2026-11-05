# Artes da intro

Artes geradas para Bichos do Brasil nesta etapa: capa amazônica em 3:2 e folha com Bia/Tio Sam em duas colunas. Bia é a guia da aventura; Tio Sam é o magnata fictício da história.

`tools/build_intro_assets.py` reduz a capa para 240×160 RGB555 e converte os personagens para 64×96, com fundo transparente e paletas compatíveis com o motor da intro. Execute com Python 3 e Pillow 12.1 ou posterior. A reconversão foi conferida byte a byte nesta etapa. Os resultados ficam em `pokefirered/graphics/amazon_intro/` e `pokefirered/graphics/oak_speech/`.

A capa é uma imagem estática; não há uma cinemática animada nova. A música, os retratos do jogador e partes da interface continuam provisórios da base.
