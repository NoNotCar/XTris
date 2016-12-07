import Pieces
from random import randint,choice
numbers=Pieces.load_ps("numbers")
def standardgen():
    x = randint(0, 27)
    return choice(Pieces.ominos[int(x ** 0.5)])
class GameMode(object):
    name="GM"
    levels=True
    w=11
    h=25
    def new_piece(self):
        return None
    def has_won(self,world):
        return world.level==9
    def generate(self,world):
        pass
class Standard(GameMode):
    name="Standard"
    def new_piece(self):
        return standardgen()
class Tetris(GameMode):
    name="Tetris"
    def new_piece(self):
        return choice(Pieces.tetrominos)
class Pentris(GameMode):
    name="Pentris"
    def new_piece(self):
        return choice(Pieces.pentominos)
class Hextris(GameMode):
    name = "Hextris"
    w=13
    h=27
    def new_piece(self):
        return choice(Pieces.hexominoes)
class Numberpile(Standard):
    name = "NumberPile"
    w=15
    def new_piece(self):
        return Standard.new_piece(self) if randint(0,9) else choice(numbers)
class Mega(Standard):
    name="MEGA"
    w=18
    h=30
    def new_piece(self):
        return choice(Pieces.tetrominos) if randint(0,2) else choice(Pieces.megtets)
class ClearSkies(Standard):
    name="Clear Skies"
    levels = False
    h=30
    def has_won(self,world):
        for x in xrange(world.w):
            for y in xrange(world.h):
                gb=world.get_block(x,y)
                if gb and gb.name=="Cloud":
                    return False
        return True
    def generate(self,world):
        for y in xrange(world.h):
            gspace=False
            for x in xrange(world.w):
                if (y>15 and randint(0,5)) and not (not gspace and x==world.w-1):
                    world.spawn(Pieces.CloudBlock(x,y))
                else:
                    gspace=True
class Chimney(Standard):
    name="Chimney"
    h=30
    w=7
class Bowl(Standard):
    name="Bowl"
    shape={2:1,1:3}
    def generate(self,world):
        for x in xrange(world.w):
            for y in xrange(world.h):
                if world.h-y in self.shape.keys():
                    s=self.shape[world.h-y]
                    if x<s or world.w-x<=s:
                        world.spawn(Pieces.IndestBlock(x, y))
gamemodes=[Standard(),Tetris(),Pentris(),Hextris(),ClearSkies(),Chimney(),Bowl(),Mega(),Numberpile()]