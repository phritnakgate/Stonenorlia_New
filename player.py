import pygame as pg
from settings import *
from support import *


class Player(pg.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_weapon,create_ultimate,destroy_ultimate):
		super().__init__(groups)
		
		img1 = pg.image.load('player/right/right0.png')
		img2 = pg.transform.scale(img1,(64,64))
		self.image = img2.convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)

		self.import_player_assets()
		self.status = 'right'
		self.frame_index = 0
		self.animation_speed = 0.15

		self.direction = pg.math.Vector2()
		self.attacking = False
		self.attack_cooldown = 200
		self.attack_time = None
		
		#WEAPON
		self.create_attack = create_attack
		self.destroy_weapon = destroy_weapon
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]

		self.obstacle_sprites = obstacle_sprites
		
		#ultimate
		self.create_ultimate = create_ultimate
		self.destroy_ultimate = destroy_ultimate
		self.ultimate_index = 0
		self.ultimate = list(ultimate_data.keys())[self.ultimate_index]


		#Stats
		self.stats = {
			'health': 100,
			'energy': 60,
			'attack': 10,
			'speed': 5
		}
		self.health = self.stats['health']
		self.energy = self.stats['energy']
		self.money = 0
		self.ultimate_pt = 0
		self.speed = self.stats['speed']
	#PlayerTexture
	def import_player_assets(self):
		character_path = 'player/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)
	#KeyBinds
	
	def input(self):
		if not self.attacking:
			keys = pg.key.get_pressed()

			#MOVE UP-DOWN
			if keys[pg.K_w]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pg.K_s]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0
			#MOVE LEFT-RIGHT
			if keys[pg.K_d]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pg.K_a]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			#ATTACK
			if keys[pg.K_SPACE]:
				self.attacking = True
				self.attack_time = pg.time.get_ticks()
				self.create_attack()
			#Ultimate
			if keys[pg.K_q]:
				self.attacking = True
				self.attack_time = pg.time.get_ticks()
				style = list(ultimate_data.keys())[self.ultimate_index]
				strength = list(ultimate_data.values())[self.ultimate_index]['strength'] + self.stats['attack']
				self.create_ultimate(style,strength)


			#Interaction
			if keys[pg.K_e]:
				pass

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def get_status(self):
		
		#idle
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'
		#attack
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')
	#Collision
	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom
	
	def animate(self):
		animation = self.animations[self.status]

		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def cooldowns(self):
		current_time = pg.time.get_ticks()
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False
				self.destroy_weapon()
				self.destroy_ultimate()

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)