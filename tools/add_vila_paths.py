"""Build a repeating walkable stone tile from the new house palette."""
from pathlib import Path
from PIL import Image
import struct
s=Path('/workspace/pokefirered/data/tilesets/secondary/pallet_town')
colors=[tuple(map(int,l.split())) for l in (s/'palettes/07.pal').read_text().splitlines()[3:]]
def nearest(c):return min(range(1,16),key=lambda i:sum((a-b)**2 for a,b in zip(c,colors[i])))
sand,edge,light=map(nearest,[(203,170,107),(143,114,73),(235,208,151)])
im=Image.open(s/'tiles.png');assert im.size==(128,96)
new=Image.new('P',(128,104));new.putpalette(im.getpalette());new.paste(im,(0,0))
for y in range(16):
 for x in range(16):
  row=y//8;xx=(x+(4 if row%2 else 0))%8
  color=edge if y%8==7 or xx==7 else light if y%8==0 else sand
  tile=(y//8)*2+x//8+192;new.putpixel(((tile%16)*8+x%8,(tile//16)*8+y%8),color)
new.save(s/'tiles.png')
p=s/'metatiles.bin';first=640+p.stat().st_size//16
p.write_bytes(p.read_bytes()+struct.pack('<8H',*[((640+192+i)|(7<<12)) for i in range(4)],0,0,0,0))
p=s/'metatile_attributes.bin';p.write_bytes(p.read_bytes()+bytes(4))
p=Path('/workspace/pokefirered/data/layouts/PalletTown/map.bin');a=list(struct.unpack('<480H',p.read_bytes()))
road={(x,8) for x in range(6,16)}|{(11,y) for y in range(9,18)}|{(x,10) for x in range(6,12)}|{(6,9),(15,8)}
for x,y in road:a[y*24+x]=first|0x3000
p.write_bytes(struct.pack('<480H',*a))
