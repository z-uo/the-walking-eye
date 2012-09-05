#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys, os
import pygame
from pygame.locals import *

from levels import *
from functions import *
from peoples import *

SIZE = WIDTH, HEIGHT = 200, 200


class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
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
        self.key["jump"] = False
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
        #~ self.level.people.update(self.level.tiletable)
            
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
