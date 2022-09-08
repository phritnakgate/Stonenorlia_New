import pygame as pg
from settings import *
from entity import Entity
from support import *
from player import *

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        
        #Graphics
        img1 = pg.image.load(f'enemy/level_1/{monster_name}/idle/0.png')
        img2 = pg.transform.scale(img1,(32,32))
        self.image = img2.convert_alpha()
        
        self.import_enemy_graphics(monster_name)
        self.status = 'idle'
        
        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.damage = monster_info['damage']
        self.reward = monster_info['reward']
        self.urank_reward = monster_info['urank_reward']
        self.speed = monster_info['speed']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_raius']

        #player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        #timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300


    def import_enemy_graphics(self,name):
        main_path = f'../enemy/level_1/{name}/'
        self.animations = {'idle':[],'move':[],'attack':[]}
        
        for animation in self.animations.keys():
            full_path = main_path + animation
            self.animations[animation] = import_folder(full_path)
    def get_player_distance_direction(self,player):
        enemy_vec = pg.math.Vector2(self.rect.center)
        player_vec = pg.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pg.math.Vector2()
        direction = (player_vec - enemy_vec).normalize()
        return (distance,direction)
    def get_status(self,player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    def actions(self,player):
        if self.status == 'attack':
            self.attack_time = pg.time.get_ticks()
            self.damage_player(self.damage)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pg.math.Vector2()
    def animate(self):
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    
    def cooldown(self):
        current_time = pg.time.get_ticks()
        if not self.can_attack:
            
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self,player,attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                pass
            self.hit_time = pg.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()
            
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
        