"""Convert original house art into GBA tiles and install the village layout."""
from PIL import Image
from pathlib import Path
import struct
root=Path('/workspace/pokefirered');s=root/'data/tilesets/secondary/pallet_town'
assert Image.open(s/'tiles.png').size == (128,40), 'Execute somente sobre os assets originais de Pallet Town.'
art=Image.open('/workspace/teste/assets/vila-ipe/casa-original.png').convert('RGB').resize((80,80),Image.Resampling.NEAREST)
mask=[r>180 and b>150 and g<100 for r,g,b in art.getdata()]
# Background is reserved as transparent index zero. Quantize only the foreground.
pixels=list(art.getdata());foreground=[c for c,m in zip(pixels,mask) if not m]
strip=Image.new('RGB',(len(foreground),1));strip.putdata(foreground)
q=strip.quantize(colors=15,method=Image.Quantize.MEDIANCUT);pal=q.getpalette()[:45]
colors=[tuple(pal[i:i+3]) for i in range(0,45,3)]
# GBA colors use five bits per channel.
colors=[tuple((v>>3)<<3 for v in c) for c in colors]
indices=[]
for c,m in zip(pixels,mask):
 indices.append(0 if m else 1+min(range(15),key=lambda i:sum((a-b)**2 for a,b in zip(c,colors[i]))))
old=Image.open(s/'tiles.png');tile_count=old.width*old.height//64
canvas=Image.new('P',(128,96));canvas.putpalette(old.getpalette());canvas.paste(old,(0,0))
for t in range(100):
 tx,ty=t%10,t//10;dest=tile_count+t;dx,dy=(dest%16)*8,(dest//16)*8
 for y in range(8):
  for x in range(8):canvas.putpixel((dx+x,dy+y),indices[(ty*8+y)*80+tx*8+x])
canvas.save(s/'tiles.png')
(s/'palettes/07.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in [(0,0,0)]+colors)+'\n')
mt=list(struct.unpack('<%dH'%((s/'metatiles.bin').stat().st_size//2),(s/'metatiles.bin').read_bytes()));attr=bytearray((s/'metatile_attributes.bin').read_bytes())
first=640+len(mt)//8;grass=mt[(0x296-640)*8:(0x296-640)*8+4];doorattr=attr[(0x2a3-640)*4:(0x2a3-640)*4+4]
for y in range(5):
 for x in range(5):
  tiles=[640+tile_count+(y*2+oy)*10+x*2+ox for oy in range(2) for ox in range(2)]
  mt+=grass+[t|(7<<12) for t in tiles]
  attr+=doorattr if (x,y)==(2,4) else bytes(4)
(s/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(mt),*mt));(s/'metatile_attributes.bin').write_bytes(attr)
p=root/'data/layouts/PalletTown/map.bin';blocks=list(struct.unpack('<480H',p.read_bytes()))
for left in [4,13]:
 # Clear old roofs, walls and shadows before placing the new footprint.
 for y in range(3,8):
  for x in range(left,left+7):blocks[y*24+x]=0x3296
 for y in range(5):
  for x in range(5):blocks[(y+3)*24+left+x]=first+y*5+x|(0x0400 if (x,y)==(2,4) else 0x3400)
# A small flower square replaces the old fenced rectangular bed.
for y in range(10,16):
 for x in range(4,11):blocks[y*24+x]=0x3296
for x,y in [(5,11),(7,11),(9,11),(5,13),(9,13)]:blocks[y*24+x]=0x3004
blocks[13*24+9]=0x3008 # preserve the town sign at its existing event coordinate
p.write_bytes(struct.pack('<480H',*blocks))
print('Installed 100 new art tiles, 25 metatiles, two houses and revised garden; doors preserved at x6/x15, y7.')
