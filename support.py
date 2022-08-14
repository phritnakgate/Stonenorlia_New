import pygame as pg
from csv import reader
from os import walk

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        layout = reader(map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []
    
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
        return surface_list