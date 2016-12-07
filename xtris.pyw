import pygame, sys
pygame.init()
pygame.font.init()
screen=pygame.display.Info()
screen = pygame.display.set_mode((screen.current_w,screen.current_h),pygame.FULLSCREEN)
screen.convert()
clock=pygame.time.Clock()
import Board, Controllers, Img
from GameModes import gamemodes
tfont=Img.fload("cool",64)
sfont=Img.fload("cool",32)
startbuttons=[Img.button(gm.name,sfont) for gm in gamemodes]
cicons=[Img.imgn("Icons/"+i,8) for i in ["Keyboard","Gamepad"]]
music=True
del gm
cc=[]
if music:
    dj=Img.DJ()
nullrect=pygame.Rect(0,0,0,0)
levelbacks=((160,160,160),(160,160,0),(0,160,160),(160,0,160),(160,0,0),(0,160,0),(160,160,200))
srects=[nullrect]*len(startbuttons)
def dark(lvlb):
    return tuple([n-10 if n else 0 for n in lvlb])
def check_exit(event,no_exit=False):
    if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
        if no_exit:
            return True
        sys.exit()
while True:
    gamemode = None
    while not gamemode:
        for event in pygame.event.get():
            check_exit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                for n,sr in enumerate(srects):
                    if sr.collidepoint(mx,my):
                        gamemode=gamemodes[n]
                        break
        screen.fill((255, 0, 0))
        brects=[]
        Img.bcentre(tfont,"X-TRIS",screen,-100)
        for n,b in enumerate(startbuttons):
            srects[n]=Img.cxblit(b,screen,500+n*64)
        pygame.display.flip()
        clock.tick(60)
        if music:
            dj.update()
    done=False
    if not cc:
        pcs=[Controllers.Keyboard1(),Controllers.Keyboard2()]+[Controllers.UniJoyController(n) for n in range(pygame.joystick.get_count())]
        while not done:
            events=pygame.event.get()
            for event in events:
                check_exit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and cc:
                    done=True
            for p in pcs[:]:
                if p.get_buttons(events)[0]:
                    pcs.remove(p)
                    cc.append(p)
            screen.fill((200,200,200))
            Img.bcentre(tfont,"SELECT CONTROLLERS",screen)
            for n,c in enumerate(cc):
                Img.cxblit(cicons[c.icon],screen,screen.get_rect().h//2+64,n*128-len(cc)*64)
            pygame.display.flip()
            if music:
                dj.update()
    screen.fill((100,100,100))
    boards = []
    bw=gamemode.w
    bh=gamemode.h
    ps=len(cc)
    for n in range(len(cc)):
        board = pygame.Rect(0, 0, bw * 32, bh * 32 + 32)
        board.centerx = screen.get_rect().centerx - bw * 16 * (ps - 1) - 16 + n * (bw * 32 + 32)
        board.centery = screen.get_rect().centery
        boards.append(screen.subsurface(board))
    bs=[Board.Board(bw,bh,c,gamemode) for c in cc]
    while True:
        es=pygame.event.get()
        for e in es:
            check_exit(e)
        for n,b in enumerate(bs):
            if not b.lose:
                b.update(es)
                lvlb=levelbacks[b.level%len(levelbacks)]
                for x in range(bw):
                    pygame.draw.rect(boards[n],lvlb if x%2 else dark(lvlb),pygame.Rect(x*32,0,32,bh*32+32))
            b.render(boards[n])
        clock.tick(60)
        pygame.display.flip()
        if any([b.win for b in bs]) or len([b for b in bs if b.lose])>=(ps-1 if ps>1 else 1):
            break
        dj.update()
        if music:
            dj.update()
    pygame.time.wait(1000)
