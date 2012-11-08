#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys, os
import pygame
from pygame.locals import *

from functions import *

UNITE = 20

def is_collide(obj, platform):
    for p in platform:
        if pygame.sprite.collide_rect(obj, p):
            return True
    return False
    
def is_ontile(obj, platform):
    obj.underfoot.rect.topleft = (obj.rect.left, obj.rect.bottom)
    for p in platform:
        # verify one by one if underfoot collide platform and not the body (for clouds)
        if not pygame.sprite.collide_rect(obj, p) and pygame.sprite.collide_rect(obj.underfoot, p):
            # he is on something
            return True
    return False

        
class Underfoot(pygame.sprite.Sprite):
    def __init__(self, width):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, width, 1)
        
        self.img = pygame.Surface((width, 1)).convert()
        self.img.fill(Color("#FF0000"))
        
        
class Lazer(pygame.sprite.Sprite):
    def __init__(self, parent, direction, posx, posy, platform):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.platform = platform
        self.rect = pygame.Rect(0, 0, 8, 6)
        self.direction = direction
        self.isdying = False
        if self.direction == "left":
            self.rect.topright = (posx+10, posy+3)
            self.vecteur = -8
        if self.direction == "right":
            self.rect.topleft = (posx+2, posy+3)
            self.vecteur = 8
        self.image = pygame.Surface((8, 6)).convert()
        self.image.fill(Color("#FF0000"))
        
    def update(self):
        if not self.isdying:
            self.rect.x = self.rect.x + self.vecteur
            #~ if is_collide(self, self.platform):
            for i in range(abs(self.vecteur)):
                if is_collide(self, self.platform):
                    if self.vecteur > 0:
                        self.rect.x = self.rect.x - 1
                    if self.vecteur < 0:
                        self.rect.x = self.rect.x + 1
                    self.image.fill(Color("#FFFF00"))
                        
                    print "wall"
                    self.isdying = True
                else: 
                    break
                
        else:
                self.kill()
            
        
class Someone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.onground = False
        self.xvec = 0 # horizontal
        self.yvec = 0 # vertical
        
        
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
        self.direction = "right"
        
    def init_level(self, level):
        self.walltiles = level.walls
        self.cloudtiles = level.clouds
        self.laddertiles = level.ladders
        self.doortiles = level.doors
        self.onground = False
        self.oncloud = False
        self.cloudtimmer = 10
        self.acrosscloud = False
        self.bullets = pygame.sprite.Group()
        self.f = False
                
        self.onladder = False
        self.inladder = False
        self.hang = False
        
        self.rect.topleft = level.init_hero_pos()
        
    def update(self, key, tiletable):
        """move hero and adjust if collision
        """
        # see where the hero is
        self.onground = is_ontile(self, self.walltiles)
        self.oncloud = is_ontile(self, self.cloudtiles)
        self.inladder = is_collide(self, self.laddertiles)
        self.onladder = is_ontile(self, self.laddertiles)
        self.acrosscloud = False
        
        # jump
        if self.onground or (self.oncloud and not self.yvec<0):
            self.yvec = 0
        else:
            self.yvec += 1
        if key["jump"] and (self.onground or self.oncloud):
            self.yvec = -10
        
        # hang
        if self.hang and (key["jump"] or self.onground or self.oncloud or not self.inladder):
            self.hang = False
        if (key["up"] and self.inladder) or (key["down"] and self.onladder):
            self.hang = True
        
        if self.hang:
            self.yvec = 0
            if key["up"]:
                self.yvec = -2
            if key["down"]:
                self.yvec = 2
                self.acrosscloud = True
            
        
        # fall from cloud
        if key["down"] and self.oncloud and not self.hang:
            self.cloudtimmer -= 1
            print self.cloudtimmer
            if self.cloudtimmer == 0:
                self.yvec = 2
                self.acrosscloud = True
        else:
            self.cloudtimmer = 10
        
        # walk
        self.xvec = 0
        if key["right"]:
            self.xvec += 2
            self.direction = "right"
            self.img = self.rimg
        if key["left"]:
            self.xvec -= 2
            self.direction = "left"
            self.img = self.limg
            
        
        # check horizontal move
        if self.xvec != 0:
            self.rect = self.rect.move(self.xvec, 0)
            if self.xvec > 0:
                for i in range(self.xvec/2):
                    if is_collide(self, self.walltiles):
                        self.rect = self.rect.move(-2, 0)
                    else: break
            elif self.xvec < 0:
                for i in range(-self.xvec/2):
                    if is_collide(self, self.walltiles):
                        self.rect = self.rect.move(2, 0)
                    else: break
        
        # check vertical move
        # check moving down
        if self.yvec > 0:
            for i in range(self.yvec):
                if not is_ontile(self, self.walltiles):
                    if not is_ontile(self, self.cloudtiles) or self.acrosscloud:
                        self.rect = self.rect.move(0, 1)
                    else: break
                else: break
        # check moving up
        elif self.yvec < 0:
            for i in range(-self.yvec):
                if not is_collide(self, self.walltiles):
                    self.rect = self.rect.move(0, -1)
                else: 
                    self.yvec = 0 # cogne au plafond
                    self.rect = self.rect.move(0, 1)
                    break
        
        # fire
        if key["fire"]:
            self.bullet = Lazer(self, self.direction, self.rect.x, self.rect.y, self.walltiles)
            self.bullets.add(self.bullet)
            print "fire"
        
        self.bullets.update()
            
        # check doors
        for d in self.doortiles:
            if pygame.sprite.collide_rect(self, d):
                return d
        return False
        
            
                
