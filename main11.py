#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys, os
import pygame
from pygame.locals import *

UNITE = 20
SIZE = WIDTH, HEIGHT = 200, 200


def loadimg(filename, rect=False):
    """ load image with alpha support
        return pygame image with or without rect """
    filename = os.path.join('data', filename)
    try:
        img = pygame.image.load(filename)
        if img.get_alpha is None:
            img = img.convert()
        else:
            img = img.convert_alpha()
    except pygame.error, message:
        print "Impossible de charger l'image : ", filename
        raise SystemExit, message
    if rect:
        return img, img.get_rect()
    else:
        return img


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, UNITE, UNITE)
        self.wall = False
        self.cloud = False
        self.ladder = False
        self.door = False
        self.doordir = ""
        

class Underfoot(pygame.sprite.Sprite):
    def __init__(self, width):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, width, 1)
        
        self.img = pygame.Surface((width, 1)).convert()
        self.img.fill(Color("#FF0000"))
        
    def is_collide(self, platform):
        coll = False
        for p in platform:
            if pygame.sprite.collide_rect(self, p):
                coll = True
        return coll
        
        
class Someone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.onground = False
        self.xvec = 0 # horizontal
        self.yvec = 0 # vertical
        
    def tiles_to_check(self, tiletable):
        x, y = int(self.rect.center[0]/UNITE), int(self.rect.center[1]/UNITE)
        walltiles = []
        cloudtiles = []
        doortiles = []
        for d in (tiletable[y][x], 
                   tiletable[y+1][x], 
                   tiletable[y][x+1], 
                   tiletable[y-1][x], 
                   tiletable[y][x-1], 
                   tiletable[y+1][x+1], 
                   tiletable[y-1][x-1], 
                   tiletable[y+1][x-1], 
                   tiletable[y-1][x+1]):
            if d.wall:
                walltiles.append(d)
            if d.cloud:
                cloudtiles.append(d)
            if d.door:
                doortiles.append(d)
        return walltiles, cloudtiles, doortiles
        
    def is_onground(self, platform, platformcloud, yvec):
        if self.yvec < 0:
            return False
        self.underfoot.rect.topleft = (self.rect.left, self.rect.bottom)
        if self.is_collide(platform):
            return False
        if self.underfoot.is_collide(platform):
            return True
        for p in platformcloud:
            if not pygame.sprite.collide_rect(self, p) and pygame.sprite.collide_rect(self.underfoot, p):
                return True
        return False
        
    def is_collide(self, platform):
        coll = False
        for p in platform:
            if pygame.sprite.collide_rect(self, p):
                coll = True
        return coll
        
        
class Badguy(Someone):
    def __init__(self, x, y, direction):
        Someone.__init__(self)
        self.rimg, self.rect = loadimg("mechant.png", True)
        self.limg = pygame.transform.flip(self.rimg, True, False)
        self.image = self.rimg
        self.rect.topleft = (x, y)
        self.xvec = direction
        self.underfoot = Underfoot(self.rect.width)
        
    def update(self, tiletable):
        """move hero and adjust if collision
        """
        walltiles, cloudtiles,  doortiles = self.tiles_to_check(tiletable)
        self.onground = self.is_onground(walltiles, cloudtiles, self.yvec)
        
        if self.onground == False:
            self.yvec += 1
        else:
            self.yvec = 0
        
            
        if self.xvec > 0:
            self.img = self.rimg
        elif self.xvec < 0:
            self.img = self.limg
        
        # check horizontal move
        self.rect = self.rect.move(self.xvec, 0)
        if self.xvec > 0:
            if self.is_collide(walltiles):
                self.rect = self.rect.move(-2, 0)
                self.xvec = -1
        elif self.xvec < 0:
            if self.is_collide(walltiles):
                self.rect = self.rect.move(2, 0)
                self.xvec = 1
        
        # check vertical move
        # check moving down
        if self.yvec > 0:
            for i in range(self.yvec):
                if not self.is_onground(walltiles, cloudtiles, self.yvec):
                    self.rect = self.rect.move(0, 1)
                else: break
        # check moving up
        elif self.yvec < 0:
            for i in range(-self.yvec):
                if not self.is_collide(walltiles):
                    self.rect = self.rect.move(0, -1)
                else: 
                    self.yvec = 0 # cogne au plafond
                    self.rect = self.rect.move(0, 1)
                    break
        
class Hero(Someone):
    def __init__(self):
        Someone.__init__(self)
        self.rimg, self.rect = loadimg("hero.png", True)
        self.limg = pygame.transform.flip(self.rimg, True, False)
        self.img = self.rimg
        self.underfoot = Underfoot(self.rect.width)
        
    def update(self, key, tiletable):
        """move hero and adjust if collision
        """
        walltiles, cloudtiles, doortiles = self.tiles_to_check(tiletable)
        self.onground = self.is_onground(walltiles, cloudtiles, self.yvec)
        
        self.xvec = 0
        if self.onground == False:
            self.yvec += 1
        else:
            self.yvec = 0
        if key["up"] and self.onground:
            self.yvec = -10
        if key["right"]:
            self.xvec += 2
        if key["left"]:
            self.xvec -= 2
            
        if self.xvec > 0:
            self.img = self.rimg
        elif self.xvec < 0:
            self.img = self.limg
        
        # check horizontal move
        if self.xvec != 0:
            self.rect = self.rect.move(self.xvec, 0)
            if self.xvec > 0:
                for i in range(self.xvec/2):
                    if self.is_collide(walltiles):
                        self.rect = self.rect.move(-2, 0)
                    else: break
            elif self.xvec < 0:
                for i in range(-self.xvec/2):
                    if self.is_collide(walltiles):
                        self.rect = self.rect.move(2, 0)
                    else: break
        
        # check vertical move
        # check moving down
        if self.yvec > 0:
            for i in range(self.yvec):
                if not self.is_onground(walltiles, cloudtiles, self.yvec):
                    self.rect = self.rect.move(0, 1)
                else: break
        # check moving up
        elif self.yvec < 0:
            for i in range(-self.yvec):
                if not self.is_collide(walltiles):
                    self.rect = self.rect.move(0, -1)
                else: 
                    self.yvec = 0 # cogne au plafond
                    self.rect = self.rect.move(0, 1)
                    break
        # check doors
        for d in doortiles:
            if pygame.sprite.collide_rect(self, d):
                return d
        return False
            
                
                
class Level(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
    def create(self, map, size):
        tiletable = []
        doors = pygame.sprite.Group()
        people = pygame.sprite.Group()
        imgmap = pygame.Surface(size).convert()
        imgmap.fill(Color("#000000"))
        for y in range(len(map)):
            tiletable.append([])
            for x in range(len(map[y])):
                if map[y][x] == "#":
                    imgmap.blit(self.wall, (x*UNITE, y*UNITE))
                    p = Platform(x*UNITE, y*UNITE)
                    p.wall = True
                    tiletable[y].append(p)
                elif map[y][x] == ",":
                    imgmap.blit(self.floor, (x*UNITE, y*UNITE))
                    p = Platform(x*UNITE, y*UNITE)
                    tiletable[y].append(p)
                # bad guy
                elif map[y][x] == "<":
                    imgmap.blit(self.floor, (x*UNITE, y*UNITE))
                    p = Platform(x*UNITE, y*UNITE)
                    tiletable[y].append(p)
                    b = Badguy(x*UNITE, y*UNITE, -1)
                    people.add(b)
                # cloud
                elif map[y][x] == "c":
                    p = Platform(x*UNITE, y*UNITE)
                    p.cloud = True
                    tiletable[y].append(p)
                # top ladder
                elif map[y][x] == "t":
                    imgmap.blit(self.ladder, (x*UNITE, y*UNITE))
                    p = Platform(x*UNITE, y*UNITE)
                    p.cloud = True
                    p.ladder = True
                    tiletable[y].append(p)
                # bottom ladder
                elif map[y][x] == "b":
                    imgmap.blit(self.floor, (x*UNITE, y*UNITE))
                    imgmap.blit(self.ladder, (x*UNITE, y*UNITE))
                    p = Platform(x*UNITE, y*UNITE)
                    p.ladder = True
                    tiletable[y].append(p)
                elif map[y][x] == "P":
                    p = Platform(x*UNITE, y*UNITE)
                    p.door = True
                    p.doordir = -1
                    doors.add(p)
                    tiletable[y].append(p)
                elif map[y][x] == "N":
                    p = Platform(x*UNITE, y*UNITE)
                    p.door = True
                    p.doordir = 1
                    doors.add(p)
                    tiletable[y].append(p)
                else:
                    p = Platform(x*UNITE, y*UNITE)
                    tiletable[y].append(p)
        return imgmap, tiletable, people, doors
        
        
class Level01(Level):
    def __init__(self, parent):
        Level.__init__(self)
        self.parent = parent
        self.name = "level01"
        
    def init_level(self):
        map = ["##########",
               "####..####",
               "####..####",
               "#........#",
               "#..,,,,..#",
               "#..cctc..#",
               "#,,<,b...#",
               "######...#",
               "#....,,,,#",
               "#....#######",
               "#,,,,,,,,,N#",
               "############"]
        self.rect = (0, 0, 200, 240)
        self.size = (200, 240)
        self.offset = (0, 40, 200, 240)
        self.wall, wallrect = loadimg("wall.png", True)
        self.ladder, ladderrect = loadimg("ladder.png", True)
        self.floor = loadimg("floor.png")
        self.img, self.tiletable, self.people, self.doors = self.create(map, self.size)
        
    def init_hero_pos(self, prev=""):
        if prev == "level02" :
            return  (188, 202)
        else:
            return (94, 20)
        
        
class Level02(Level):
    def __init__(self, parent):
        Level.__init__(self)
        self.parent = parent
        self.name = "level02"
        
    def init_level(self):
        map = ["##############",
               "###.........N#",
               "###.........N#",
               "###....,,,,,N#",
               "###....#######",
               "###,,,.....#",
               "######...,,#",
               "######.,,###",
               "#P,,,,,#####",
               "############"]
        self.rect = (0, 0, 240, 200)
        self.size = (240, 200)
        self.offset = (40, 0, 240, 200)
        self.wall, wallrect = loadimg("wall.png", True)
        self.floor = loadimg("floor.png")
        self.img, self.tiletable, self.people, self.doors = self.create(map, self.size)
        
    def init_hero_pos(self, prev=""):
        if prev == "level01" :
            return  (40, 162)
        elif prev == "level03" :
            return  (228, 62)
        else:
            return (40, 162)
        
        
class Level03(Level):
    def __init__(self, parent):
        Level.__init__(self)
        self.parent = parent
        self.name = "level03"
    def init_level(self):
        map = ["############",
               "#P.........#",
               "#P.........#",
               "#P,,,,,....#",
               "#######,...#",
               "########...#",
               "#######..,,#",
               "###......#####",
               "###,,,,,,,,,N#",
               "##############"]
        self.rect = (0, 0, 240, 200)
        self.size = (240, 200)
        self.offset = (40, 0, 240, 200)
        self.wall, wallrect = loadimg("wall.png", True)
        self.floor = loadimg("floor.png")
        self.img, self.tiletable, self.people, self.doors = self.create(map, self.size)
        
    def init_hero_pos(self, prev=""):
        if prev == "level02" :
            return (40, 62)
        if prev == "level04" :
            return (228, 162)
        else:
            return (40, 62)
        
        
class Level04(Level):
    def __init__(self, parent):
        Level.__init__(self)
        self.parent = parent
        self.name = "level04"
    def init_level(self):
        map = ["############",
               "###........#",
               "###........#",
               "###,,,,....#",
               "#######,...#",
               "########...#",
               "#######..,,#",
               "###......###",
               "#P,,,,,,,,,#",
               "############"]
        self.rect = (0, 0, 240, 200)
        self.size = (240, 200)
        self.offset = (40, 0, 240, 200)
        self.wall, wallrect = loadimg("wall.png", True)
        self.floor = loadimg("floor.png")
        self.img, self.tiletable, self.people, self.doors = self.create(map, self.size)
        
    def init_hero_pos(self, prev=""):
        if prev == "level03" :
            return (40, 162)
        else:
            return (40, 162)
        
        
class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.timer = pygame.time.Clock()
        self.key = {"up": False, 
                    "down": False, 
                    "right": False, 
                    "left": False, 
                    "jump": False}
        self.levelList = [Level01(self), Level02(self), Level03(self), Level04(self)]
        self.nlevel = 0
        self.init_level()
    
    def init_level(self):
        self.level = self.levelList[self.nlevel]
        self.level.init_level()
        self.surfprov = pygame.Surface(self.level.size)
        self.surfprov.blit(self.level.img, self.level.rect)
        self.hero = Hero()
        self.hero.rect.topleft = self.level.init_hero_pos()
        self.surfprov.blit(self.hero.img, self.hero.rect)
        self.screen.blit(self.surfprov, (0, 0), self.level.offset)
        pygame.display.update()
        self.loop()
        
    def change_level(self, n):
        self.nlevel += n
        prev = self.level.name
        self.level = self.levelList[self.nlevel]
        self.level.init_level()
        self.surfprov = pygame.Surface(self.level.size)
        self.surfprov.blit(self.level.img, self.level.rect)
        self.hero.rect.topleft = self.level.init_hero_pos(prev)
        
    def check_input(self):
        self.key["up"] = False
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit, "QUIT"
            elif e.type == KEYDOWN:
                if e.key == K_UP:
                    self.key["up"] = True
                if e.key == K_DOWN:
                    self.key["down"] = True
                if e.key == K_RIGHT:
                    self.key["right"] = True
                if e.key == K_LEFT:
                    self.key["left"] = True
                if e.key == K_x:
                    self.key["jump"] = True
            elif e.type == KEYUP:
                if e.key == K_UP:
                    self.key["up"] = False
                if e.key == K_DOWN:
                    self.key["down"] = False
                if e.key == K_RIGHT:
                    self.key["right"] = False
                if e.key == K_LEFT:
                    self.key["left"] = False
                if e.key == K_x:
                    self.key["jump"] = False
                    
    def blit(self):
        self.surfprov.blit(self.level.img, self.hero.rect, self.hero.rect)
        self.surfprov.blit(self.level.img, self.hero.underfoot.rect, self.hero.underfoot.rect)
        self.level.people.clear(self.surfprov, self.level.img)
        
    def update(self):
        # update
        exitblock = self.hero.update(self.key, self.level.tiletable)
        if exitblock:
            self.change_level(exitblock.doordir)
        self.level.people.update(self.level.tiletable)
            
    def draw(self):
        self.surfprov.blit(self.hero.img, self.hero.rect)
        self.surfprov.blit(self.hero.underfoot.img, self.hero.underfoot.rect)
        self.level.people.draw(self.surfprov)
        self.screen.blit(self.surfprov, (0, 0), self.level.offset)
        pygame.display.update()
        
    def loop(self):
        while 1:
            self.timer.tick(30)
            self.check_input()
            self.blit()
            self.update()
            self.draw()
        
        
if(__name__ == "__main__"):
    game = Game()
