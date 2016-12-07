import pygame
import UniJoy
class Controller(object):
    icon=0
    def get_buttons(self,events):
        return 0,0
    def get_dirs(self):
        return [(0,0)]
    def get_pressed(self):
        return 0,0
    def get_dir_pressed(self, events):
        return 0,0

class Keyboard1(Controller):
    kconv = {pygame.K_w: (0, -1), pygame.K_s: (0, 1), pygame.K_a: (-1, 0), pygame.K_d: (1, 0)}
    def get_buttons(self,events):
        bomb=False
        act=False
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:
                    bomb=True
                elif e.key==pygame.K_LSHIFT:
                    act=True
        return bomb,act
    def get_pressed(self):
        keys = pygame.key.get_pressed()
        return (keys[pygame.K_SPACE],keys[pygame.K_LSHIFT])
    def get_dirs(self):
        keys = pygame.key.get_pressed()
        kpr=[]
        for k, v in self.kconv.iteritems():
            if keys[k]:
                kpr.append(v)
        return kpr
    def get_dir_pressed(self,events):
        for e in events:
            if e.type==pygame.KEYDOWN and e.key in self.kconv.keys():
                return self.kconv[e.key]
        return 0,0
class Keyboard2(Keyboard1):
    kconv={pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
    def get_buttons(self,events):
        bomb=False
        act=False
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN:
                    bomb=True
                elif e.key==pygame.K_RCTRL:
                    act=True
        return bomb,act
    def get_pressed(self):
        keys = pygame.key.get_pressed()
        return (keys[pygame.K_RETURN],keys[pygame.K_RCTRL])
class UniJoyController(Controller):
    icon=1
    def __init__(self,n):
        self.uj=UniJoy.Unijoy(n)
        self.ld=(0,0)
        self.cooldown=0
    def get_buttons(self,events):
        bomb=False
        act=False
        for e in events:
            if e.type==pygame.JOYBUTTONDOWN and e.joy==self.uj.jnum:
                if self.uj.get_b("A"):
                    bomb=True
                if self.uj.get_b("B"):
                    act=True
        return bomb,act
    def get_dirs(self):
        ds=self.uj.getdirstick(1)
        if ds!=(0,0):
            return [ds]
        return []
    def get_dir_pressed(self,events):
        if self.uj.binarystick:
            ds = self.uj.getdirstick(1)
            if ds!=self.ld:
                self.ld = ds
                return ds
        else:
            ds,mg = self.uj.getdirstickmag(1)
            if self.cooldown:
                self.cooldown-=1
            else:
                if ds!=(0,0):
                    self.cooldown=int((1.2-mg)*20)
                return ds
        return (0,0)
    def get_pressed(self):
        return (self.uj.get_b("A"),self.uj.get_b("B"))