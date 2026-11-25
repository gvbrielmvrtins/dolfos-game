"""Build the game's 32 x 48 directional animation cells."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parent
COLORS = {
    'k':'#302a2b','h':'#43332e','b':'#785445','s':'#cd8d6a','f':'#ebb08a',
    'l':'#f5c39c','g':'#81898a','G':'#a6aca9','H':'#c3c8c1','d':'#585e60',
    'r':'#b33822','o':'#eb5527','O':'#fc7137','w':'#ffe8c1','n':'#332c39',
    't':'#b9aa91','T':'#dacbb2','S':'#554c44'
}

# Knit crown, folded brim, cropped hair, strong eyebrows and parted moustache.
CAP = [
    '.....ddddddd.....','...dgGGHHHGGgd...','..dgGGHHGGGGGgd..',
    '.dgGGGGGGGgGGGgd.','.dGGGGGGGgGGGGGgd','dggggGGGGGGgggggd',
    'ddggggggggggggddd','.dddddggggdddddd.'
]
FRONT = [
    '.khhhhsffffffhhk.','.khhsffffffffffk.','.ksffhhfflfhhffk.',
    '.ssfffkfflffkffs.','..sfffffflffffs..','...sfffssfsfffs..',
    '...sffhkkhkkhfs..','....shkkhfhkkhs..','....sffffsfffs...',
    '.....sffffffs....','......bssssb.....'
]
PROFILE = [
    '.khhhhhhhhfffff..','.khhhhhhsffffff..','.khhhssfssffhhf..',
    '.khhsfffsffffkf..','..khssfsffffflff.','...hbssffffffflls',
    '....bsfffffhhkkk.','....bsfffffhkkkf.','.....bsfffffffs..',
    '......sfffffss...','......bssssb.....'
]
BACK = [
    '.khhhhhhhhhhhhhk.','.khhhhhhbhhhhhh k.'.replace(' ',''),'.khhhbhhhhhhhhhk.',
    '.shhhhhhhhhhhhhs.','..shhhhhhhhhhhs..','...khhhhhhhhhk...',
    '....khhhhhhhk....','.....bbhhhbbs....','......ssssss.....',
    '......sffffs.....','......bssssb.....'
]
SHIRT = [
    '....rrr...rrr....','..rOOnrsrsrnOOr..','.rOOwwnrrrnwOOOr.',
    'rOwOnwnrorwwnOOr.','rOnwOnwrorwnnOOOr','rOwnwwOroOnwOOOOr',
    'rOOwwOOrOOOwnwwOr','rOnnOOOroOOnnwwOr','.rrrOwwroOwwnrrr.',
    '....OwnroOnwO....','....OwwroOOnO....','....rrrroorrr....'
]
def stamp(image, x, y, rows):
    for j,row in enumerate(rows):
        for i,key in enumerate(row):
            if key != '.':
                image.putpixel((x+i,y+j), tuple(bytes.fromhex(COLORS[key][1:]))+(255,))

def frame(direction, phase):
    image = Image.new('RGBA',(32,48))
    pen = ImageDraw.Draw(image)
    side = direction in ('left','right')
    bob = int(phase in (2,4))
    stride = [0,-1,0,1,0][phase]
    for index, hip in enumerate((13,16) if side else (10,17)):
        swing = (2*index-1)*stride
        toe = hip + (2*swing if side else 0)
        ankle = 43 - int(swing<0)
        pen.polygon([(hip,34+bob),(hip+4,34+bob),(toe+3,ankle),(toe,ankle)],COLORS['s'])
        pen.line([(hip+3,38+bob),(toe+2,ankle)],COLORS['f'],2)
        pen.rectangle([toe-1,ankle,toe+5,ankle+1],COLORS['S'])
        pen.line([(toe,ankle-1),(toe+2,ankle),(toe+4,ankle-1)],COLORS['k'])
        pen.polygon([(hip-1,31+bob),(hip+5,31+bob),(hip+5,37+bob),(hip-1,37+bob)],COLORS['t' if index==0 else 'T'])
    for x in ([13] if side else [8,21]):
        pen.rectangle([x,26+bob,x+2,33+bob],COLORS['s'])
        pen.rectangle([x+1,29+bob,x+3,32+bob],COLORS['f'])
    shirt=SHIRT if direction!='back' else [row.replace('roO','oOO').replace('rsrsr','rrrrr') for row in SHIRT]
    stamp(image,7,21+bob,shirt)
    stamp(image,7,10+bob,BACK if direction=='back' else PROFILE if side else FRONT)
    stamp(image,7,3+bob,CAP)
    return ImageOps.mirror(image) if direction=='left' else image

atlas=Image.new('RGBA',(160,192))
for row,direction in enumerate(('front','back','right','left')):
    for column in range(5):
        atlas.paste(frame(direction,column),(column*32,row*48))
atlas.save(ROOT/'assets/adventurer.png')
