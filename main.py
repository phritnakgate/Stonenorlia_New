import pygame as pg
import sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        #Main Window 
        pg.init()
        self.window = pg.display.set_mode((WIDTH,HEIGHT))
        self.clock = pg.time.Clock()    #FPS
        self.level = Level()

        # Window Config
        pg.display.set_caption("Stonenorlia")
        gicon = pg.image.load('window/cave_icon.png')
        pg.display.set_icon(gicon)
        
    def run(self):
        #Window Loop
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            self.window.fill('black')
            self.level.run()
            pg.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
