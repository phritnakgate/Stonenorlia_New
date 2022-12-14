import pygame as pg
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from support import *
from weapon import *
from ui import *
from ultimate import *

class Level1:
	def __init__(self):
		self.display_surface = pg.display.get_surface()
		
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pg.sprite.Group()
		self.all_sprites = pg.sprite.Group()
		self.attack_sprite = pg.sprite.Group()
		self.attackable_sprites = pg.sprite.Group()

		self.current_attack = None
		self.current_ultimate = None

		self.create_map()

		self.ui = UI()
	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('map\level1\level_1_obstacle.csv'),
			'enemy': import_csv_layout('map\level1\level_1_entity.csv')
			}
		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index,col in enumerate(row):
					if col !='-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style == 'enemy':
							if col == '0':
								Enemy('Ochre Jelly',(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.damage_player)
							elif col == '1':
								Enemy('Death Slime',(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.damage_player)
							elif col == '2':
								Enemy('Acid Ooze',(x,y),[self.visible_sprites,self.attackable_sprites],self.obstacle_sprites,self.damage_player)
		self.player = Player((64,1440),[self.visible_sprites,self.attack_sprite],self.obstacle_sprites,self.all_sprites,self.create_attack,self.destroy_weapon,self.create_ultimate,self.destroy_ultimate)

	def create_attack(self):
		self.current_attack = Weapon(self.player,[self.visible_sprites])
	def create_ultimate(self,style,strength):
		self.current_ultimate = Ultimate(self.player,[self.visible_sprites])
	
	def destroy_weapon(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None
	def destroy_ultimate(self):
		if self.current_ultimate:
			self.current_ultimate.kill()
		self.current_ultimate = None
	
	def player_attack_logic(self):
		if self.attack_sprite:
			for attack_sprite in self.attack_sprite:
				collision_sprites = pg.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						target_sprite.get_damage(self.player,attack_sprite.sprite_type)
	def damage_player(self,amount):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pg.time.get_ticks()
	def toggle_shop(self):
		pass
	
	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.visible_sprites.enemy_update(self.player)
		self.player_attack_logic()
		self.ui.display(self.player)

#Camera
class YSortCameraGroup(pg.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pg.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pg.math.Vector2()

		#create floor
		self.floor_surface = pg.image.load('map/Maintexture/level_1_terrain.png').convert_alpha()
		self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		#drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surface,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
	
	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)