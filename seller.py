import pygame as pg
from settings import *
from entity import Entity
from support import *

class Seller(Entity):
    def __init__(self,pos,groups,sprite_type):
        super().__init__(groups)
        img1 = pg.image.load('seller/seller2/idle/0.png')
        img2 = pg.transform.scale(img1,(32,32))
        self.image = img2.convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.import_seller_assets()
        self.status = 'idle'
    def import_seller_assets(self):
        character_path = 'seller/seller2'
        self.animations = {'idle':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    def animate(self):
        self.frame_index = 0
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
    def update(self):
        self.animate()