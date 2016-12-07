__author__ = 'NoNotCar'
import pygame
import os
from random import choice
import colorsys

np = os.path.normpath
loc = os.getcwd() + "/Assets/"
pygame.mixer.init()

def img(fil):
    return pygame.image.load(np(loc + fil + ".png")).convert_alpha()
def img2(fil):
    return imgn(fil,2)
def imgn(fil,n):
    return xn(img(fil),n)
def xn(img,n):
    return pygame.transform.scale(img,(int(img.get_width()*n),int(img.get_height()*n))).convert_alpha()
def imgsz(fil, sz):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), sz).convert_alpha()

def imgstrip2(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // h):
        imgs.append(pygame.transform.scale(img.subsurface(pygame.Rect(n * h, 0, h, h)), (h*2, h*2)).convert_alpha())
    return imgs
def imgstrip(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // h):
        imgs.append(img.subsurface(pygame.Rect(n * h, 0, h, h)).convert_alpha())
    return imgs
def imgstrip4f(fil,w):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // w):
        imgs.append(pygame.transform.scale(img.subsurface(pygame.Rect(n * w, 0, w, h)), (w*4, h*4)).convert_alpha())
    return imgs
def imgrot(i):
    imgs=[i]
    for n in range(3):
        imgs.append(pygame.transform.rotate(i,-90*n-90))
    return imgs


def musplay(fil,loops=-1):
    pygame.mixer.music.load(np(loc+ fil+".ogg"))
    pygame.mixer.music.play(loops)


def bcentre(font, text, surface, offset=0, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.centery = surface.get_rect().centery + offset
    return surface.blit(render, textrect)

def bcentrex(font, text, surface, y, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.top = y
    return surface.blit(render, textrect)
def bcentrerect(font, text, surface, rect, col=(0, 0, 0)):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = rect.centerx
    textrect.centery = rect.centery
    return surface.blit(render, textrect)
def cxblit(source, dest, y, xoff=0):
    srect=source.get_rect()
    drect=dest.get_rect()
    srect.centerx=drect.centerx+xoff
    srect.top=y
    return dest.blit(source,srect)
def sndget(fil):
    return pygame.mixer.Sound(np(loc+"Sound/"+fil+".wav"))

def hflip(img):
    return pygame.transform.flip(img,1,0)

def fload(fil,sz=16):
    return pygame.font.Font(np(loc+fil+".ttf"),sz)
buttimg=imgn("MenuButton",4)
def button(text,font):
    img=buttimg.copy()
    bcentre(font,text,img,-4)
    return img
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawTextRect(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
def colswap(img,sc,ec):
    px=pygame.PixelArray(img)
    px.replace(sc,ec)
def colcopy(img,sc,ec):
    i=img.copy()
    px=pygame.PixelArray(i)
    px.replace(sc,ec)
    return i
def darken(surface, value):
    "Value is 0 to 255. So 128 would be 50% darken"
    dark = pygame.Surface(surface.get_size(), 32)
    dark.set_alpha(value, pygame.RLEACCEL)
    surface.blit(dark, (0, 0))
def darkcopy(surface,value):
    nsurf=surface.copy()
    darken(nsurf,value)
    return nsurf
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


#blank64=img4("Trans")
dirs=["Game"]
music_mix={}
for d in dirs:
    emx=os.listdir(np(loc+"EMX/"+d))
    emx=[e[:-4] for e in emx if e[-4:]==".ogg"]
    if emx:
        music_mix[d]=["EMX/"+d+"/"+e for e in emx]
    else:
        mus = os.listdir(np(loc + "Music/" + d))
        mus = [m[:-4] for m in mus if m[-4:] == ".ogg"]
        music_mix[d] = ["Music/"+d+"/" + m for m in mus]
class DJ(object):
    def __init__(self):
        self.songs=music_mix["Game"]
        self.state="Menu"
    def switch(self,d):
        if self.state!=d:
            self.songs=music_mix[d]
            pygame.mixer.music.stop()
            musplay(choice(self.songs), 1)
            self.state=d
    def update(self):
        if not pygame.mixer.music.get_busy():
            musplay(choice(self.songs),1)
#dfont=fload("PressStart2P")