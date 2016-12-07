import pygame, sys, pickle
size=4
boundary = (size * 2 + 1) * 32
pygame.init()
screen = pygame.display.set_mode((320,320))
clock=pygame.time.Clock()
import Img
from Pieces import mirror
bimg=Img.img2("Indest")
cimg=Img.img2("Centre")
icons=[Img.img2("Icons/"+i) for i in ["Add","AddMirror","Save","Grid","Trash","Back"]]
icons.append(Img.hflip(icons[-1]))
pieceset=[[]]
centregrid=False
def check_exit(event,no_exit=False):
    if (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE) or event.type==pygame.QUIT:
        if no_exit:
            return True
        sys.exit()
while True:
    for event in pygame.event.get():
        check_exit(event)
        if event.type==pygame.MOUSEBUTTONDOWN:
            mx,my=pygame.mouse.get_pos()
            if mx< boundary and my< boundary:
                if centregrid:
                    if 16<=mx<boundary-16 and 16<=my<boundary-16:
                        mx, my = [((n-16) // 16 - size*2)//2 * 2+1 for n in (mx, my)]
                    else:
                        continue
                else:
                    mx,my=[(n//32-size)*2 for n in (mx,my)]
                if event.button==1:
                    if (mx,my) not in pieceset[-1]:
                        pieceset[-1].append((mx,my))
                elif event.button==3:
                    if (mx, my) in pieceset[-1]:
                        pieceset[-1].remove((mx,my))
            elif boundary <my and mx<len(icons)*32:
                n=mx//32
                if n in [5,6]:
                    if len(pieceset)>1:
                        if n==5:
                            if not pieceset[-1]:
                                del pieceset[-1]
                            else:
                                pieceset.insert(0,pieceset.pop())
                        else:
                            if not pieceset[-1]:
                                del pieceset[-1]
                            pieceset.append(pieceset.pop(0))
                elif n==4:
                    if len(pieceset)>1:
                        del pieceset[-1]
                        centregrid=pieceset[-1][0][0]%2
                elif n==3:
                    pieceset[-1]=[]
                    centregrid=not centregrid
                elif n==2:
                    with open(Img.np(Img.loc+"Piecesets/sav.ps"),"wb") as sav:
                        pickle.dump(pieceset,sav)
                        sys.exit()
                elif n==1:
                    if pieceset[-1]:
                        pieceset.append(mirror(pieceset[-1])[1])
                        pieceset.append([])
                else:
                    if pieceset[-1]:
                        pieceset.append([])
    screen.fill((100,100,100))
    for x,y in pieceset[-1]:
        screen.blit(bimg,(x*16+size*32,y*16+size*32))
    for n,i in enumerate(icons):
        screen.blit(i, (n * 32, boundary))
    screen.blit(cimg,(size*32,size*32))
    pygame.display.flip()
    clock.tick(60)