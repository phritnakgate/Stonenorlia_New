import pygame as pg
from settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.image = pg.Surface((32,32))
        self.rect = self.image.get_rect(topleft= pos)




