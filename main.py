# coding=utf-8

import pygame, sys
from pygame.locals import *
from colors import *
from copy import deepcopy

def terminate():
    pygame.quit()
    sys.exit()

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, marked = False, health = 1, sizew = 1, sizeh = 1):
        pygame.sprite.Sprite.__init__(self)
        
        self.type = "wall"
        self.game = game
        self.marked = marked
        self.sizew = sizew
        self.sizeh = sizeh
        
        
        self.image = pygame.Surface((self.sizew*self.game.basesize, self.sizeh*self.game.basesize))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        self.tmpmarked = False
        
        self.health = health
        self.posx = self.rect.centerx//(self.game.basesize*self.sizew)
        self.posy = self.rect.centery//(self.game.basesize*self.sizeh)
        
        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()
        
        self.color()
        
        
    def update(self, time):
        pass
    
    def clicked(self):
        self.marked = not self.marked
        if(self.game.lattice[self.posy][self.posx] == "wall"):
            self.game.lattice[self.posy][self.posx] = "markedwall"
        elif(self.game.lattice[self.posy][self.posx] == "markedwall"):
            self.game.lattice[self.posy][self.posx] = "wall"
        self.color()
    
    def color(self):
        if(self.marked):
            if(self.tmpmarked):
                self.image.fill(self.game.backgroundcolor)
                self.image.fill(OLIVE, rect=(1, 1, self.rect.width-2, self.rect.height-2))
            else:
                self.image.fill(self.game.backgroundcolor)
                self.image.fill(CAPRI, rect=(1, 1, self.rect.width-2, self.rect.height-2))
        else:
            if(self.tmpmarked):
                self.image.fill(self.game.backgroundcolor)
                self.image.fill(AQUA, rect=(1, 1, self.rect.width-2, self.rect.height-2))
            else:
                self.image.fill(self.game.backgroundcolor)
                self.image.fill(CORAL, rect=(1, 1, self.rect.width-2, self.rect.height-2))
                
    def isHit(self, n):
        self.health -= n
        if(self.health <= 0):
            self.die()
    
    def die(self):
        self.game.tileGroup.add(Tile(self.game, self.rect.centerx, self.rect.centery))
        self.game.lattice[self.posy][self.posx] = "tile"
        self.kill()
    
class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, claimed = False, sizew = 1, sizeh = 1):
        pygame.sprite.Sprite.__init__(self)
        
        self.type = "tile"
        self.game = game
        self.x = x
        self.claimed = claimed
        self.sizew = sizew
        self.sizeh = sizeh
        
        self.image = pygame.Surface((self.sizew*self.game.basesize, self.sizeh*self.game.basesize))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        self.posx = self.rect.centerx//(self.game.basesize*self.sizew)
        self.posy = self.rect.centery//(self.game.basesize*self.sizeh)
        
        self.mask = pygame.mask.from_surface(self.image, 0)
        
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
        
        self.goingTo = None
        self.bestWay = None
        self.index = 0
        self.finished = False
        #self.move(10,10)
        #pygame.draw.circl
        #self.mask = pygame.mask.from_threshold(self.image, YELLOW)
        #self.mask.fill()
        #print(self.mask.outline())
        
    
    def update(self, time):
        #print(self.finished)
        if(self.game.changed or self.finished):
            self.finished = False
            self.chooseMove()
        self.calculateMove()
        self.move(self.vx*time*self.movespeed*self.game.basesize, self.vy*time*self.movespeed*self.game.basesize)
        if(self.goingTo):
            if(self.goingTo.type == "wall"):
                #see if they are close
                if(abs(self.posx - self.goingTo.posx) + abs(self.posy - self.goingTo.posy) <= 1):
                    #see if they collide
                    if(pygame.sprite.collide_mask(self, self.goingTo)):
                        #print("Collide")
                        self.goingTo.isHit(self.strength)
                        self.finished = True
                        self.goingTo = None
                        self.bestWay = None
                        self.index = 0
            
    def findWay(self, start, stop):
        #print(start, stop)
        def costEstimate(a, b):
            return(abs(a[0] - b[0]) + abs(a[1] + b[1]))
        
        def reconstructPath(current_node):
            try:
                return(reconstructPath(came_from[current_node]) + [(current_node)])
            except:
                return([(current_node)])
        def neighborNodes(node):
            foo = []
            try:
                bar = self.game.lattice[node[1]+1][node[0]]
                if(bar == "tile" or bar == "markedwall"):
                    foo.append((node[0], node[1]+1))
            except:
                pass
            try:
                bar = self.game.lattice[node[1]-1][node[0]]
                if(bar == "tile" or bar == "markedwall"):
                    foo.append((node[0], node[1]-1))
            except:
                pass
            try:
                bar = self.game.lattice[node[1]][node[0]+1]
                if(bar == "tile" or bar == "markedwall"):
                    foo.append((node[0]+1, node[1]))
            except:
                pass
            try:
                bar = self.game.lattice[node[1]][node[0]-1]
                if(bar == "tile" or bar == "markedwall"):
                    foo.append((node[0]-1, node[1]))
            except:
                pass
            #print(foo)
            return(foo)
            
            
            
        closedset = []
        openset = [start]
        came_from = {}
        
        g_score = {}
        f_score = {}
        
        g_score[start] = 0
        f_score[start] = g_score[start] + costEstimate(start, stop)
        
        while(openset):
            current = openset[0]
            #Find the one with the smallest score
            for i in openset:
                if(f_score[i] < f_score[current]):
                    current = i
            if(current == stop):
                return(reconstructPath(stop))
            
            openset.remove(current)
            closedset.append(current)
            for neighbor in neighborNodes(current):
                #print(neighbor)
                if(neighbor in closedset):
                    continue
                #if(neighbor in closedset):
                    #continue    
                tenative_g_score = g_score[current] + 1
                
                if(neighbor not in openset or tenative_g_score <= g_score[neighbor]):
                    came_from[neighbor] = current
                    g_score[neighbor] = tenative_g_score
                    f_score[neighbor] = g_score[neighbor] + costEstimate(neighbor, stop)
                    if(neighbor not in openset):
                        openset.append(neighbor)
        return(None)
        
    def chooseMove(self):
        #Find the position of a clicked area you can get to
        #Bar is the pos of all walls that touch the tiles
        
        #if(not self.game.changed):
        #    return(None)
        self.goingTo = None
        self.bestWay = None
        
        bar = []
        for tile in self.game.tileGroup:
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
        flag = False
        for wall in self.game.wallGroup:
            if(flag):
                break
            if(wall.marked):
                for (i,j) in bar:
                    if(wall.rect.collidepoint(i,j)):
                        foo = self.findWay((self.rect.centerx//(self.game.basesize*wall.sizew), self.rect.centery//(self.game.basesize*wall.sizeh)), (wall.rect.centerx//(wall.game.basesize*wall.sizew), wall.rect.centery//(wall.game.basesize*wall.sizeh)) )
                        #print(foo)
                        if(len(foo) <= 2):
                            self.bestWay = foo
                            flag = True
                            break
                        try:
                            if(len(foo) < len(self.bestWay)):
                                self.bestWay = foo
                        except:
                            self.bestWay = foo
        
                    
                        #self.goingTo = wall
                        #flag = True
                    """
                    if(wall.rect.collidepoint(i,j)):
                        self.goingTo = wall
                        flag = True
                        break
                    """
        try:
            self.bestWay[1]
            for wall in self.game.wallGroup:
                if((wall.posx, wall.posy) == self.bestWay[1]):
                    self.goingTo = wall
                    self.index = 1
                    break
        except:
            pass
        if(not self.goingTo):
            try:
                self.bestWay[0]
                for wall in self.game.wallGroup:
                    if((wall.posx, wall.posy) == self.bestWay[0]):
                        self.goingTo = wall
                        self.index = 0
                        break
            except:
                pass
        
        if(not self.goingTo):
            try:
                #print("Se zgodim!!!!")
                self.bestWay[1]
                for tile in self.game.tileGroup:
                    #print("tiles: ", tile.posx, tile.posy)
                    if((tile.posx, tile.posy) == self.bestWay[1]):
                        self.goingTo = tile
                        self.index = 1
                        break
            except:
                pass
            if(not self.goingTo):
                try:
                    self.bestWay[0]
                    for tile in self.game.tileGroup:
                        if((tile.posx, tile.posy) == self.bestWay[0]):
                            self.goingTo = tile
                            self.index = 0
                            break
                except:
                    pass         

    def calculateMove(self):
        #Calculate movement vector
        #print(self.goingTo)
        if(self.goingTo):
            self.posx = self.rect.centerx//(self.game.basesize*self.goingTo.sizew)
            self.posy = self.rect.centery//(self.game.basesize*self.goingTo.sizeh)
            if(self.posx == self.goingTo.posx and self.posy == self.goingTo.posy):
                #print("Happenin")
                self.index += 1
                if(self.index >= len(self.bestWay)):
                    self.finished = True
                    self.index = 0
                    self.goingTo = None
                    self.bestWay = None
                    return(None)
                    
                #print(self.index, self.bestWay)
                self.goingTo = None
                for wall in self.game.wallGroup:
                    if((wall.posx, wall.posy) == self.bestWay[self.index]):
                        self.goingTo = wall
                        break
                if(not self.goingTo):
                    for tile in self.game.tileGroup:
                        if((tile.posx, tile.posy) == self.bestWay[self.index]):
                            self.goingTo = tile
                            break
                    

            try:
                dx = self.goingTo.rect.centerx - self.rect.centerx
                dy = self.goingTo.rect.centery - self.rect.centery
                #print(dx, dy)
                self.vx = dx/(dx**2 + dy**2)**(1/2)
                self.vy = dy/(dx**2 + dy**2)**(1/2)
                #print(self.vx, self.vy)
            except:
                self.vx = self.vy = 0
                self.goingTo = None
        else:
            self.vx = self.vy = 0
            
    def move(self, dx, dy):
        if(dx != 0 or dy != 0):
            self.movex += dx
            self.movey += dy
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
        self.changed = False
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
                    self.impGroup.add(Imp(self, i+5, j, movespeed = 10, strength= 1, hitspeed = 1))
                    self.impGroup.add(Imp(self, i-5, j, movespeed = 10, strength= 1, hitspeed = 1))
                    self.impGroup.add(Imp(self, i, j+5, movespeed = 10, strength= 1, hitspeed = 1))
                    self.impGroup.add(Imp(self, i, j-5, movespeed = 10, strength= 1, hitspeed = 1))
                    self.impGroup.add(Imp(self, i-5, j-5, movespeed = 10, strength= 1, hitspeed = 1))
                    self.lattice[-1][-1] = "tile"
                else:
                    self.wallGroup.add(Wall(self, i, j, False))
                    

        
    def gameloop(self):
        self.continue_playing = True
        self.clock.tick()
        while(self.continue_playing):
            time = self.clock.tick(self.fps)
            #print(self.lattice)
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
                                self.changed = True
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
                                self.changed = True   
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
            self.changed = False
            
            #Drawing
            self.surface.blit(self.background, (0,0))
            self.wallGroup.draw(self.surface)
            self.tileGroup.draw(self.surface)
            self.impGroup.draw(self.surface)
            
            pygame.display.update()
            
if( __name__ == "__main__") :
    game = Game(800, 800, fps=240)
    game.setup()
    game.gameloop()