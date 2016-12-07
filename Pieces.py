import Img
from random import choice, randint
import pickle
norot=Img.sndget("norot")
class XOmino(object):
    def __init__(self,bpos):
        if bpos[0][0]%2:
            self.centergrid=True
        self.bpos=bpos
        self.w=max([b[0] for b in bpos])-min([b[0] for b in bpos])//2+1
        self.h=max([b[1] for b in bpos])-min([b[1] for b in bpos])//2+1
        self.x=-min([b[0] for b in bpos])
        self.y=-min([b[1] for b in bpos])
def mirror(bpos):
    return [bpos,[(-bx,by) for bx,by in bpos]]
def megaomino(bpos):
    nbpos=[]
    for bx,by in bpos:
        cx,cy=bx*2,by*2
        for dx,dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
            nbpos.append((cx+dx,cy+dy))
    return nbpos
def load_ps(savfile):
    with open(Img.np(Img.loc+"Piecesets/"+savfile+".ps"),"rb") as sav:
        return [XOmino(bpos) for bpos in pickle.load(sav)]

monomino=[XOmino([(0,0)])]
domino=[XOmino([(-1,-1),(-1,1)])]
triominos=[XOmino([(-1,-1),(-1,1),(1,1)]),XOmino([(0,-2),(0,0),(0,2)])]
tetrominos=[[(-3,-1),(-1,-1),(1,-1),(3,-1)],
            [(-1,-1),(1,-1),(-1,1),(1,1)],
            [(-2,0),(0,0),(2,0),(0,2)],
            [(0,-2),(0,0),(-2,0),(-2,2)],[(0, -2), (0, 0), (2, 0), (2, 2)],
            [(0, -2), (0, 0), (0, 2), (2, 2)],[(0, -2), (0, 0), (0, 2), (-2, 2)]]
megtets=[[(-3,0),(-1,0),(1,0),(3,0)],
            [(-1,-1),(1,-1),(-1,1),(1,1)],
            [(-2,0),(0,0),(2,0),(0,-2)],
            [(-1,-2),(-1,0),(1,0),(1,2)],[(1, -2), (1, 0), (-1, 0), (-1, 2)],
            [(0, -2), (0, 0), (0, 2), (2, 2)],[(0, -2), (0, 0), (0, 2), (-2, 2)]]
megtets=[megaomino(m) for m in megtets]
pentominos=[[(0,-4),(0,-2),(0,0),(0,2),(0,4)],
            [(0,0),(0,-2),(-2,-2),(2,-2),(0,2)],
            [(0,2),(2,0),(-2,0),(2,2),(-2,2)],
            [(-2,0),(0,2),(-2,-2),(-2,2),(2,2)],
            [(0,0),(-2,0),(-2,-2),(0,2),(2,2)],
            [(0,0),(2,0),(-2,0),(0,2),(0,-2)]]\
           +mirror([(0, 0), (-2, 0), (0, -2), (0, 2),(2,-2)])\
           +mirror([(-1,-3),(-1,-1),(-1,1),(-1,3),(1,3)])\
           +mirror([(-1,-3),(-1,-1),(-1,1),(-1,3),(1,1)])\
           +mirror([(-1, -3), (-1, -1), (-1, 1), (1, 1), (1, 3)])\
           +mirror([(0,0),(2,0),(0,2),(0,-2),(2,-2)])\
           +mirror([(0,0),(0,2),(0,-2),(2,-2),(-2,2)])
hexominoes=load_ps("hex")
for o in [tetrominos,pentominos,megtets]:
    for n,t in enumerate(o):
        o[n]=XOmino(t)
ominos=[monomino,domino,triominos,tetrominos,pentominos,hexominoes]
bcols=[]
for r in range(3):
    for g in range(3):
        for b in range(3):
            if r!=g or g!=b or b!=r:
                bcols.append((r,g,b))
def cswap(t,e):
    return tuple([e if t[n]==2 else e//2 if t[n] else t[n] for n in range(len(t))])
bimgs=[]
for bc in bcols:
    bimg=Img.img2("Block2")
    Img.colswap(bimg,(255,255,255),cswap(bc,255))
    Img.colswap(bimg, (192, 192, 192), cswap(bc, 192))
    Img.colswap(bimg, (160, 160, 160), cswap(bc, 160))
    bimgs.append(bimg)
class Block(object):
    img=None
    fixed=False
    name="Block"
    destructible=True
    def __init__(self,x,y,p,img):
        self.x=x
        self.y=y
        self.p=p
        self.img=img
    def can_move(self,world,dx,dy):
        tx=self.x+dx
        ty=self.y+dy
        if 0<=tx<world.w and 0<=ty<world.h:
            b=world.get_block(tx,ty)
            if self.fixed:
                return not (b and b not in self.fb)
            else:
                return not (b and b not in self.p.bs)
    def get_img(self):
        return self.img
    def fix(self):
        self.fb=[]
        for b in self.p.bs:
            if abs(b.x-self.x)+abs(b.y-self.y)==1:
                self.fb.append(b)
        del self.p
    def get_fp(self,fp):
        fp.append(self)
        for b in self.fb:
            if b not in fp:
                b.get_fp(fp)
        return fp
    def fall(self,world,flist,fixlist,testedlist,fbtest=None):
        if self in fixlist:
            return False,[]
        if self in flist:
            return True,[]
        if self in testedlist:
            return True, []
        else:
            testedlist.append(self)
        if not fbtest:
            fbtest=self.get_fp([])
        else:
            fbtest=[]
        if self.y<world.h-1:
            b = world.get_block(self.x, self.y+1)
            if b and b not in self.fb:
                success,testlist=b.fall(world,flist,fixlist,testedlist)
                if not success:
                    fixlist.extend(testlist)
                    return False,fbtest
                else:
                    flist.extend(testlist)
            if fbtest:
                for b in fbtest:
                    success,testlist=b.fall(world,flist,fixlist,testedlist,fbtest)
                    if not success:
                        return False,fbtest
        else:
            return False,fbtest
        return True,fbtest
    def re_fix(self,world):
        for b in self.fb[:]:
            if not world.exists(b):
                self.fb.remove(b)
class CloudBlock(Block):
    imgs=Img.imgstrip2("Cloud")
    name="Cloud"
    def __init__(self,x,y):
        self.fixed=True
        self.x=x
        self.y=y
        self.fb=[]
        self.i=randint(0,3)
    def fall(self,world,flist,fixlist,testedlist,fbtest=None):
        return False,[]
    def get_img(self):
        return self.imgs[self.i]
class IndestBlock(Block):
    img=Img.img2("Indest")
    name="Indest"
    destructible = False
    def __init__(self,x,y):
        self.fixed=True
        self.x=x
        self.y=y
        self.fb=[]
    def fall(self,world,flist,fixlist,testedlist,fbtest=None):
        return False,[]
class Piece(object):
    def __init__(self,xo,world):
        self.xo=xo
        self.bpos=xo.bpos[:]
        xoff=(world.w-xo.w)//2
        self.x=xoff
        self.y=0
        self.bimg=choice(bimgs)
        self.spawn(world)
    def can_move(self,world,dx,dy):
        return all([b.can_move(world,dx,dy) for b in self.bs])
    def spawn(self,world):
        self.bs=[]
        for bx,by in self.bpos:
            self.bs.append(Block(self.x+(self.xo.x+bx)//2,self.y+(self.xo.y+by)//2,self,self.bimg))
        for b in self.bs:
            world.spawn(b)
    def can_spawn(self,world,bpos):
        for bx,by in bpos:
            tx,ty=self.x+(self.xo.x+bx)//2,self.y+(self.xo.y+by)//2
            if not world.in_world(tx,ty) or world.get_block(tx,ty):
                return False
        return True
    def rot(self,world):
        for b in self.bs:
            world.dest(b)
        nbpos=[]
        for bx, by in self.bpos:
            nbpos.append((-by,bx))
        if self.can_spawn(world,nbpos):
            self.bpos=nbpos
            self.spawn(world)
        else:
            self.spawn(world)
            norot.play()

