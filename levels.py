#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys, os
import pygame
from pygame.locals import *

from functions import *
from peoples import *

UNITE = 32


def create_map(map, size):
    # images
    imgmap = pygame.Surface(size).convert()
    imgmap.fill(Color("#000000"))
    wall = loadimg("wall.png")
    ladder = loadimg("ladder.png")
    floor = loadimg("floor.png")
    # groups
    walls = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    ladders = pygame.sprite.Group()
    doors = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    for y in range(len(map)):
        for x in range(len(map[y])):
            # wall
            if map[y][x] == "#":
                imgmap.blit(wall, (x*UNITE, y*UNITE))
                p = Platform(x*UNITE, y*UNITE)
                p.wall = True
                walls.add(p)
            # floor
            elif map[y][x] == ",":
                imgmap.blit(floor, (x*UNITE, y*UNITE))
            # bad guy
            elif map[y][x] == "<":
                imgmap.blit(floor, (x*UNITE, y*UNITE))
                b = Badguy(x*UNITE, y*UNITE, -1)
                enemies.add(b)
            # cloud
            elif map[y][x] == "c":
                p = Platform(x*UNITE, y*UNITE)
                p.cloud = True
                clouds.add(p)
            # top ladder
            elif map[y][x] == "t":
                p = Platform(x*UNITE, y*UNITE)
                p.cloud = True
                clouds.add(p)
                
                imgmap.blit(ladder, (x*UNITE, y*UNITE))
                p = Platform((x*UNITE + (UNITE/2)) - 1, y*UNITE, 2, UNITE)
                p.ladder = True
                imgmap.blit(p.return_rect_img(), p.rect)
                ladders.add(p)
            # bottom ladder
            elif map[y][x] == "b":
                imgmap.blit(floor, (x*UNITE, y*UNITE))
                imgmap.blit(ladder, (x*UNITE, y*UNITE))
                p = Platform((x*UNITE + (UNITE/2)) - 1, y*UNITE, 2, UNITE)
                p.ladder = True
                imgmap.blit(p.return_rect_img(), p.rect)
                ladders.add(p)
            # door -1
            elif map[y][x] == "P":
                p = Platform(x*UNITE, y*UNITE)
                p.door = True
                p.doordir = -1
                doors.add(p)
            # door +1
            elif map[y][x] == "N":
                p = Platform(x*UNITE, y*UNITE)
                p.door = True
                p.doordir = 1
                doors.add(p)
    return imgmap, walls, clouds, ladders, doors, enemies
    
    
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w=UNITE, h=UNITE):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, w, h)
        self.wall = False
        self.cloud = False
        self.ladder = False
        self.door = False
        self.doordir = ""
        
    def return_rect_img(self):
        img = pygame.Surface((self.rect.w, self.rect.h)).convert()
        img.fill(Color("#FF0000"))
        return img
        
        
class Level01(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.name = "level01"
        
    def init_level(self):
        map = ["##########",
               "####..####",
               "####..####",
               "#........#",
               "#..,,,,..#",
               "#..cctc..#",
               "#,,,<b...#",
               "######...#",
               "#....,,,,#",
               "#....#######",
               "#,,,,,,,,,N#",
               "############"]
        self.rect = (0, 0, 384, 384)
        self.size = (384, 384)
        self.offset = (0, 64, 320, 320)
        self.img, self.walls, self.clouds, self.ladders, self.doors, self.enemies = create_map(map, self.size)
        self.img = loadimg("map1.png")
        
    def init_hero_pos(self, prev=""):
        if prev == "level02" :
            return  (188, 202)
        else:
            return (144, 32)
        
        
class Level02(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.name = "level02"
        
    def init_level(self):
        map = ["##############",
               "###.........N#",
               "###.........N#",
               "###....,,<,,N#",
               "###....#######",
               "###,<,.....#",
               "######...,,#",
               "######.,,###",
               "#P,,,,,#####",
               "############"]
        self.rect = (0, 0, 240, 200)
        self.size = (240, 200)
        self.offset = (40, 0, 240, 200)
        self.wall, wallrect = loadimg("wall.png", True)
        self.floor = loadimg("floor.png")
        self.img, self.walls, self.clouds, self.ladders, self.doors, self.enemies = create_map(map, self.size)
        
    def init_hero_pos(self, prev=""):
        if prev == "level01" :
            return  (40, 162)
        elif prev == "level03" :
            return  (228, 62)
        else:
            return (40, 162)
        
        
class Level03(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.name = "level03"
    def init_level(self):
        map = ["############",
               "#P.........#",
               "#P.........#",
               "#P,,,,<....#",
               "#######,...#",
               "########...#",
               "#######..,,#",
               "###......#####",
               "###,,,,<,,,,N#",
               "##############"]
        self.rect = (0, 0, 240, 200)
        self.size = (240, 200)
        self.offset = (40, 0, 240, 200)
        self.wall, wallrect = loadimg("wall.png", True)
        self.floor = loadimg("floor.png")
        self.img, self.walls, self.clouds, self.ladders, self.doors, self.enemies = create_map(map, self.size)
        
    def init_hero_pos(self, prev=""):
        if prev == "level02" :
            return (40, 62)
        if prev == "level04" :
            return (228, 162)
        else:
            return (40, 62)
        
        
class Level04(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.name = "level04"
    def init_level(self):
        map = ["############",
               "###........#",
               "###........#",
               "###,,<,....#",
               "#######,...#",
               "########...#",
               "#######..,,#",
               "###......###",
               "#P,,,,,,,<,#",
               "############"]
        self.rect = (0, 0, 240, 200)
        self.size = (240, 200)
        self.offset = (40, 0, 240, 200)
        self.wall, wallrect = loadimg("wall.png", True)
        self.floor = loadimg("floor.png")
        self.img, self.walls, self.clouds, self.ladders, self.doors, self.enemies = create_map(map, self.size)
        
    def init_hero_pos(self, prev=""):
        if prev == "level03" :
            return (40, 162)
        else:
            return (40, 162)
        
