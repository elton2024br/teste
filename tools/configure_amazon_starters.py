from pathlib import Path
import re
r=Path('/workspace/pokefirered')
mons=[('BULBASAUR','Bulbasaur','TATUPEDRA','GROUND',[60,60,75,25,30,60],'BATTLE_ARMOR',['TACKLE','MUD_SLAP'],'DEFENSE_CURL'),('CHARMANDER','Charmander','ARARAFOGO','FIRE',[45,55,40,70,65,35],'BLAZE',['PECK','EMBER'],'GROWL'),('SQUIRTLE','Squirtle','CAPIVÁGUA','WATER',[60,40,65,35,55,55],'TORRENT',['TACKLE','WATER_GUN'],'TAIL_WHIP')]
p=r/'src/data/text/species_names.h';s=p.read_text()
for key,_,name,*_ in mons:s=re.sub(r'(\[SPECIES_'+key+r'\]\s*= _\(")[^"]+',lambda m:m[1]+name,s)
p.write_text(s)
p=r/'src/data/pokemon/species_info.h';s=p.read_text()
for key,_,name,typ,stats,ability,moves,last in mons:
 pattern=r'(\[SPECIES_'+key+r'\]\s*=\s*\{)(.*?)(\n    \},)'
 def replace(m):
  b=m[2]
  for field,value in zip(['baseHP','baseAttack','baseDefense','baseSpeed','baseSpAttack','baseSpDefense'],stats):b=re.sub(r'(\.'+field+r' = )\d+',lambda n:n[1]+str(value),b)
  b=re.sub(r'\.types = \{[^}]+\}',f'.types = {{TYPE_{typ}, TYPE_{typ}}}',b)
  b=re.sub(r'\.abilities = \{[^}]+\}',f'.abilities = {{ABILITY_{ability}, ABILITY_NONE}}',b)
  b=re.sub(r'\.growthRate = \w+', '.growthRate = GROWTH_MEDIUM_FAST',b)
  return m[1]+b+m[3]
 s,n=re.subn(pattern,replace,s,count=1,flags=re.S);assert n==1,key
p.write_text(s)
p=r/'src/data/pokemon/level_up_learnsets.h';s=p.read_text()
for key,camel,_,typ,stats,ability,moves,last in mons:
 pattern=r'(static const u16 s'+camel+r'LevelUpLearnset\[\] = \{).*?\n\};'
 s,n=re.subn(pattern,lambda m:m[1]+'\n'+''.join(f'    LEVEL_UP_MOVE(1, MOVE_{move}),\n' for move in moves)+f'    LEVEL_UP_MOVE(8, MOVE_{last}),\n    LEVEL_UP_END\n}};',s,count=1,flags=re.S);assert n==1
p.write_text(s)
p=r/'src/data/pokemon/evolution.h';s=p.read_text()
for key,*_ in mons:s=re.sub(r'(\[SPECIES_'+key+r'\]\s*= )\{\{[^\n]+',lambda m:m[1]+'{{0}},',s,count=1)
p.write_text(s)
print('Names, types, stats, abilities, initial moves and disabled legacy evolutions updated for all three starters.')
