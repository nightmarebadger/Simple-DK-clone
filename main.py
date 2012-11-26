# coding=utf-8

import pygame, sys
from pygame.locals import *

def terminate():
    pygame.quit()
    sys.exit()

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, marked = False):
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.marked = marked
        
        self.image = pygame.Surface((width, height))
        
        self.tmpmarked = False
        self.color()
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def update(self, time):
        #self.tmpmarked = False
        pass
    
    def clicked(self):
        self.marked = not self.marked
        self.color()
    
    def color(self):
        if(self.marked):
            if(self.tmpmarked):
                self.image.fill((0,0,0))
                self.image.fill((100,50,50), rect=(1, 1, self.width-2, self.height-2))
            else:
                self.image.fill((0,0,0))
                self.image.fill((0,0,180), rect=(1, 1, self.width-2, self.height-2))
        else:
            if(self.tmpmarked):
                self.image.fill((0,0,0))
                self.image.fill((50, 50, 10), rect=(1, 1, self.width-2, self.height-2))
            else:
                self.image.fill((0,0,0))
                self.image.fill((175, 50, 50), rect=(1, 1, self.width-2, self.height-2))
        
class Game:
    def __init__(self, windowwidth, windowheight, fps=120):
        
        self.windowwidth = windowwidth
        self.windowheight = windowheight
        self.fps = fps
        self.background = pygame.Surface((self.windowwidth, self.windowheight))
        self.background.fill((0,0,0))
        
        self.caption = "Simple DK-like game"
        
        self.selection_rect = None
        self.selection_first_pos = None
        
    def setup(self):
        pygame.init()
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((self.windowwidth, self.windowheight), SRCALPHA)
        
        #Sprite groups
        self.tileGroup = pygame.sprite.RenderPlain()
        for i in range(20, 800, 40):
            for j in range(20, 800, 40):
                self.tileGroup.add(Tile(self, i, j, 40, 40, False))
        
    def gameloop(self):
        self.continue_playing = True
        self.clock.tick()
        while(self.continue_playing):
            time = self.clock.tick(self.fps)
            
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
                        print("Klik levi")
                        for tile in self.tileGroup:
                            if(tile.rect.collidepoint(event.pos)):
                                tile.clicked()
                    elif(event.button == 3):
                        self.selection_first_pos = event.pos
                elif(event.type == MOUSEBUTTONUP):
                    if(event.button == 3):
                        #print(self.selection_first_pos, event.pos)
                        self.selection_rect = pygame.Rect(self.selection_first_pos, (-(self.selection_first_pos[0]-event.pos[0]), -(self.selection_first_pos[1]-event.pos[1])))
                        #print(self.selection_rect.topleft, self.selection_rect.width, self.selection_rect.height)
                        self.selection_rect.normalize()
                        for tile in self.tileGroup:
                            if(self.selection_rect.colliderect(tile.rect)):
                                tile.tmpmarked = False
                                tile.clicked()
                                
                        #self.tmpRectGroup.add(self.selection_rect)   
                        #pygame.draw.rect(self.surface, (0,0,0), self.selection_rect)
                        #pygame.display.update()
                        #x = input("Pocakaj")     
                elif(event.type == MOUSEMOTION):
                    if(pygame.mouse.get_pressed()[2]):
                        self.selection_rect = pygame.Rect(self.selection_first_pos, (-(self.selection_first_pos[0]-event.pos[0]), -(self.selection_first_pos[1]-event.pos[1])))
                        self.selection_rect.normalize()
                        for tile in self.tileGroup:
                            if(self.selection_rect.colliderect(tile.rect)):
                                tile.tmpmarked=True
                                tile.color()
                            else:
                                tile.tmpmarked=False
                                tile.color()
            
            #Update groups
            self.tileGroup.update(time/1000)
            
            #Drawing
            self.surface.blit(self.background, (0,0))
            self.tileGroup.draw(self.surface)
            
            pygame.display.update()
            
if( __name__ == "__main__") :
    game = Game(800, 800, 120)
    game.setup()
    game.gameloop()