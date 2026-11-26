"""Draw the central library hall at its native pixel resolution."""
from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
rng = random.Random(42)
im = Image.new('RGB',(640,400),'#202826')
d = ImageDraw.Draw(im)
ink='#302c28'; walnut='#5c4132'; wood='#865e43'; honey='#bc9561'
brass='#d2aa69'; gold='#edce88'; plaster='#bfad87'; pale='#e3d1a5'
def box(coords,c): d.rectangle(coords,fill=c)
def poly(points,c): d.polygon(points,fill=c)
def line(points,c,w=1): d.line(points,fill=c,width=w)
def diamond(x,y,w,h,c): poly([(x-w,y),(x,y-h),(x+w,y),(x,y+h)],c)
def beam(x,y,w,h):
    box((x,y,x+w,y+h),ink);box((x+1,y+1,x+w-1,y+h-1),walnut)
    line([(x+2,y+1),(x+w-1,y+1)],honey)
def shelf(x):
    beam(x,47,53,65);box((x+4,51,x+49,108),'#302d29')
    colors=['#98634a','#838c74','#b3996a','#6e7c76','#ad8161','#746353']
    for base in [67,85,103]:
        left=x+5
        while left<x+46:
            w=rng.randrange(2,6);h=rng.randrange(7,15)
            box((left,base-h,left+w-1,base),rng.choice(colors))
            if w>2: line([(left,base-h+2),(left+w-2,base-h+2)],'#c8b384')
            left+=w+1
        beam(x+2,base+1,49,3)
def lamp(x,y):
    box((x-3,y+3,x+3,y+17),walnut)
    box((x-1,y+3,x+1,y+15),brass)
    poly([(x-7,y),(x-4,y-7),(x+4,y-7),(x+7,y),(x+4,y+5),(x-4,y+5)],ink)
    poly([(x-5,y),(x-3,y-5),(x+3,y-5),(x+5,y),(x+3,y+3),(x-3,y+3)],'#e4ac61')
    box((x-2,y-4,x+1,y+2),'#ffe7a3')
    line([(x-6,y+1),(x+6,y+1)],honey)
def arch(x,base,w,h,color):
    left=x-w//2;top=base-h
    poly([(left,base),(left,top+9),(left+4,top+4),(left+10,top),(left+w-10,top),(left+w-4,top+4),(left+w,top+9),(left+w,base)],color)
def emblem(x,y,kind):
    if kind=='archive':
        for off in [-3,2]:
            box((x-5,y+off,x+5,y+off+3),brass);box((x-1,y+off,x+1,y+off+1),walnut)
    elif kind in ('book','journal'):
        box((x-5,y-4,x+5,y+3),gold);line([(x,y-4),(x,y+4)],walnut)
        if kind=='journal':line([(x+3,y-4),(x+3,y+2)],'#ae5841')
    elif kind=='board':
        box((x-5,y-4,x+5,y+2),brass);line([(x-3,y-2),(x+1,y-2)],walnut);line([(x,y+3),(x,y+5)],gold)
    else:
        line([(x-5,y),(x-4,y-3),(x+3,y-3),(x+5,y)],gold,2)
        box((x-3,y+1,x+3,y+4),brass)
font=ImageFont.load_default(size=11)
def plaque(x,y,label):
    w=int(d.textlength(label,font=font))+14
    box((x-w//2-1,y-1,x+w//2+1,y+12),ink)
    box((x-w//2,y,x+w//2,y+11),'#4a4738')
    line([(x-w//2+1,y),(x+w//2-1,y)],brass)
    d.text((x,y+6),label,font=font,anchor='mm',fill='#fff0c5',stroke_width=0)
def door(x,base,width,height,kind,label):
    arch(x,base,width+8,height+4,ink);arch(x,base,width+4,height+2,honey)
    arch(x,base,width,height,walnut);arch(x,base-2,width-8,height-6,'#74604b')
    for offset in range(-width//2+8,width//2-4,6):
        line([(x+offset,base-height+14),(x+offset,base-4)],'#604c3d')
    beam(x-width//2+4,base-13,width-8,3)
    box((x-8,base-height//2-6,x+8,base-height//2+6),'#453d32')
    emblem(x,base-height//2,kind);box((x+width//2-7,base-18,x+width//2-5,base-15),gold)
    box((x-width//2-5,base,x+width//2+5,base+2),'#c4ab83')
    plaque(x,base-height-18,label)

# Stone floor in a brick bond, clipped to the cutaway's converging sides.
floor=Image.new('RGB',im.size,'#96836b');f=ImageDraw.Draw(floor)
for row,y in enumerate(range(112,365,15)):
    for x in range(-30+(row%2)*22,640,44):
        shade=rng.choice(['#b9a78a','#bfae91','#c4b296','#b6a387','#bfaa8c'])
        f.rectangle((x+1,y+1,x+43,y+14),fill=shade)
        f.line((x+2,y+1,x+40,y+1),fill='#d0bea0')
        for _ in range(4):
            px=x+rng.randint(3,40);py=y+rng.randint(3,12)
            f.point((px,py),fill='#a99579')
mask=Image.new('1',im.size);ImageDraw.Draw(mask).polygon([(117,112),(523,112),(598,359),(42,359)],fill=1)
im.paste(floor,mask=mask)
# Symmetric wood-lined wings with stepped door bays.
for flip in [False,True]:
    def wing(points,c): poly([(640-x if flip else x,y) for x,y in points],c)
    wing([(94,25),(123,35),(123,115),(50,359),(22,364),(22,274)],ink)
    wing([(97,30),(119,37),(119,114),(47,354),(28,356),(28,276)],wood)
    wing([(96,34),(115,40),(115,100),(44,341),(31,344),(31,277)],plaster)
    for v in range(5):
        y=112+v*45;x=112-v*13
        wing([(x,y),(x+3,y),(x-11,y+45),(x-14,y+45)],'#8e765a')
    wing([(97,30),(119,35),(47,281),(26,278)],'#7d634b')
    wing([(97,27),(119,32),(47,275),(28,273)],'#c9af83')
box((95,25,545,116),ink);box((101,31,539,105),plaster)
for x in range(104,536,8):
    for y in range(40,95,9):
        d.point((x+rng.randrange(4),y+rng.randrange(3)),fill='#ae9b78')
for y,h,c in [(25,3,walnut),(28,2,honey),(31,4,wood),(36,2,pale),(96,15,walnut),(109,3,honey),(113,3,ink)]:
    box((98,y,542,y+h-1),c)
for x in [107,215,425,533]:beam(x,36,5,78)
shelf(143);shelf(444)
lamp(235,69);lamp(405,69)
door(320,115,52,61,'archive','CASE STUDIES')
# Runner has doubled selvedges, a repeated central rosette and a fringed end.
poly([(290,119),(350,119),(364,359),(276,359)],'#87735d')
for delta,color in [(0,'#563f35'),(2,'#b89a6d'),(4,'#904733'),(7,'#d4ad76'),(9,'#a45339')]:
    poly([(291+delta,119),(349-delta,119),(362-delta,356),(278+delta,356)],color)
for y in range(130,352,18):
    diamond(320,y,9,5,'#d7af76');diamond(320,y,5,3,'#724331')
    for sign in [-1,1]:diamond(320+sign*15,y,2,1,'#d7af76')
for x in range(280,362,3):line([(x,357),(x,360+rng.randrange(2))],'#cdb68a')
for x,y,kind,name in [(114,182,'book','PROJECTS'),(76,305,'board','SERVICES'),(526,182,'journal','ABOUT ME'),(564,305,'phone','CONTACT')]:
    # Deep lintel and recessed vestibule at each side-wall turn.
    box((x-33,y-74,x+33,y+2),ink);box((x-31,y-72,x+31,y),wood)
    box((x-28,y-69,x+28,y-2),'#baa581')
    beam(x-34,y-76,68,5)
    door(x,y,34,47,kind,name)
# Front wall is cut at the entrance to reveal the player.
for left,right in [(22,265),(375,618)]:
    box((left,359,right,369),ink);box((left+2,359,right-2,361),honey)
    box((left+2,362,right-2,366),walnut)
for x in [23,256,376,608]:
    beam(x,352,9,17);box((x-1,352,x+10,354),honey)
im.save(ROOT/'assets/hall.png',optimize=True)
