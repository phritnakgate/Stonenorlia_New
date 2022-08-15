import pygame as pg
from settings import *
from player import *

class UI:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font(UI_FONT,UI_FONT_SIZE)

        self.health_bar_rect = pg.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pg.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)
    
    def show_bar(self,current,max_amount,bg_rect,color):
        pg.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        
        #convert stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        #draw
        pg.draw.rect(self.display_surface,color,current_rect)
        pg.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
    
    def show_money(self,money):
        text_surf = self.font.render(str(int(money)),False,TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))
        
        pg.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pg.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pg.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
    
    def weapon_box(self,left,top):
        bg_rect = pg.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pg.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        pg.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect
    
    def weapon_overlay(self,weapon_index):
        bg_rect = self.weapon_box(10,630)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf,weapon_rect)
    
    def show_ult(self,ultimate_pt):
        text_surf = self.font.render(str(int(ultimate_pt)),False,TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 80
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))
        
        pg.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pg.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)
    
    def display(self,player):
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)

        self.show_money(player.money)   #money
        self.show_ult(player.ultimate_pt)
        
        self.weapon_overlay(player.weapon_index)