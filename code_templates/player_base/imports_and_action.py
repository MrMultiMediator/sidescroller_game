from pygame.sprite import Sprite
from pygame.transform import flip
from pygame import image, Surface
import pygame
import json
import os

class Action:
    def __init__(self, name, status="running"):
        self.name = name
        self.status = status

    def __repr__(self):
        return self.name

