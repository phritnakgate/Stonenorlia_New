import pygame as pg
import sys
from settings import *
from level import Level
from level1 import Level1

#Main Window 
pg.init()
window = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()    #FPS
level = Level()
level1 = Level1()

# Window Config
pg.display.set_caption("Stonenorlia")
gicon = pg.image.load('window/cave_icon.png')
pg.display.set_icon(gicon)
font = pg.font.Font(UI_FONT,UI_FONT_SIZE)

keys = pg.key.get_pressed()

current_level = 0
class Gamestate():
    def __init__(self):
        self.current_level = current_level
    def main_lv(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_b:
                    pg.time.wait(500)
                    
                    self.current_level = 1
                    print(self.current_level)
            window.fill([0, 0, 0])
            level.run() #Open Main level
           
             
            
    def lv1(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_b:
                    pg.time.wait(500)
                    
                    self.current_level = 0
                    print(self.current_level)
            window.fill([0, 0, 0])
            level1.run()    #Open Dungeon1 level
        
            

if __name__ == '__main__':
    game_state = Gamestate()

while True:
    cl = game_state.current_level
    
    if cl == 0:
        
        game_state.main_lv()
        pg.display.update()
        clock.tick(FPS)
    else:
     
        game_state.lv1()
        pg.display.update()
        clock.tick(FPS)
    
    