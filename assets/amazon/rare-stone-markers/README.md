# Marcos das cinco pedras

Cinco objetos originais de 16×16 substituem os rochedos genéricos ao redor
do eixo final das Terras Raras. Água usa uma gota, Raízes uma ramificação,
Seca um sol, Mata uma folha e Cheias duas ondas. O marco de Cheias ocupa o
ponto do santuário e é substituído pelo Santuário das Cinco Pedras após o
desfecho.

Todos reutilizam `npc_green.pal`, sem alterar paletas compartilhadas. Para
recriar as fontes RGBA e os PNGs indexados usados pelo jogo:

```bash
python3 tools/build_rare_stone_markers.py
```

As posições, colisões, scripts e flags dos objetos originais são preservados.
