import random as rd
#game setup
WIDTH = 960
HEIGHT = 720
FPS = 60
TILESIZE = 32

#UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'window/Kanit-Medium.ttf'
UI_FONT_SIZE = 18

#Color
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

#weapons
weapon_data = {
    'sword_lv0' : {'cooldown': 100,
                   'damage' : 10,
                   'graphic' : 'weapon/sword_lv0/full.png'}
    }

#ultimate
ultimate_data = {
    'pistol' : {
        'strength': 5,
        'graphic':'weapon/ultimate/ultimate.gif'
        }
    }
#enemy
monster_data = {
    #Dungeon1_Monster
    #Minor1
    'Ochre Jelly' : {'health': 50,
                'damage': 5,
                'reward': rd.randint(1,5), 
                'urank_reward': 1,
                'attack_sound':'',
                'speed':3,
                'resistance': 3,
                'attack_radius': 32,
                'notice_raius': 360},
    #Minor2
    'Death Slime':{'health': 100, 
                'damage': 7,
                'reward': rd.randint(2,5), 
                'urank_reward': 1,
                'attack_sound':'',
                'speed':3,
                'resistance': 3,
                'attack_radius': 32,
                'notice_raius': 360},
    #Boss
    'Acid Ooze'  :{'health': 150, 
                'damage': 10,
                'reward': 10, 
                'urank_reward': 1,
                'attack_sound':'',
                'speed':3,
                'resistance': 5,
                'attack_radius': 60,
                'notice_raius': 360}
        }  