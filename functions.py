#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys, os
import pygame
from pygame.locals import *

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
