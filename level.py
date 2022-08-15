import pygame as pg
from settings import *
from tile import Tile
from player import Player
from support import *
from weapon import *

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pg.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pg.sprite.Group()

		#attack sprites
		self.current_attack = None

		# sprite setup
		self.create_map()

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('map\level0\level_0_edit_blocked.csv'),
			'deco': import_csv_layout('map\level0\level_0_edit_decoration.csv')
			}
		#graphics = {
		#	'deco': import_folder('map\Maintexture\deco')
		#	}

		#Game Map & Object
		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index,col in enumerate(row):
					if col !='-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style == 'deco':
							if col == '0':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/0.png'))
							elif col == '32':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/32.png'))
							elif col == '34':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/34.png'))
							elif col == '64':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/64.png'))
							elif col == '66':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/66.png'))	
							elif col == '91':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/91.png'))
							elif col == '96':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/96.png'))
							elif col == '97':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/97.png'))
							elif col == '98':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/98.png'))
							elif col == '99':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/99.png'))
							elif col == '107':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/107.png'))
							elif col == '123':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/123.png'))
							elif col == '484':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/484.png'))	
							elif col == '485':
								Tile((x,y),[self.visible_sprites],'deco',pg.image.load('map/Maintexture/deco/485.png'))	
		
		#Player Spawn						
		self.player = Player((450,400),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_weapon)
	
	def create_attack(self):
		self.current_attack = Weapon(self.player,[self.visible_sprites])
	
	def destroy_weapon(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None
	
	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()

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
		self.floor_surface = pg.image.load('map/Maintexture/level_0_terrain.png').convert()
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