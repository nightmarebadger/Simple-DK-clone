# coding=utf-8

import pygame, sys
from pygame.locals import *
from colors import *

def terminate():
    pygame.quit()
    sys.exit()

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, marked = False, health = 1, sizew = 1, sizeh = 1):
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        self.marked = marked
        self.sizew = sizew
        self.sizeh = sizeh
        
        self.image = pygame.Surface((self.sizew*self.game.basesize, self.sizeh*self.game.basesize))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        self.tmpmarked = False
        
        self.health = health
        
        self.color()
        
        #print(self.rect.x, self.rect.y, self.rect.centerx, self.rect.centery)
        
    def update(self, time):
        pass
    
    def clicked(self):
        self.marked = not self.marked
        self.color()
    
    def color(self):
        if(self.marked):
            if(self.tmpmarked):
                self.image.fill(self.game.backgroundcolor)
                self.image.fill(OLIVE, rect=(1, 1, self.rect.width-2, self.rect.height-2))
            else:
                self.image.fill(self.game.backgroundcolor)
                self.image.fill(CAPRI, rect=(1, 1, self.rect.width-2, self.rect.height-2))
                #self.image.fill(CAPRI, rect=(5, 5, self.width-10, self.height-10))
        else:
            if(self.tmpmarked):
                self.image.fill(self.game.backgroundcolor)
                self.image.fill(AQUA, rect=(1, 1, self.rect.width-2, self.rect.height-2))
            else:
                self.image.fill(self.game.backgroundcolor)
                self.image.fill(CORAL, rect=(1, 1, self.rect.width-2, self.rect.height-2))
                #self.image.fill(CORAL, rect=(5, 5, self.width-10, self.height-10))
                
    def isHit(self, n):
        self.health -= n
        if(self.health < 0):
            self.die()
    
    def die(self):
        self.game.tileGroup.add(Tile(self.game, self.rect.centerx, self.rect.centery))
        self.kill()
    
class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, claimed = False, sizew = 1, sizeh = 1):
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        self.x = x
        self.claimed = claimed
        self.sizew = sizew
        self.sizeh = sizeh
        
        self.image = pygame.Surface((self.sizew*self.game.basesize, self.sizeh*self.game.basesize))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        self.color()
        
    def update(self, time):
        pass
    
    def color(self):
        if(self.claimed):
            self.image.fill(self.game.backgroundcolor)
            self.image.fill(RED, rect=(1, 1, self.rect.width-2, self.rect.height-2))
        else:
            self.image.fill(self.game.backgroundcolor)
            self.image.fill(WHITE, rect=(1, 1, self.rect.width-2, self.rect.height-2))

class Imp(pygame.sprite.Sprite):
    def __init__(self, game, x, y, movespeed, strength, hitspeed, sizew = 0.5, sizeh = 0.5):
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        self.x = x
        self.y = y
        self.movespeed = movespeed
        self.strength = strength
        self.hitspeed = hitspeed
        self.carryload = strength * 10
        
        self.vx = 0
        self.vy = 0
        
        self.sizew = sizew
        self.sizeh = sizeh
        
        self.movex = self.movey = 0
        
        self.image = pygame.Surface((self.sizew*self.game.basesize, self.sizeh*self.game.basesize), SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        #self.image.fill(BLACK)
        pygame.draw.circle(self.image, BLACK, (self.rect.width//2, self.rect.height//2), self.rect.width//2)
        pygame.draw.circle(self.image, YELLOW, (self.rect.width//2, self.rect.height//2), self.rect.width//2-1)
        
        #self.move(10,10)
        #pygame.draw.circl
        
        
    
    def update(self, time):
        self.calculatemove()
        self.move(self.vx*time*self.movespeed*self.game.basesize, self.vy*time*self.movespeed*self.game.basesize)
        if(self.goingTo):
            if(self.goingTo.rect.collidepoint(self.rect.center)):
                self.goingTo.isHit(self.strength)
            
    
    def calculatemove(self):
        #Find the position of a clicked area you can get to
        #Foo is the pos of the chosen marked wall
        #Bar is the pos of all walls that touch the tiles
        self.goingTo = None
        
        bar = []
        for tile in self.game.tileGroup:
            #print(tile.rect.centerx, tile.rect.centery)
            tmp1 = tile.rect.centerx + self.game.basesize*tile.sizew
            tmp2 = tile.rect.centery
            if((tmp1, tmp2) not in bar):
                if(tmp1 <= self.game.windowwidth and tmp2 <= self.game.windowheight):
                    bar.append((tmp1, tmp2))
            tmp1 = tile.rect.centerx - self.game.basesize*tile.sizew
            tmp2 = tile.rect.centery
            if((tmp1, tmp2) not in bar):
                if(tmp1 <= self.game.windowwidth and tmp2 <= self.game.windowheight):
                    bar.append((tmp1, tmp2))
            tmp1 = tile.rect.centerx
            tmp2 = tile.rect.centery - self.game.basesize*tile.sizeh
            if((tmp1, tmp2) not in bar):
                if(tmp1 <= self.game.windowwidth and tmp2 <= self.game.windowheight):
                    bar.append((tmp1, tmp2))
            tmp1 = tile.rect.centerx
            tmp2 = tile.rect.centery + self.game.basesize*tile.sizeh
            if((tmp1, tmp2) not in bar):
                if(tmp1 <= self.game.windowwidth and tmp2 <= self.game.windowheight):
                    bar.append((tmp1, tmp2))
        #print(bar)
        flag = False
        for wall in self.game.wallGroup:
            if(flag):
                break
            if(wall.marked):
                for (i,j) in bar:
                    if(wall.rect.collidepoint(i,j)):
                        self.goingTo = wall
                        flag = True
                        break
                
        """
        for wall in self.game.wallGroup:
            if(wall.marked):
                foo = wall.rect.center
                break
        """
        #Calculate movement vector
        if(self.goingTo):
            #print(foo, self.rect.x, self.rect.y)
            try:
                dx = self.goingTo.rect.centerx - self.rect.centerx
                dy = self.goingTo.rect.centery- self.rect.centery
                #print(dx, dy)
                self.vx = dx/(dx**2 + dy**2)**(1/2)
                self.vy = dy/(dx**2 + dy**2)**(1/2)
                #print(self.vx, self.vy)
            except:
                self.vx = self.vy = 0
        else:
            self.vx = self.vy = 0
        
    def move(self, dx, dy):
        if(dx != 0 or dy != 0):
            self.movex += dx
            self.movey += dy
            #print("moving...")
            self.rect.x = self.rect.x + int(self.movex)
            self.rect.y = self.rect.y + int(self.movey)
            self.movex = self.movex - int(self.movex)
            self.movey = self.movey - int(self.movey)
    
        
        
        
class Game:
    def __init__(self, windowwidth, windowheight, fps=120):
        
        self.windowwidth = windowwidth
        self.windowheight = windowheight
        self.fps = fps
        
        self.backgroundcolor = BLACK
        self.background = pygame.Surface((self.windowwidth, self.windowheight))
        self.background.fill(self.backgroundcolor)
        
        self.caption = "Simple DK-like game"
        
        self.selection_rect = None
        self.selection_first_pos = None
        
        self.basesize = 80
        
        self.lattice = [["wall" for i in range(self.windowwidth//self.basesize)] for j in range(self.windowheight//self.basesize)]
        #print(self.lattice)
        
    def setup(self):
        pygame.init()
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((self.windowwidth, self.windowheight), SRCALPHA, 32)
        
        #Sprite groups
        self.wallGroup = pygame.sprite.RenderPlain()
        self.tileGroup = pygame.sprite.RenderPlain()
        self.impGroup = pygame.sprite.RenderPlain()
        
        for i in range(self.basesize//2, self.windowheight, self.basesize):
            for j in range(self.basesize//2, self.windowwidth, self.basesize):
                if(i == j == 800 - self.basesize//2):
                    self.tileGroup.add(Tile(self, i, j, False))
                    self.impGroup.add(Imp(self, i, j, 1, 1, 1))
                    self.lattice[-1][-1] = "tile"
                    #print(self.lattice)
                else:
                    self.wallGroup.add(Wall(self, i, j, False))
                    

        
    def gameloop(self):
        self.continue_playing = True
        self.clock.tick()
        while(self.continue_playing):
            time = self.clock.tick(self.fps)
            #print(self.clock.get_fps())
            
            #Key handler
            for event in pygame.event.get():
                if(event.type == QUIT):
                    terminate()
                elif(event.type == KEYDOWN):
                    if(event.key == K_ESCAPE):
                        terminate()
                elif(event.type == MOUSEBUTTONDOWN):
                    """
                        1: levi
                        2: srednji
                        3: desni
                        4: kolešček gor
                        5: kolešček dol
                        8: stranski
                    
                    """
                    if(event.button == 1):
                        for wall in self.wallGroup:
                            if(wall.rect.collidepoint(event.pos)):
                                wall.clicked()
                    elif(event.button == 3):
                        self.selection_first_pos = event.pos
                elif(event.type == MOUSEBUTTONUP):
                    if(event.button == 3):
                        self.selection_rect = pygame.Rect(self.selection_first_pos, (-(self.selection_first_pos[0]-event.pos[0]), -(self.selection_first_pos[1]-event.pos[1])))
                        self.selection_rect.normalize()
                        for wall in self.wallGroup:
                            if(self.selection_rect.colliderect(wall.rect)):
                                wall.tmpmarked = False
                                wall.clicked()    
                elif(event.type == MOUSEMOTION):
                    if(pygame.mouse.get_pressed()[2]):
                        self.selection_rect = pygame.Rect(self.selection_first_pos, (-(self.selection_first_pos[0]-event.pos[0]), -(self.selection_first_pos[1]-event.pos[1])))
                        self.selection_rect.normalize()
                        for wall in self.wallGroup:
                            if(self.selection_rect.colliderect(wall.rect)):
                                wall.tmpmarked=True
                                wall.color()
                            else:
                                wall.tmpmarked=False
                                wall.color()
            
            #Update groups
            self.wallGroup.update(time/1000)
            self.tileGroup.update(time/1000)
            self.impGroup.update(time/1000)
            
            #Drawing
            self.surface.blit(self.background, (0,0))
            self.wallGroup.draw(self.surface)
            self.tileGroup.draw(self.surface)
            self.impGroup.draw(self.surface)
            
            pygame.display.update()
            
if( __name__ == "__main__") :
    game = Game(800, 800, 120)
    game.setup()
    game.gameloop()