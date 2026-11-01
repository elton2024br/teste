from PIL import Image
from pathlib import Path
import re,json
r=Path('/workspace/pokefirered');sheet=Image.open('/workspace/teste/assets/amazon/creatures/starter-sheet.png').convert('RGB');cw,ch=sheet.width//3,sheet.height//2
rows=[]
def transparent(c):return c[0]>180 and c[1]<95 and c[2]>150
def colors_from_pal(p):return [tuple(map(int,s.split())) for s in p.read_text().splitlines()[3:19]]
icon_pals=[colors_from_pal(r/f'graphics/pokemon/icon_palettes/icon_palette_{i}.pal') for i in range(3)]
for col,slot in enumerate(['squirtle','charmander','bulbasaur']):
 images=[sheet.crop((col*cw,row*ch,(col+1)*cw,(row+1)*ch)).resize((64,64),Image.Resampling.NEAREST) for row in range(2)]
 fg=[c for im in images for c in im.get_flattened_data() if not transparent(c)]
 strip=Image.new('RGB',(len(fg),1));strip.putdata(fg);q=strip.quantize(colors=15,method=Image.Quantize.MEDIANCUT);raw=q.getpalette()[:45];pal=[(0,0,0)]+[tuple((v>>3)<<3 for v in raw[i:i+3]) for i in range(0,45,3)]
 def indexed(im,colors):
  out=Image.new('P',im.size);out.putpalette([v for c in colors for v in c]+[0]*(768-3*len(colors)))
  out.putdata([0 if transparent(c) else min(range(1,len(colors)),key=lambda i:sum((a-b)**2 for a,b in zip(c,colors[i]))) for c in im.get_flattened_data()]);return out
 folder=r/f'graphics/pokemon/{slot}'
 for name,im in zip(['front','back'],images):indexed(im,pal).save(folder/(name+'.png'))
 text='JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in pal)+'\n'
 for name in ['normal','shiny']:(folder/(name+'.pal')).write_text(text)
 small=images[0].resize((32,32),Image.Resampling.NEAREST)
 def score(colors):return sum(min(sum((a-b)**2 for a,b in zip(c,d)) for d in colors[1:]) for c in small.get_flattened_data() if not transparent(c))
 ip=min(range(3),key=lambda i:score(icon_pals[i]));icon=Image.new('P',(32,64));icon.putpalette([v for c in icon_pals[ip] for v in c]+[0]*720)
 im=indexed(small,icon_pals[ip]);icon.paste(im,(0,0));icon.paste(im,(0,32));icon.save(folder/'icon.png')
 # Footprint is a compact monochrome identifier derived from the sprite silhouette.
 mono=Image.new('P',(16,16));mono.putpalette([255,255,255,0,0,0]+[0]*762);thumb=images[0].resize((16,16),Image.Resampling.NEAREST);mono.putdata([0 if transparent(c) else 1 for c in thumb.get_flattened_data()]);mono.save(folder/'footprint.png')
 rows.append({'slot':slot,'icon_palette':ip,'battle_palette_colors':len(pal),'front_back_size':[64,64],'shiny':'same art palette for current milestone'})
 p=r/'src/pokemon_icon.c';s=p.read_text();key=slot.upper();start=s.index('const u8 gMonIconPaletteIndices[]');a=s[:start];b=s[start:];b,n=re.subn(r'(\[SPECIES_'+key+r'\]\s*= )\d+',lambda m:m[1]+str(ip),b,count=1);assert n==1;p.write_text(a+b)
 for name in ['front_pic_coordinates.h','back_pic_coordinates.h']:
  p=r/'src/data/pokemon_graphics'/name;s=p.read_text();pattern=r'(\[SPECIES_'+key+r'\]\s*=\s*\{)(.*?)(\n    \},)'
  def adjust(m):
   b=re.sub(r'MON_COORDS_SIZE\(\d+, \d+\)','MON_COORDS_SIZE(64, 64)',m[2]);b=re.sub(r'\.y_offset = \d+','.y_offset = 0',b);return m[1]+b+m[3]
  s,n=re.subn(pattern,adjust,s,count=1,flags=re.S);assert n==1;p.write_text(s)
Path('/workspace/teste/assets/amazon/creatures/conversion.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Original front/back sprites, icons, palettes and coordinate bindings integrated for all three starters.')
