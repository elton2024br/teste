# Mico-leão

Arte original em pixel art para o adversário obrigatório da Mata Atlântica. O slot técnico continua sendo `SPECIES_HOOTHOOT`, mas nome, gráficos, atributos, golpes e evolução são substituídos no jogo.

Reconversão:

```bash
python3 tools/build_micoleao_asset.py
```

O script gera frente, costas, ícone, pegada e paletas. `micoleao-source.png` é a folha transparente de referência. A paleta alternativa repete a normal neste marco. Cry, textos e categoria de Pokédex ainda são herdados do slot técnico. A arte é deliberadamente simples e pode receber refinamento posterior sem mudar o ID da espécie ou os saves.
