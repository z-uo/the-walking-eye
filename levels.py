#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys, os
import pygame
from pygame.locals import *

from functions import *
from peoples import *

UNITE = 20

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, UNITE, UNITE)
        self.wall = False
        self.cloud = False
        self.ladder = False
        self.door = False
        self.doordir = ""
    #~ def make_ladder(self):
        #~ self.ladder = True
        #~ # ladder collision rect = 2 pixels in the center of the tile
        #~ self.ladderrect = pygame.Rect((self.rect.x + (UNITE/2)) - 1,
                                      #~ self.rect.y,
                                      #~ (self.rect.x + (UNITE/2)) + 1,
                                      #~ UNITE)
        

                
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
                    #~ p.make_ladder()
                    tiletable[y].append(p)
                # bottom ladder
                elif map[y][x] == "b":
                    imgmap.blit(self.floor, (x*UNITE, y*UNITE))
                    imgmap.blit(self.ladder, (x*UNITE, y*UNITE))
                    p = Platform(x*UNITE, y*UNITE)
                    p.ladder = True
                    #~ p.make_ladder()
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
        
