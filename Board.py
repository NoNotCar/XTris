import Pieces
import Img
import random
import pygame
clear=Img.sndget("lineclear")
hit=Img.sndget("hit")
up=Img.sndget("levelup")
dark=Img.img2("Dark")
tfont=Img.fload("cool",64)
sfont=Img.fload("cool",32)
class SpawnSolidException(Exception):
    pass
class Board(object):
    lines=0
    level=0
    win=False
    lose=False
    def __init__(self, w, h, c, gm):
        self.w=w
        self.h=h
        self.b=[[None]*h for _ in range(w)]
        self.fp=None
        self.ft=32
        self.c=c
        self.state="NEW PIECE"
        self.pause=0
        self.gm=gm
        gm.generate(self)
    def update(self,events):
        if self.state=="FALLING":
            pressed=self.c.get_dir_pressed(events)
            buttons=self.c.get_buttons(events)
            if pressed[0]:
                dx=pressed[0]
                self.fpmove(dx,0)
            elif pressed[1]==1:
                self.fpmove(0,1)
            if buttons[0]:
                self.fp.rot(self)
            if buttons[1]:
                self.state="SLAMMING"
        if self.state=="NEW PIECE":
            try:
                self.fp=Pieces.Piece(self.gm.new_piece(),self)
                self.state="FALLING"
            except SpawnSolidException:
                self.lose=True
                return None
            self.ft=32-self.level*4 if 32-self.level*4>8 else 8
        if self.state=="FALLING":
            if self.ft:
                self.ft -= 1
            else:
                self.ft = 32-self.level*4 if 32-self.level*4>8 else 8
                self.fpmove(0, 1)
        elif self.state=="SLAMMING":
            if self.fpmove(0,1):
                self.fpmove(0, 1)
        elif self.pause:
            self.pause-=1
        else:
            if not self.gravity():
                if self.check_lines():
                    self.state="GRAVITY"
                    self.pause = 16
                else:
                    self.state="NEW PIECE"
            else:
                self.pause=16
    def render(self,screen):
        if not (self.win or self.lose):
            for x in range(self.w):
                for y in range(self.h):
                    b=self.get_block(x,y)
                    if b:
                        screen.blit(b.get_img(),(b.x*32,b.y*32+32))
            if self.fp:
                darkpos=[]
                for b in self.fp.bs:
                    y=b.y+1
                    while y<self.h:
                        if (b.x,y) not in darkpos and not self.get_block(b.x,y):
                            screen.blit(dark,(b.x*32,y*32+32))
                            darkpos.append((b.x,y))
                        else:
                            break
                        y+=1
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,0,self.w*32,32))
            if self.gm.levels:
                Img.bcentrex(sfont,"LEVEL "+str(self.level+1),screen,-8)
        else:
            screen.fill((0,0,0))
            Img.bcentre(tfont,"LOSE" if self.lose else "WIN",screen,col=(255,255,255))
    def get_block(self,x,y):
        try:
            return self.b[x][y]
        except IndexError:
            raise Exception("OUT OF BOARD: %s,%s"%(str(x),str(y)))
    def in_world(self,x,y):
        return 0<=x<self.w and 0<=y<self.h
    def spawn(self,b):
        if self.get_block(b.x,b.y):
            raise SpawnSolidException("SPAWNING BLOCK IN SOLID MATTER. NOT COMPENSATING. POS: %s,%s" % (str(b.x),str(b.y)))
        else:
            self.b[b.x][b.y]=b
    def dest(self,b):
        self.b[b.x][b.y]=None
    def exists(self,b):
        return self.get_block(b.x,b.y) is b
    def move_bs(self,bs,dx,dy):
        for b in bs:
            self.dest(b)
        for b in bs:
            b.x+=dx
            b.y+=dy
            self.spawn(b)
    def fpmove(self,dx,dy):
        if self.fp.can_move(self, dx, dy):
            self.move_bs(self.fp.bs, dx, dy)
            self.fp.x+=dx
            self.fp.y+=dy
            return True
        elif dy>0:
            for b in self.fp.bs:
                b.fix()
            self.fp = None
            if self.check_lines():
                self.state="GRAVITY"
                self.pause=16
            else:
                self.state="NEW PIECE"
    def check_lines(self):
        hooray=False
        for y in range(self.h):
            if all([self.get_block(x,y) for x in range(self.w)]):
                for x in range(self.w):
                    gb=self.get_block(x,y)
                    if gb.destructible:
                        self.dest(self.get_block(x,y))
                hooray=True
                if self.gm.levels:
                    self.lines+=1
        if hooray:
            if self.gm.has_won(self):
                self.win=True
            if self.lines<5:
                clear.play()
            else:
                self.lines=0
                self.level+=1
                up.play()
            self.re_fix()
            return True
        else:
            hit.play()
    def gravity(self):
        flist=[]
        fixlist=[]
        for x in range(self.w):
            for y in range(self.h):
                b=self.get_block(x,y)
                if b and b not in flist:
                    success,testlist=b.fall(self,flist,fixlist,[])
                    if success:
                        flist.extend(testlist)
                    else:
                        fixlist.extend(testlist)
        if flist:
            self.move_bs(flist,0,1)
            return True
    def re_fix(self):
        for x in range(self.w):
            for y in range(self.h):
                b=self.get_block(x,y)
                if b:
                    b.re_fix(self)