# Onça-pintada

Arte original em pixel art para o adversário de Tio Sam nas Terras Raras. O slot técnico continua sendo `SPECIES_SPINARAK`, mas nome, gráficos, atributos e evolução são substituídos no jogo.

Reconversão:

```bash
python3 tools/build_oncapinta_asset.py
```

O script gera frente, costas, ícone, pegada e paletas. `oncapinta-source.png` é a folha transparente de referência. A paleta alternativa repete a normal neste marco. Cry, textos e categoria de Pokédex ainda são herdados do slot técnico. O nome de batalha `ONCA-PINTA` cabe no limite técnico de dez caracteres. A arte é deliberadamente simples e pode receber refinamento posterior sem mudar o ID da espécie ou os saves.
