#!/usr/bin/env python3

import random
import os
import math
import time
import json

from graphics import GraphWin, Circle, Point, update, Rectangle, Text, Entry, Line, Image
from screeninfo import get_monitors


settings = {
    "window_x": {"value": 1280,"modifiable": False},
    "window_y": {"value": 960,"modifiable": False},
    "top_boundary": {"value": 100,"modifiable":False},
    "frame_rate": {"value": 60,"modifiable": True},
    "debug_mode": {"value": False,"modifiable": True},
    "bg_color": {"value": "black","modifiable": True},
    "bg_flash": {"value": "red","modifiable":True},
    "fg_color": {"value": "white","modifiable": True},
    "hero_size": {"value": 10,"modifiable": True},
    "hero_color": {"value": "aqua","modifiable": True},
    "hero_speed": {"value": 8,"modifiable": True},
    "mob_color": {"modifiable": True,
        "value": ["red","lime","blue","yellow","orchid1","snow2","tan1","brown1"]},
    "mob_splat_color": {"modifiable": True,
        "value": ["red4","dark green","blue4","yellow4","orchid4","snow4","tan4","brown4"]},
    "mob_size": {"value": 8,"modifiable": True},
    "mob_speed": {"value": 0.5,"modifiable": True},
    "projectile_size": {"value": 3,"modifiable": True},
    "projectile_speed": {"value": 16,"modifiable": True},
    "projectile_max_distance": {"value": 400,"modifiable":True},
    "extra_radius": {"value": 5,"modifiable":True},
    "max_name_len": {"value": 20,"modifiable":False},
    "xset_default": {"value": 70,"modifiable":False},
    "keys": {"modifiable":True,    
        "move_up": {"value": "Up","modifiable": True},
        "move_down": {"value": "Down","modifiable": True},
        "move_left": {"value": "Left","modifiable": True},
        "move_right": {"value": "Right","modifiable": True},
        "shoot": {"value": "Control_L","modifiable": True},
        "pause": {"value": "p","modifiable": True},
        "switch_weapon": {"value": "Shift_L","modifiable": True},
    }
}


all_guns = [
    {"p_type":"Gun","name":"Shotgun","type":"Spread","use":"immediate","value":50,"tier":1,"radius":3,
     "decay_time":300,"decay":0,"passthru":0,"price":1000,"ammo":200,
     "damage":0.5,"fire_rate":12,"angle":45,"n":7,"range":settings["projectile_max_distance"]["value"]/2,
     "speed":settings["projectile_speed"]["value"],"color":"white"},
    
    {"p_type":"Gun","name":"SMG","type":"Basic","use":"immediate","value":50,"tier":1,"radius":3,
     "decay_time":300,"decay":0,"passthru":0,"price":1500,"ammo":500,
     "damage":1,"fire_rate":4,"angle":45,"n":1,"range":settings["projectile_max_distance"]["value"]*0.6,
     "speed":settings["projectile_speed"]["value"],"color":"white"},
    
    {"p_type":"Gun","name":"ShatterGun","type":"Shatter","use":"immediate","value":50,"tier":1,"radius":3,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":0,"price":2000,"ammo":100,
     "damage":1,"fire_rate":8,"angle":30,"n":3,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"],"color":"white"},
    
    {"p_type":"Gun","name":"SplitGun","type":"Split","use":"immediate","value":50,"tier":1,"radius":3,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":0,"price":2000,"ammo":100,
     "damage":1,"fire_rate":8,"angle":30,"n":4,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"],"color":"white"},
    
    {"p_type":"Gun","name":"WideGun","type":"Wide","use":"immediate","value":50,"tier":2,"radius":3,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":1,"price":5000,"ammo":100,
     "damage":1,"fire_rate":6,"angle":10,"n":4,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"],"color":"white"},
    
    {"p_type":"Gun","name":"Heavy Pistol","type":"Basic","use":"immediate","value":50,"tier":2,"radius":3,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":1,"price":6000,"ammo":500,
     "damage":2,"fire_rate":20,"angle":30,"n":1,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"],"color":"white"},
    
    {"p_type":"Gun","name":"Rifle","type":"Basic","use":"immediate","value":50,"tier":2,"radius":3,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":2,"price":9000,"ammo":200,
     "damage":1,"fire_rate":16,"angle":30,"n":1,"range":settings["projectile_max_distance"]["value"]*2,
     "speed":settings["projectile_speed"]["value"]*2,"color":"white"},
    
    {"p_type":"Gun","name":"Heavy Shotgun","type":"Spread","use":"immediate","value":50,"tier":2,"radius":3,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":1,"price":12000,"ammo":200,
     "damage":1,"fire_rate":8,"angle":45,"n":7,"range":settings["projectile_max_distance"]["value"]/2,
     "speed":settings["projectile_speed"]["value"],"color":"white"},
    
    {"p_type":"Gun","name":"Split > ShatterGun","type":"Split > Shatter","use":"immediate","tier":2,"radius":3,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":0,"price":20000,"ammo":100,
     "damage":1,"fire_rate":6,"angle":30,"n":4,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"],"color":"white"},
    
    {"p_type":"Gun","name":"Assault Rifle","type":"Basic","use":"immediate","value":50,"tier":2,"radius":3,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":2,"price":22000,"ammo":250,
     "damage":2,"fire_rate":4,"angle":30,"n":1,"range":settings["projectile_max_distance"]["value"]*2,
     "speed":settings["projectile_speed"]["value"]*2,"color":"white"},
    
    {"p_type":"Gun","name":"Assault ShatterRifle","type":"Shatter","use":"immediate","value":50,"tier":2,"radius":3,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":1,"price":28000,"ammo":250,
     "damage":2,"fire_rate":5,"angle":60,"n":4,"range":settings["projectile_max_distance"]["value"]*1.75,
     "speed":settings["projectile_speed"]["value"]*2,"color":"white"},
    
    {"p_type":"Gun","name":"Plasma Orb","type":"Basic","use":"immediate","tier":2,"radius":10,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":3,"price":20000,"ammo":100,
     "damage":1,"fire_rate":6,"angle":30,"n":1,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"]*0.65,"color":"purple"},
    
    {"p_type":"Gun","name":"Plasma ShattOrb","type":"Shatter","use":"immediate","tier":2,"radius":10,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":3,"price":28000,"ammo":100,
     "damage":1,"fire_rate":6,"angle":120,"n":5,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"]*0.65,"color":"purple"},
    
    {"p_type":"Gun","name":"Plasma BoomOrb","type":"Split","use":"immediate","tier":2,"radius":10,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":3,"price":38000,"ammo":100,
     "damage":1,"fire_rate":6,"angle":60,"n":6,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"]*0.65,"color":"purple"},
    
    {"p_type":"Gun","name":"Plasma ShattOrb T2","type":"Shatter","use":"immediate","tier":3,"radius":10,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":4,"price":42000,"ammo":100,
     "damage":2,"fire_rate":6,"angle":150,"n":7,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"]*0.75,"color":"pink"},
    
    {"p_type":"Gun","name":"Plasma BoomOrb T2","type":"Split","use":"immediate","tier":3,"radius":10,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":4,"price":56000,"ammo":100,
     "damage":2,"fire_rate":6,"angle":60,"n":8,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"]*0.75,"color":"pink"},
    
    {"p_type":"AutoGun","name":"Sentry Gun","type":"Basic","use":"immediate","tier":2,"radius":3,"last_shot":0,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":0,"price":20000,"ammo":250,
     "damage":1,"fire_rate":20,"angle":60,"n":1,"range":settings["projectile_max_distance"]["value"]*1.5,
     "speed":settings["projectile_speed"]["value"],"color":"white"},
    
    {"p_type":"AutoGun","name":"Sentry SMG","type":"Basic","use":"immediate","tier":2,"radius":3,"last_shot":0,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":0,"price":20000,"ammo":500,
     "damage":0.5,"fire_rate":8,"angle":60,"n":1,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"]*1.5,"color":"yellow"},
    
    {"p_type":"AutoGun","name":"Sentry Shotgun","type":"Spread","use":"immediate","tier":2,"radius":3,"last_shot":0,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":0,"price":20000,"ammo":250,
     "damage":0.5,"fire_rate":30,"angle":90,"n":9,"range":settings["projectile_max_distance"]["value"]/2,
     "speed":settings["projectile_speed"]["value"],"color":"green1"},
    
    {"p_type":"AutoGun","name":"Plasma Sentry","type":"Basic","use":"immediate","tier":2,"radius":10,"last_shot":0,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":3,"price":20000,"ammo":250,
     "damage":1,"fire_rate":40,"angle":90,"n":1,"range":settings["projectile_max_distance"]["value"],
     "speed":settings["projectile_speed"]["value"]*0.65,"color":"purple"},
    
    {"p_type":"AutoGun","name":"Bullet Shield Mk1","type":"Spread","use":"immediate","tier":3,"radius":3,"last_shot":0,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":3,"price":20000,"ammo":500,
     "damage":1,"fire_rate":8,"angle":360,"n":16,"range":settings["projectile_max_distance"]["value"]/3,
     "speed":settings["projectile_speed"]["value"],"color":"black"},
    
    {"p_type":"AutoGun","name":"Bullet Shield Mk2","type":"Spread","use":"immediate","tier":4,"radius":3,"last_shot":0,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":3,"price":20000,"ammo":500,
     "damage":1.5,"fire_rate":8,"angle":360,"n":16,"range":settings["projectile_max_distance"]["value"]/2.5,
     "speed":settings["projectile_speed"]["value"],"color":"white"},
]


## Adventure maps ##
## Series of nodes denoting areas of interest ##
adv_maps = [
    [
        {"name":"Homebase","loc":[100,200],"size":40,"faction":"Friendly","features":["Shop"],"mobs":0,"tier":0,
         "locked":False,"unlocks": [[250,200]],"rewards":{}},
        {"name":"Alberta","loc":[250,200],"size":18,"faction":"Hostile","features":[],"mobs":55,"tier":1,
         "locked":False,"unlocks":[[400,200]],"rewards":{"cash":500}},
        {"name":"Bretonia","loc":[400,200],"size":18,"faction":"Hostile","features":[],"mobs":75,"tier":1,
         "locked":True,"unlocks":[[450,450],[550,250]],"rewards":{"cash":1000}},
        {"name":"Cartesia","loc":[550,250],"size":18,"faction":"Hostile","features":[],"mobs":90,"tier":1,
         "locked":True,"unlocks":[[650,450]],"rewards":{"cash":1500}},
        {"name":"Charleston","loc":[450,450],"size":18,"faction":"Hostile","features":[],"mobs":100,"tier":1,
         "locked":True,"unlocks":[[650,450]],"rewards":{"cash":1750}},
        {"name":"Dixie","loc":[650,450],"size":18,"faction":"Hostile","features":[],"mobs":120,"tier":1,
         "locked":True,"unlocks":[[850,450]],"rewards":{"cash":2500}},
        {"name":"Eucharist","loc":[850,450],"size":24,"faction":"Hostile","features":[],"mobs":150,"tier":1,
         "locked":True,"unlocks":[[900,350],[900,550],[800,600]],"rewards":{"cash":2500}},
        {"name":"Freginald","loc":[900,350],"size":18,"faction":"Hostile","features":[],"mobs":150,"tier":1,
         "locked":True,"unlocks":[[700,150]],"rewards":{"cash":2500}},
        {"name":"Frankinston","loc":[900,550],"size":18,"faction":"Hostile","features":[],"mobs":150,"tier":1,
         "locked":True,"unlocks":[[1000,700]],"rewards":{"cash":2500}},
        {"name":"Flippin","loc":[800,600],"size":18,"faction":"Hostile","features":[],"mobs":150,"tier":1,
         "locked":True,"unlocks":[],"rewards":{"cash":2500}},
        {"name":"Grok","loc":[700,150],"size":18,"faction":"Hostile","features":[],"mobs":200,"tier":1,
         "locked":True,"unlocks":[],"rewards":{"cash":3500}},
        {"name":"Gardenton","loc":[1000,700],"size":18,"faction":"Hostile","features":[],"mobs":200,"tier":1,
         "locked":True,"unlocks":[[1100,500]],"rewards":{"cash":3500}},
        {"name":"Hereland","loc":[1100,500],"size":18,"faction":"Hostile","features":[],"mobs":240,"tier":1,
         "locked":True,"unlocks":[[1250,650]],"rewards":{"cash":4200}},
        {"name":"Istaria","loc":[1250,650],"size":24,"faction":"Hostile","features":[],"mobs":280,"tier":1,
         "locked":True,"unlocks":[[1150,450],[1400,750],[1450,350],[1200,800]],"rewards":{"cash":4800}},
        {"name":"Julian","loc":[1150,450],"size":18,"faction":"Hostile","features":[],"mobs":320,"tier":1,
         "locked":True,"unlocks":[],"rewards":{"cash":5200}},
        {"name":"Joshua Tea","loc":[1450,350],"size":18,"faction":"Hostile","features":[],"mobs":320,"tier":1,
         "locked":True,"unlocks":[],"rewards":{"cash":5200}},
        {"name":"Jonestown","loc":[1200,800],"size":18,"faction":"Hostile","features":[],"mobs":320,"tier":1,
         "locked":True,"unlocks":[],"rewards":{"cash":5200}},
        {"name":"Joburg","loc":[1400,750],"size":18,"faction":"Hostile","features":[],"mobs":320,"tier":1,
         "locked":True,"unlocks":[[1600,400]],"rewards":{"cash":5200}},
        {"name":"Kettenburg","loc":[1600,400],"size":32,"faction":"Hostile","features":["Portal to map 1"],
         "mobs":360,"tier":1,"locked":True,"unlocks":[],"rewards":{"cash":6000}},
    ]
]

adv_map = adv_maps[0]



def clear():
    _ = os.system('clear')
    
    
def load_high_scores():
    with open ("high_scores.json","r") as score_data:
        high_scores = json.load(score_data)
    return(high_scores)


def save_high_scores():
    with open("high_scores.json","w") as json_file:
        json.dump(high_scores, json_file)
    
    
def set_xset():
    os.system('xset r rate {}'.format(settings["xset_default"]["value"]))
    
    
def reset_xset():
    os.system('xset r rate')
    
    
def calculate_top_boundary():
    settings["top_boundary"]["value"] = int(settings["window_y"]["value"] / 10)
    
    
def get_screen_size():
    m = get_monitors()
    return(m[0].width,m[0].height)
    
    
def collect_screen_info():
    print("Monitor info:")
    try:
        for m in get_monitors():
            print(m)
        settings["window_x"]["value"] = int(m.width)
        settings["window_y"]["value"] = int(m.height - 100)
    except:
        print("Could not gather screen info! Using default 1280x960")

    
def open_window():
    win = GraphWin("Shooter",settings["window_x"]["value"],settings["window_y"]["value"],autoflush=False)
    win.setBackground(settings["bg_color"]["value"])
    win.update()
    return(win)
    
    
def draw_hero(win,hero):
    to_draw = []
    centerX,centerY = settings["window_x"]["value"]/2,settings["window_y"]["value"]/2
    hero["graphics"] = Circle(Point(centerX,centerY), settings["hero_size"]["value"])
    to_draw.append(hero["graphics"])
    hero["graphics"].setFill(settings["hero_color"]["value"])
    hero["graphics"].setOutline("black")
    hero["graphics"].setWidth(2)
    hero = draw_reticule(win,hero,centerX,centerY)
    return(hero)


def draw_reticule(win,hero,centerX,centerY):
    to_draw = []
    max_dist = settings["projectile_max_distance"]["value"]/2
    end_x,end_y = calculate_end_point(hero["direction"],max_dist,centerX,centerY)
    
    hero["reticule"] = Point(end_x,end_y)
    hero["reticule"].setFill(settings["hero_color"]["value"])
    to_draw.append(hero["reticule"])
    draw_to_draw(win,to_draw)
    return(hero)
        

def move_hero(win,hero):
    if check_hero_border(win,hero):
        move_x,move_y = calculate_move_xy(hero["direction"],hero["speed"])
        hero["graphics"].move(move_x,move_y)
    hero = move_reticule(win,hero)
    return(hero)


def move_reticule(win,hero):
    hero["reticule"].undraw()
    centerX,centerY = get_object_xy(hero)
    hero = draw_reticule(win,hero,centerX,centerY)
    return(hero)


def build_hero(win):
    hero = {}
    hero["cash"] = 500
    hero["direction"] = 0
    hero["health"] = 3
    hero["damage"] = 1
    hero["fire_rate"] = 20
    max_dist = settings["projectile_max_distance"]["value"]*2
    p_speed = settings["projectile_speed"]["value"]
    hero["guns"] = [{"name":"Basic Pistol","type":"Basic","damage": 1,"ammo":100000,"radius":3,
                     "fire_rate":20,"range":max_dist,"n":1,"passthru":0,"price":0,"speed":p_speed}]
    hero["gun"] = hero["guns"][0]
    hero["color"] = settings["hero_color"]["value"]
    hero["animation"] = []
    hero["tangible"] = True
    hero["boosts"] = []
    hero["speed"] = settings["hero_speed"]["value"]
    hero["base_speed"] = hero["speed"]
    hero = draw_hero(win,hero)
    return(hero)


def spawn_controller(win,mobs,max_mobs,score):
    mobs_current = 0
    for mob in mobs:
        mobs_current += 1
    if score < 0:
        temp_score = 0
    else:
        temp_score = score
    if mobs_current < max_mobs+(temp_score/25):
        mob = spawn_mob(win,score)
        mobs.append(mob)
    return(mobs)
    

def spawn_mob(win,score):
    to_draw = []
    mob = {}
    move_factor = 0
    border_width = 5
    if score >= 0:
        move_factor = score / 100
    
    big_roll = random.randrange(0,50) + score
    if big_roll >= 800:
        mob["health"] = 12
        mob["damage"] = 2
        mob["score"] = 24
        mob["index"] = 7
        mob["color"] = settings["mob_color"]["value"][7]
        mob["size"] = round(settings["mob_size"]["value"]*4.2)
        mob["speed"] = round(settings["mob_speed"]["value"]*0.8,1)
    elif big_roll >= 600:
        mob["health"] = 6
        mob["damage"] = 1
        mob["score"] = 12
        mob["index"] = 6
        mob["color"] = settings["mob_color"]["value"][6]
        mob["size"] = round(settings["mob_size"]["value"]*1.6)
        mob["speed"] = round(settings["mob_speed"]["value"]*1.5,1)
    elif big_roll >= 450:
        mob["health"] = 6
        mob["damage"] = 1
        mob["score"] = 12
        mob["index"] = 5
        mob["color"] = settings["mob_color"]["value"][5]
        mob["size"] = round(settings["mob_size"]["value"]*3.6)
        mob["speed"] = round(settings["mob_speed"]["value"]*1.1,1)
    elif big_roll >= 300:
        mob["health"] = 3
        mob["damage"] = 1
        mob["score"] = 6
        mob["index"] = 4
        mob["color"] = settings["mob_color"]["value"][4]
        mob["size"] = round(settings["mob_size"]["value"]*1.8)
        mob["speed"] = round(settings["mob_speed"]["value"]*1.25,1)
    elif big_roll >= 200:
        mob["health"] = 4
        mob["damage"] = 1
        mob["score"] = 8
        mob["index"] = 3
        mob["color"] = settings["mob_color"]["value"][3]
        mob["size"] = round(settings["mob_size"]["value"]*3)
        mob["speed"] = round(settings["mob_speed"]["value"]/1.5,1)
    elif big_roll >= 100:
        mob["health"] = 2
        mob["damage"] = 1
        mob["score"] = 4
        mob["index"] = 2
        mob["color"] = settings["mob_color"]["value"][2]
        mob["size"] = settings["mob_size"]["value"]
        mob["speed"] = settings["mob_speed"]["value"]
    elif big_roll >= 50:
        mob["health"] = 2
        mob["damage"] = 1
        mob["score"] = 4
        mob["index"] = 1
        mob["color"] = settings["mob_color"]["value"][1]
        mob["size"] = settings["mob_size"]["value"]*2
        mob["speed"] = round(settings["mob_speed"]["value"]/2,1)
    elif big_roll >= -500:
        mob["health"] = 1
        mob["damage"] = 1
        mob["score"] = 2
        mob["index"] = 0
        mob["color"] = settings["mob_color"]["value"][0]
        mob["size"] = settings["mob_size"]["value"]
        mob["speed"] = settings["mob_speed"]["value"]
    else:
        mob["health"] = 1
        mob["damage"] = 10
        mob["score"] = 2
        mob["index"] = 0
        mob["color"] = settings["mob_color"]["value"][0]
        mob["size"] = round(settings["mob_size"]["value"]/5)
        mob["speed"] = settings["hero_speed"]["value"]
        
    mob["speed"] += move_factor
    mob["direction"] = random.randrange(0,360)
    mob["animation"] = []
    #move_type_choices = ["random","approach_hero"]
    #mob["move_type"] = random.choice(move_type_choices)
    mob["move_type"] = "approach_hero"
    mob["delete"] = False
    mob["tangible"] = True
    mob["radius"] = mob["size"] + border_width
    
    spawn_side = random.choice(["top","bottom","left","right"])
    border_gap = mob["radius"] + settings["extra_radius"]["value"]
    if spawn_side == "top":
        #print("Mob radius: {}\n top_boundary: {}\n window_x: {}\n border_gap: {}".format(
        #    mob["radius"],settings["top_boundary"]["value"],settings["window_x"]["value"],border_gap))
        centerX = random.randrange(
            mob["radius"]+settings["top_boundary"]["value"],settings["window_x"]["value"]-border_gap)
        centerY = border_gap+settings["top_boundary"]["value"]
        #print("Spawning mob at top at {}x{}".format(centerX,centerY))
    elif spawn_side == "bottom":
        centerX = random.randrange(mob["radius"]+border_gap,settings["window_x"]["value"]-border_gap)
        centerY = settings["window_y"]["value"]-border_gap
        #print("Spawning mob at bottom at {}x{}".format(centerX,centerY))
    elif spawn_side == "left":
        centerX = border_gap
        centerY = random.randrange(mob["radius"]+border_gap,settings["window_y"]["value"]-border_gap)
        #print("Spawning mob at left at {}x{}".format(centerX,centerY))
    elif spawn_side == "right":
        centerX = settings["window_x"]["value"]-border_gap
        centerY = random.randrange(mob["radius"]+border_gap,settings["window_y"]["value"]-border_gap)
        #print("Spawning mob at right at {}x{}".format(centerX,centerY))
    
    mob["graphics"] = Circle(Point(centerX,centerY), mob["size"])
    mob["graphics"].setFill(mob["color"])
    mob["graphics"].setOutline("red")
    mob["graphics"].setWidth(border_width)
    to_draw.append(mob["graphics"])
    draw_to_draw(win,to_draw)
    #print("Spawned\n")
    return(mob)
    
    
def draw_to_draw(win,to_draw):
    for item in to_draw:
        item.draw(win)
    win.update()


def switch_weapons(char):
    if len(char["guns"]) > 1:
        next_index = 0
        max_index = len(char["guns"]) - 1
        for i in range(0,len(char["guns"])):
            if char["gun"]["name"] == char["guns"][i]["name"]:
                if i == max_index:
                    next_index = 0
                else:
                    next_index = i + 1
        char["gun"] = char["guns"][next_index]
        #char["damage"] = set_damage(char)
        #char["fire_rate"] = char["gun"]["fire_rate"]
        char = set_hero_gun_settings(char,char["gun"])
    return(char)


def check_hero_ammo(hero):
    guns_copy = hero["guns"].copy()
    for gun in hero["guns"]:
        #print(gun)
        if gun["ammo"] <= 0:
            if gun["name"] != "Basic Pistol":
                guns_copy.remove(gun)
                hero["guns"] = guns_copy
                hero = switch_weapons(hero)
                
            else:
                gun["ammo"] = 10000
    return(hero)
        
        
def set_damage(char):
    return(char["gun"]["damage"])


def dir_to_nearest_mob(win,char,mobs):
    distance = 10000
    nearest_mob = None
    direction = 0
    for mob in mobs:
        new_distance = distance_between_objects(char,mob)
        if new_distance < distance:
            distance = new_distance
            nearest_mob = mob
            
    if nearest_mob != None:        
        #print(mob)
        direction = direction_between_points(
            char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY(),
            nearest_mob["graphics"].getCenter().getX(),nearest_mob["graphics"].getCenter().getY())
            
    return(direction,distance)
    
    
def fire_auto_projectile(win,char,autogun,mobs):
    projectiles = []
    if autogun["ammo"] > 0:
        radius = autogun["radius"]
        aim_dir,distance = dir_to_nearest_mob(win,char,mobs)
        max_dist = autogun["range"]

        if distance < (max_dist/2):
            autogun["ammo"] -= 1
            passthru = autogun["passthru"]
            char_dir = char["direction"]
            o = ""
            ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
            
            if autogun["type"] == "Basic":
                ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
                projectiles = [spawn_projectile(win,char,ox,oy,radius,passthru,aim_dir,autogun["damage"],max_dist,o,
                                               autogun["speed"])]

            elif autogun["type"] == "Spread":
                number = autogun["n"]
                angle = autogun["angle"]
                angles = calc_angles_from_max(number,angle)
                ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
                projectiles = []
                for i in range(number):
                    projectile = spawn_projectile(
                        win,char,ox,oy,radius,passthru,aim_dir+angles[i],autogun["damage"],max_dist,o,autogun["speed"])
                    projectiles.append(projectile)
                    
    return(projectiles)
    

def fire_projectile(win,char):
    #print(char["gun"])
    radius = char["gun"]["radius"] #settings["projectile_size"]["value"]
    char["gun"]["ammo"] -= 1
    #passthru = False
    passthru = char["gun"]["passthru"]
    char_dir = char["direction"]
    o = ""
    max_dist = char["gun"]["range"]
    #max_dist = settings["projectile_max_distance"]["value"]
    
    if char["gun"]["type"] == "Basic":
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o,
                                       char["gun"]["speed"])]
        
    elif char["gun"]["type"] == "Spread":
        number = char["gun"]["n"]
        angle = char["gun"]["angle"]
        angles = calc_angles_from_max(number,angle)
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = []
        for i in range(number):
            projectile = spawn_projectile(
                win,char,ox,oy,radius,passthru,char_dir+angles[i],char["damage"],max_dist,o,char["gun"]["speed"])
            projectiles.append(projectile)
            
    elif char["gun"]["type"] == "Wide":
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        if char["direction"] == 0 or char["direction"] == 180:
            ox2 = ox - 25
            ox3 = ox + 25
            oy2,oy3 = oy,oy
        elif char["direction"] == 90 or char["direction"] == 270:
            oy2 = oy - 25
            oy3 = oy + 25
            ox2,ox3 = ox,ox
        elif char["direction"] > 270 or char["direction"] < 90:
            ox2 = ox - 25
            ox3 = ox + 25
            oy2,oy3 = oy,oy
        else:
            oy2 = oy - 25
            oy3 = oy + 25
            ox2,ox3 = ox,ox
        projectile1 = spawn_projectile(
            win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o,char["gun"]["speed"])
        projectile2 = spawn_projectile(
            win,char,ox2,oy2,radius,passthru,char_dir,char["damage"],max_dist,o,char["gun"]["speed"])
        projectile3 = spawn_projectile(
            win,char,ox3,oy3,radius,passthru,char_dir,char["damage"],max_dist,o,char["gun"]["speed"])
        projectiles = [projectile1,projectile2,projectile3]
        
    elif char["gun"]["type"] == "Big":
        radius = settings["projectile_size"]["value"]*3
        passthru = True
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(
            win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o,char["gun"]["speed"])]
    
    elif char["gun"]["type"] == "Split":
        o = [{"type":"split","delay":0,"projectiles":char["gun"]["n"],"recursion":0}]
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(
            win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o,char["gun"]["speed"])]
    
    elif char["gun"]["type"] == "Split (Recursive 1)":
        o = [{"type":"split","delay":0,"projectiles":char["gun"]["n"],"recursion":1}]
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(
            win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o,char["gun"]["speed"])]
    
    elif char["gun"]["type"] == "Shatter":
        o = [{"type":"shatter","delay":0,"projectiles":char["gun"]["n"],"max_angle":char["gun"]["angle"],"recursion":0}]
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(
            win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o,char["gun"]["speed"])]
    
    elif char["gun"]["type"] == "Split Shatter":
        o = [{"type":"shatter","delay":0,"projectiles":char["gun"]["n"],"max_angle":char["gun"]["angle"],"recursion":0},
            {"type":"split","delay":0,"projectiles":char["gun"]["n"],"recursion":0}]
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(
            win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o,char["gun"]["speed"])]
    
    elif char["gun"]["type"] == "Split > Shatter":
        o = [{"type":"shatter","delay":1,"projectiles":char["gun"]["n"],"max_angle":char["gun"]["angle"],"recursion":0},
            {"type":"split","delay":0,"projectiles":char["gun"]["n"],"recursion":0}]
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(
            win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o,char["gun"]["speed"])]
        
    return(projectiles)
    
    
def spawn_projectile(win,origin,origin_x,origin_y,radius,passthru,direction,damage,max_dist,other,speed):
    to_draw = []
    projectile = {}
    #origin_x, origin_y = origin["graphics"].getCenter().getX(),origin["graphics"].getCenter().getY()
    projectile["graphics"] = Circle(Point(origin_x,origin_y), radius)
    projectile["graphics"].setFill(settings["hero_color"]["value"])
    projectile["origin_x"],projectile["origin_y"] = origin_x,origin_y
    projectile["direction"] = direction
    projectile["damage"] = damage
    projectile["speed"] = speed
    projectile["dir_x"],projectile["dir_y"] = calc_projectile_direction(projectile)
    projectile["origin"] = origin
    projectile["passthru"] = passthru
    projectile["max_distance"] = max_dist
    projectile["distance"] = 0
    projectile["other"] = other
    to_draw.append(projectile["graphics"])
    draw_to_draw(win,to_draw)
    return(projectile)


def move_projectiles(win,projectiles):
    for projectile in projectiles:
        if projectile != None:
            ## Move the item on-screen ##
            projectile["graphics"].move(projectile["dir_x"],projectile["dir_y"])
            projectile["distance"] += (abs(projectile["dir_x"])+abs(projectile["dir_y"]))
            ## Check if item has gone beyond playfield bounds ##
            if check_projectile_deletion(win,projectile) or (projectile["distance"] >= projectile["max_distance"]):
                projectile["graphics"].undraw()
                projectiles.remove(projectile)
                if settings["debug_mode"]["value"]:
                    print("Projectile deleted")
    return(projectiles)


def calc_projectile_direction(projectile):
    direction = projectile["direction"]
    origin_x,origin_y = projectile["graphics"].getCenter().getX(),projectile["graphics"].getCenter().getY()
    move_x,move_y = calculate_move_xy(direction,projectile["speed"])
    return(move_x,move_y)
                                        
    
def check_projectile_deletion(win,projectile):
    centerX,centerY=projectile["graphics"].getCenter().getX(),projectile["graphics"].getCenter().getY()
    if (centerX > settings["window_x"]["value"] or centerX < 0) or (centerY > settings["window_y"]["value"] or centerY < settings["top_boundary"]["value"]):
        #print("{} went beyond map bounds: deleting".format(projectile))
        return(True)
    return(False)


def distance_between_objects(obj1,obj2):
    o1x,o1y = obj1["graphics"].getCenter().getX(),obj1["graphics"].getCenter().getY()
    o1r = obj1["graphics"].getRadius()
    o2x,o2y = obj2["graphics"].getCenter().getX(),obj2["graphics"].getCenter().getY()
    o2r = obj2["graphics"].getRadius()
    dx = math.pow((o1x - o2x),2)
    dy = math.pow((o1y - o2y),2)
    distance = (math.sqrt(dx + dy))
    return(distance)


def check_projectile_hit(projectile,mobs):
    proj_x,proj_y = projectile["graphics"].getCenter().getX(),projectile["graphics"].getCenter().getY()
    proj_r = projectile["graphics"].getRadius()
    for mob in mobs:
        if mob["tangible"]:
            mob_x,mob_y = mob["graphics"].getCenter().getX(),mob["graphics"].getCenter().getY()
            mob_r = mob["radius"]
            dx = math.pow((proj_x - mob_x),2)
            dy = math.pow((proj_y - mob_y),2)
            distance = (math.sqrt(dx + dy))
            max_hit_dist = mob_r + proj_r
            if distance <= (mob_r + proj_r):
                return([mob,projectile])
    return(None)

## Currently checking every projectile against every mob each frame ##
## This creates lag when large amounts of projectiles exist ##
def check_for_projectile_hits(win,projectiles,mobs):
    hit_mob = ""
    for projectile in projectiles:
        if projectile != None:
            hit = check_projectile_hit(projectile,mobs)
            if hit != None:
                ## Flash hit mob, remove health ##
                mob_copy = hit[0].copy()
                hit[0]["health"] -= hit[1]["damage"]
                flash_mob(hit[0])
                ## Slow down mob slightly ##
                hit[0]["speed"] = hit[0]["speed"] * 0.9
                
                ## Undraw and cull projectile ##
                if projectile["passthru"] <= 0:
                    hit[1]["graphics"].undraw()
                    projectiles.remove(hit[1])
                else:
                    projectile["passthru"] -= 1
                    
                ## Check the 'other' for special projectile instruction strings ##
                #print(hit[1]["other"])
                for instruction in hit[1]["other"]:
                    #print(instruction)
                    if instruction["delay"] > 0:
                        instruction["delay"] -= 1
                        #print(instruction)
                    else:
                        if instruction["type"] == "split":
                            i_copy = instruction.copy()
                            if instruction["recursion"] > 0:
                                recursion = instruction["recursion"] - 1
                                instruction = {
                                    "type":"split","projectiles":projectile["other"][0]["projectiles"],
                                    "recursion":recursion,"delay":0}
                            else:
                                instruction = {"type":"none","recursion":0,"delay":0}
                            o = []
                            if len(hit[1]["other"]) > 1:
                                for i in hit[1]["other"]:
                                    if i != i_copy:
                                        #o.append(instruction)
                                        o.append(i)
                            o.append(instruction)
                            radius = hit[1]["graphics"].getRadius()
                            offset = hit[0]["radius"] + settings["extra_radius"]["value"]
                            passthru = hit[1]["passthru"]
                            max_dist = round(hit[1]["max_distance"]*0.75)
                            if settings["debug_mode"]["value"]:
                                print(instruction)
                                print(hit[1])
                            ox,oy = hit[0]["graphics"].getCenter().getX(),hit[0]["graphics"].getCenter().getY()
                            
                            projectile_list = []
                            #print(projectile)
                            #print(projectile.keys())
                            for i in range(0,360,int(360/projectile["other"][0]["projectiles"])):
                                projectile_list.append(spawn_projectile(
                                    win,hit[1],ox,oy-offset,radius,passthru,i,hit[1]["damage"],
                                    max_dist,o,projectile["speed"]))
                            
                            for p in projectile_list:
                                projectiles.append(p)
                                
                        if instruction["type"] == "shatter":
                            i_copy = instruction.copy()
                            max_angle = projectile["other"][0]["max_angle"]
                            if instruction["recursion"] > 0:
                                recursion = instruction["recursion"] - 1
                                instruction = {
                                    "type":"split","projectiles":projectile["other"][0]["projectiles"],
                                    "recursion":recursion,"max_angle":max_angle,"delay":0,"speed":projectile["speed"]}
                            else:
                                instruction = {"type":"none","recursion":0,"max_angle":max_angle,"delay":0,"speed":0}
                            o = []
                            if len(hit[1]["other"]) > 1:
                                for i in hit[1]["other"]:
                                    if i != i_copy:
                                        #o.append(instruction)
                                        o.append(i)
                            o.append(instruction)
                            radius = hit[1]["graphics"].getRadius()
                            offset=hit[0]["radius"] + settings["extra_radius"]["value"]
                            passthru = hit[1]["passthru"]
                            max_dist = round(hit[1]["max_distance"]*0.75)
                            if settings["debug_mode"]["value"]:
                                print(instruction)
                                print(hit[1])
                            ndir1 = hit[1]["direction"]
                            ndir2 = hit[1]["direction"] + (instruction["max_angle"]/2)
                            ndir3 = hit[1]["direction"] - (instruction["max_angle"]/2)
                            ox,oy = hit[0]["graphics"].getCenter().getX(),hit[0]["graphics"].getCenter().getY()
                            ox1,oy1 = calculate_end_point(ndir1,offset,ox,oy)
                            ox2,oy2 = calculate_end_point(ndir2,offset,ox,oy)
                            ox3,oy3 = calculate_end_point(ndir3,offset,ox,oy)
                            
                            projectile_list = []
                            for i in range(int(ndir3),int(ndir2)+1,int(max_angle/projectile["other"][0]["projectiles"])):
                                projectile_list.append(spawn_projectile(
                                    win,hit[1],ox,oy-offset,radius,passthru,i,hit[1]["damage"],
                                    max_dist,o,projectile["speed"]))
                            
                            for p in projectile_list:
                                projectiles.append(p)
                    
                    
                ## If mob health has dropped to 0 or less ##
                ## Add animation info to the mob itself ##
                ## And return the list of mobs ##
                if hit[0]["health"] <= 0:
                    ## MOB INHERITS DIRECTION/SPEED FROM PROJECTILE ##
                    hit[0]["direction"],hit[0]["speed"] = hit[1]["direction"],hit[1]["speed"]/2
                    #hit[0]["direction"] = opposite_direction(hit[0]["direction"])
                    death_options = ["explode","pop"]
                    choice = random.choice(death_options)
                    if choice == "explode":
                        hit[0] = explode_mob(win,hit[0])
                    elif choice == "pop":
                        hit[0] = pop_mob(win,hit[0])
                    #mobs.remove(hit[0])
    return(projectiles,mobs)


def calc_angles_from_max(number,angle):
    between = int(angle / (number-1))
    max_angle = int(angle / 2)
    angle_list = []
    for i in range(-max_angle,max_angle+1,between):
        angle_list.append(i)
    return(angle_list)


def redraw_item_group(win,group):
    for item in group:
        item["graphics"].undraw()
        item["graphics"].draw(win)

    
def flash_mob(mob):
    mob["animation"] = (
        {"instruction": "flash","tick":0,"flash_ticks":1,"flash_color":"white","start_color":mob["color"]})
    if settings["debug_mode"]["value"]:
        print(mob)
    return(mob)

    
def i_flash_mob(mob):
    mob["animation"] = (
        {"instruction": "flash","tick":0,"flash_ticks":20,"flash_on":True,
         "flash_color":"white","start_color":mob["color"]})
    if settings["debug_mode"]["value"]:
        print(mob)
    return(mob)


def screen_flash(mob):
    mob["animation"] = (
        {"instruction": "screen_flash","tick":0,"flash_ticks":20,"flash_on":True,
         "flash_color":"white","start_color":mob["color"]})
    if settings["debug_mode"]["value"]:
        print(mob)
    return(mob)

    
def explode_mob(win,mob):
    mob["tangible"] = False
    start_size = mob["graphics"].getRadius()
    size = start_size
    max_size = start_size * 3
    mob["animation"] = ({"instruction": "explode","step_value":2,"start_value":size,"max_value":max_size})
    if settings["debug_mode"]["value"]:
        print(mob)
    return(mob)
    
    
def pop_mob(win,mob):
    mob["tangible"] = False
    start_size = mob["graphics"].getRadius()
    size = start_size
    max_size = start_size * 3
    mob["animation"] = ({"instruction": "pop","step_value":3,"start_value":size,"max_value":max_size})
    if settings["debug_mode"]["value"]:
        print(mob)
    return(mob)
    
    
def animation_queue(win,items):
    ## Iterate through all items in queue ##
    for item in items:
        ## Make sure that the item has animation in its personal queue ##
        if len(item["animation"]) > 0:
            if settings["debug_mode"]["value"]:
                print(item)
            ## Different instructions call for different animations ##
            instruction = item["animation"]["instruction"]
            
            #### EXPLODE, POP ####
            if instruction == "explode" or instruction == "pop":
                item["size"] = item["graphics"].getRadius()
                #item["graphics"].undraw()
                ## For explode, increase item size by step_value per tick until it reaches max value ##
                if item["size"] < item["animation"]["max_value"]:
                    if instruction == "pop":
                        item["speed"] = 0
                    item["graphics"].undraw()
                    item["size"] += item["animation"]["step_value"]
                    size = item["size"]

                    item["graphics"] = Circle(
                        Point(item["graphics"].getCenter().getX(),item["graphics"].getCenter().getY()),size)
                    item_id = item["index"]
                    item["graphics"].setFill(settings["mob_splat_color"]["value"][item_id])
                    #if instruction == "explode":
                    #    item["graphics"].setOutline(settings["mob_splat_color"]["value"][item_id])
                    #elif instruction == "pop":
                        #item["graphics"].setOutline(item["color"])
                    item["graphics"].setOutline(item["color"])
                    item["graphics"].draw(win)
                
                ## Once it has reached full size, remove it from items to help iteration speed ##
                if item["size"] >= item["animation"]["max_value"]:
                    item["delete"] = True
                    item["graphics"].setOutline(settings["mob_splat_color"]["value"][item_id])
                    item["graphics"].undraw()
                    #if instruction == "pop":
                        #pass
                        #item["graphics"].undraw()
                        
            #### FLASH ####
            elif instruction == "flash":
                if item["animation"]["tick"] >= item["animation"]["flash_ticks"]:
                    item["graphics"].setFill(item["animation"]["start_color"])
                    item["animation"] = {}
                else:
                    item["graphics"].setFill(item["animation"]["flash_color"])
                    item["animation"]["tick"] += 1
                    
            elif instruction == "i_flash":
                #flash_on = True
                if item["animation"]["tick"] >= item["animation"]["flash_ticks"]:
                    item["graphics"].setFill(item["animation"]["start_color"])
                    item["animation"] = {}
                    item["tangible"] = True
                else:
                    if(item["animation"]["tick"] % 5) == 0:
                        item["animation"]["flash_on"] = switch_bool(item["animation"]["flash_on"])
                if item["animation"]["flash_on"]:
                    item["graphics"].setFill("white")
                    win.setBackground(settings["bg_flash"]["value"])
                else:
                    item["graphics"].setFill(item["color"])
                    win.setBackground(settings["bg_color"]["value"])
                item["animation"]["tick"] += 1
                item["tangible"] = False
            elif instruction == "speed_flash":
                pass
            elif instruction == "screen_flash":
                if item["animation"]["tick"] >= item["animation"]["flash_ticks"]:
                    win.setBackground(settings["bg_flash"]["value"])
                else:
                    win.setBackground(settings["bg_color"]["value"])
                item["animation"]["tick"] += 1
    ## Return the updated queue to be called next frame ##
    return(items)


def text_animation_queue(win,ui,items):
    for item in items:
        instruction = item["instruction"]
        if instruction == "timed_info_text":
            if item["tick"] == 0:
                ui["info_box"]["text"].setText(item["text"])
            if item["tick"] < item["time"]:
                item["tick"] += 1
            elif item["tick"] >= item["time"]:
                ui["info_box"]["text"].setText("")
                items.remove(item)
    return(ui,items)


def timed_info_text(text,time):
    info = {}
    info["instruction"] = "timed_info_text"
    info["text"] = text
    info["time"] = time
    info["tick"] = 0
    return(info)


def get_object_xy(g):
    gx, gy = g["graphics"].getCenter().getX(),g["graphics"].getCenter().getY()
    return(gx,gy)


def check_hero_border(win,hero):
    direction = hero["direction"]
    hero_x, hero_y = get_object_xy(hero)
    
    if direction == 0:
        hero_y = hero_y + settings["hero_speed"]["value"] + settings["hero_size"]["value"]
    elif direction == 90:
        hero_x = hero_x + settings["hero_speed"]["value"] + settings["hero_size"]["value"]
    elif direction == 180:
        hero_y = hero_y - settings["hero_speed"]["value"] - settings["hero_size"]["value"]
    elif direction == 270:
        hero_x = hero_x - settings["hero_speed"]["value"] - settings["hero_size"]["value"]
        
    if (hero_x > settings["window_x"]["value"] or hero_x < 0) or (hero_y > settings["window_y"]["value"] or hero_y < settings["top_boundary"]["value"]):
        return(False)
    return(True)


def check_hero_mob_collisions(win,hero,mobs):
    if hero["tangible"]:
        hero_x, hero_y = get_object_xy(hero)
        for mob in mobs:
            if mob["tangible"]:
                mob_x,mob_y = get_object_xy(mob)
                touch_distance = mob["radius"] + hero["graphics"].getRadius()
                distance = distance_between_objects(hero,mob)
                if distance <= touch_distance:
                    hero = i_flash_mob(hero)
                    #hero = screen_flash(hero)
                    hero["health"] -= mob["damage"]
                    hero["tangible"] = False
    return(hero)


def redraw_graphic(win,graphic):
    graphic.undraw()
    graphic.draw(win)
    return(graphic)


def mob_controller(win,mobs):
    #for mob in mobs:
    pass

    
def mob_approach_hero(mob,hero):
    mob_x,mob_y = mob["graphics"].getCenter().getX(),mob["graphics"].getCenter().getY()
    hero_x,hero_y = hero["graphics"].getCenter().getX(),hero["graphics"].getCenter().getY()
    mob["direction"] = direction_between_points(hero_x,hero_y,mob_x,mob_y)
    mob["direction"] = opposite_direction(mob["direction"])
    return(mob)


def opposite_direction(direction):
    if direction > 180:
        return(direction - 180)
    return(direction + 180)


def move_mobs(win,mobs,hero):
    for mob in mobs:
        if mob["tangible"]:
            if mob["move_type"] == "approach_hero":
                mob = mob_approach_hero(mob,hero)
        #direction = mob["direction"]
        speed = mob["speed"]
        move_x,move_y = calculate_move_xy(mob["direction"],speed)
        mob["graphics"].move(move_x,move_y)
        ## Check if mob has reached border of playfield ##
        ## Uses same function that projectiles use ##
        delete = check_projectile_deletion(win,mob)
        if delete:
            #print("\n\nMob deleted buring def move_mobs\n\n")
            mobs.remove(mob)
            mob["graphics"].undraw()
    return(mobs)


def calculate_move_xy(direction,speed):
    move_x = speed * math.sin(math.radians(direction))
    move_y = speed * math.cos(math.radians(direction))
    return(move_x,move_y)


def calculate_end_point(direction,speed,origin_x,origin_y):
    disp_x,disp_y = calculate_move_xy(direction,speed)
    end_x = origin_x + disp_x
    end_y = origin_y + disp_y
    return(end_x,end_y)
    

def coords_to_direction(x,y):
    return(math.atan2(y,x)/math.pi*180)


def direction_between_points(x1,y1,x2,y2):
    return(math.atan2(x2-x1,y2-y1)/math.pi*180)


def bool_switch(b):
    if b:
        return(False)
    return(True)


def fps_check(win,projectiles,mobs):
    if settings["debug_mode"]["value"]:
        print("{} Projectiles\n{} Mobs".format(str(len(projectiles)),str(len(mobs))))
        
        
def build_ui(win):
    ## [fps_box][count_box][         info_box         ][wpn_box][score_box] ##
    ## [fps_box][count_box][     info_box     ][hp_box][wpn_box][score_box] ##
    ui = {}
    to_draw = []
    
    fps_box = {}
    fps_box_x,fps_box_y = settings["window_x"]["value"]/10,settings["window_y"]["value"]/10
    fps_box_P1 = [0,0]
    fps_box_P2 = [fps_box_x,fps_box_y]
    fps_box = build_ui_box(fps_box,fps_box_P1,fps_box_P2)
    to_draw.append(fps_box["box"])
    to_draw.append(fps_box["text"])
    ui["fps_box"] = fps_box
    
    score_box = {}
    score_box_x,score_box_y = settings["window_x"]["value"]/10,settings["window_y"]["value"]/10
    score_box_P1 = [settings["window_x"]["value"],0]
    score_box_P2 = [settings["window_x"]["value"]*0.9,settings["window_y"]["value"]/10]
    score_box = build_ui_box(score_box,score_box_P1,score_box_P2)
    score_box["text"].setSize(20)
    to_draw.append(score_box["box"])
    to_draw.append(score_box["text"])
    ui["score_box"] = score_box
    
    weapon_box = {}
    weapon_box_x,weapon_box_y = settings["window_x"]["value"]*0.15,settings["window_y"]["value"]/10
    weapon_box_P1 = [score_box_P2[0],0]
    weapon_box_P2 = [score_box_P2[0]-weapon_box_x,settings["window_y"]["value"]/10]
    weapon_box = build_ui_box(weapon_box,weapon_box_P1,weapon_box_P2)
    weapon_box["text"].setSize(18)
    to_draw.append(weapon_box["box"])
    to_draw.append(weapon_box["text"])
    ui["weapon_box"] = weapon_box
    
    hp_box = {}
    hp_box_x,hp_box_y = settings["window_x"]["value"]*0.1,settings["window_y"]["value"]/10
    hp_box_P1 = [weapon_box_P2[0],0]
    hp_box_P2 = [weapon_box_P2[0]-hp_box_x,settings["window_y"]["value"]/10]
    hp_box = build_ui_box(hp_box,hp_box_P1,hp_box_P2)
    hp_box["text"].setSize(18)
    to_draw.append(hp_box["box"])
    to_draw.append(hp_box["text"])
    ui["hp_box"] = hp_box
    
    count_box = {}
    count_box_x,count_box_y = settings["window_x"]["value"]*0.1,settings["window_y"]["value"]/10
    count_box_P1 = [fps_box_P2[0],0]
    count_box_P2 = [fps_box_P2[0]+count_box_x,settings["window_y"]["value"]/10]
    count_box = build_ui_box(count_box,count_box_P1,count_box_P2)
    count_box["text"].setSize(14)
    to_draw.append(count_box["box"])
    to_draw.append(count_box["text"])
    ui["count_box"] = count_box
    
    info_box = {}
    info_box_x,score_box_y = settings["window_x"]["value"]*0.8,settings["window_y"]["value"]/10
    info_box_P1 = [hp_box_P2[0],0]
    info_box_P2 = [count_box_P2[0],settings["window_y"]["value"]/10]
    info_box = build_ui_box(info_box,info_box_P1,info_box_P2)
    info_box["text"].setSize(24)
    to_draw.append(info_box["box"])
    to_draw.append(info_box["text"])
    ui["info_box"] = info_box
    
    
    draw_to_draw(win,to_draw)
    return(ui)


def build_ui_box(ui_box,ui_box_P1,ui_box_P2):
    ui_box_center = [(ui_box_P1[0] + ui_box_P2[0]) / 2,(ui_box_P1[1] + ui_box_P2[1]) / 2]
    ui_box["type"] = ""
    ui_box["box"] = Rectangle(
        Point(ui_box_P1[0],ui_box_P1[1]),Point(ui_box_P2[0],ui_box_P2[1]))
    ui_box["box"].setFill(settings["bg_color"]["value"])
    ui_box["box"].setOutline(settings["fg_color"]["value"])
    ui_box["text"] = Text(Point(ui_box_center[0],ui_box_center[1]),"")
    ui_box["text"].setTextColor(settings["fg_color"]["value"])
    return(ui_box)


def build_dbl_ui_box(ui_box,ui_box_P1,ui_box_P2):
    border = 20
    ui_box_center = [(ui_box_P1[0] + ui_box_P2[0]) / 2,(ui_box_P1[1] + ui_box_P2[1]) / 2]
    ui_box1_center = [(ui_box_P1[0] + ui_box_P2[0]) * 0.25,(ui_box_P1[1] + ui_box_P2[1]) / 2]
    ui_box2_center = [(ui_box_P1[0] + ui_box_P2[0]) * 0.75,(ui_box_P1[1] + ui_box_P2[1]) / 2]
    ui_box1_P1x = ui_box_P1[0]
    ui_box1_P1y = ui_box_P1[1]
    ui_box1_P2x = ui_box_center[0] - border
    ui_box1_P2y = ui_box_P2[1]
    ui_box2_P1x = ui_box_center[0] + border
    ui_box2_P1y = ui_box_P1[1]
    ui_box2_P2x = ui_box_P2[0]
    ui_box2_P2y = ui_box_P2[1]
    ui_box["type"] = "dbl"
    ui_box1,ui_box2 = {},{}
    ui_box1["box"] = Rectangle(
        Point(ui_box1_P1x,ui_box1_P1y),Point(ui_box1_P2x,ui_box1_P2y))
    ui_box1["box"].setFill(settings["bg_color"]["value"])
    ui_box1["box"].setOutline(settings["fg_color"]["value"])
    ui_box2["box"] = Rectangle(
        Point(ui_box2_P1x,ui_box2_P1y),Point(ui_box2_P2x,ui_box2_P2y))
    ui_box2["box"].setFill(settings["bg_color"]["value"])
    ui_box2["box"].setOutline(settings["fg_color"]["value"])
    ui_box1["text"] = Text(Point(ui_box1_center[0],ui_box1_center[1]),"")
    ui_box1["text"].setTextColor(settings["fg_color"]["value"])
    ui_box2["text"] = Text(Point(ui_box2_center[0],ui_box2_center[1]),"")
    ui_box2["text"].setTextColor(settings["fg_color"]["value"])
    return(ui_box1,ui_box2)


def build_debug_ui(win):
    debug_ui = Text(
        Point(settings["window_x"]["value"]/2,
              settings["top_boundary"]["value"]+settings["extra_radius"]["value"]*3),"")
    debug_ui.setTextColor(settings["fg_color"]["value"])
    return(debug_ui)


def toggle_debug_ui(win,debug_text):
    if settings["debug_mode"]["value"]:
        debug_text.undraw()
        settings["debug_mode"]["value"] = False
    else:
        debug_text.draw(win)
        settings["debug_mode"]["value"] = True
        
        
def update_debug_ui(win,debug_ui,string):
    #print(debug_ui)
    debug_ui.setText(str(string))
    #return(debug_ui)


def set_weapon_text(win,ui,hero):
    string = "{}\n{}".format(hero["gun"]["name"],str(hero["gun"]["ammo"]))
    ui["weapon_box"]["text"].setText(string)
    return(ui)


def set_info_text(win,ui,string):
    ui["info_box"]["text"].setText(string)
    return(ui)


def redraw_ui(win,ui):
    for item in ui.items():
        for subitem in ["box","text"]:
            item[1][subitem] = redraw_graphic(win,item[1][subitem])
    return(ui)


def shoot_button(win,hero,score,projectiles):
    new_projectiles=fire_projectile(win,hero)
    if settings["debug_mode"]["value"]:
        print(projectiles)
    for projectile in new_projectiles:
        projectiles.append(projectile)
    score -= 1
    return(projectiles,score)


def shoot_autoshot(win,hero,score,projectiles,mobs):
    new_projectiles = []
    for boost in hero["boosts"]:
        if boost["p_type"] == "AutoGun":
            autogun = boost
            np=fire_auto_projectile(win,hero,autogun,mobs)
            for projectile in np:
                new_projectiles.append(projectile)
    if settings["debug_mode"]["value"]:
        print(projectiles)
    for projectile in new_projectiles:
        projectiles.append(projectile)
    score -= 1
    return(projectiles,score)


def low_fps_factor(fps,target_fps):
    return(target_fps/fps)


def return_higher(a,b):
    if a > b:
        return(a)
    return(b)


def pickup_spawn_controller_wave(win,hero,pickups,wave_number,pickup_types):
    ## If there are no pickups active ##
    if len(pickups) == 0:
        ## Make a roll that is increased by score ##
        roll = random.randrange(0,25)
        ## Score determines maximum weapon tier ##
        
        ## If roll is successful ##
        if roll <= 1:
            ## Set a random location in the playfield to spawn the pickup ##
            origin_x = random.randrange(0,settings["window_x"]["value"])
            origin_y = random.randrange(
                settings["top_boundary"]["value"],
                settings["window_y"]["value"])
            pickup = spawn_pickup(origin_x,origin_y,wave_number,pickup_types)
            pickups.append(pickup)
            pickup["graphics"].draw(win)
    return(pickups)


def pickup_spawn_controller(win,hero,pickups,score,pickup_types):
    ## If there are no pickups active ##
    if len(pickups) == 0:
        ## Make a roll that is increased by score ##
        roll = random.randrange(0,200) - score/200
        ## Score determines maximum weapon tier ##
        if score >= 200:
            tier = 2
        else:
            tier = 1
        ## If roll is successful ##
        if roll <= 0:
            ## Set a random location in the playfield to spawn the pickup ##
            origin_x = random.randrange(0,settings["window_x"]["value"])
            origin_y = random.randrange(
                settings["top_boundary"]["value"],
                settings["window_y"]["value"])
            pickup = spawn_pickup(origin_x,origin_y,tier,pickup_types)
            pickups.append(pickup)
            pickup["graphics"].draw(win)
    return(pickups)


def spawn_pickup(origin_x,origin_y,tier,pickup_types):
    roll = random.randrange(0,100)
    max_dist = settings["projectile_max_distance"]["value"]
    if roll >= 75:
        pickup = {"p_type":"Health","name":"HP+1","use":"immediate","value":1,
                  "decay_time":300,"decay":0,"hit_box":20,"border":5}
        fill,outline = "red","cyan"
    elif roll >= 50:
        typeroll = random.randrange(0,2)
        if typeroll == 1:
            pickup = {"p_type":"Speed","name":"Speed Boost","use":"temp","value":[600,1],
                      "decay_time":300,"decay":0,"hit_box":20,"border":5}
        else:
            pickup = {"p_type":"Speed","name":"Speed Boost","use":"perm","value":0.1,
                      "decay_time":300,"decay":0,"hit_box":20,"border":5}
        fill,outline = "yellow2","cyan"
        
    else:
        if "guns" in pickup_types:
            gun_choices = []
            fill,outline = "green2","cyan"
            max_roll = 100
            gun_roll = random.randrange(0,max_roll)

            for gun in all_guns:
                if gun["tier"] <= tier:
                    gun_choices.append(gun)

            pickup = random.choice(gun_choices)
            pickup["p_radius"] = pickup["radius"]
            pickup["hit_box"] = 15
            pickup["border"] = 5
        elif "cash" in pickup_types:
            cash_amount = random.randrange(100+(tier*100),1001+(tier*100),100)
            pickup = {"p_type":"Cash","name":"Cash","use":"immediate","value":1,"cash":cash_amount,
                      "decay_time":600,"decay":0,"hit_box":15,"border":5}
            fill,outline = "blue","cyan"

    pickup["radius"] = pickup["hit_box"]+pickup["border"]
    
    origin_x = random.randrange(
        pickup["radius"]+settings["extra_radius"]["value"],
        settings["window_x"]["value"]-(pickup["radius"]+settings["extra_radius"]["value"]))
    origin_y = random.randrange(
        pickup["radius"]+settings["extra_radius"]["value"]+settings["top_boundary"]["value"],
        settings["window_y"]["value"]-(pickup["radius"]+settings["extra_radius"]["value"]))
            
    pickup["graphics"] = Circle(Point(origin_x,origin_y),pickup["hit_box"])
    pickup["graphics"].setFill(fill)
    pickup["graphics"].setOutline(outline)
    pickup["graphics"].setWidth(pickup["border"])
    pickup["decay"] = 0
    #print("New pickup: {}".format(pickup))
    return(pickup)


def check_pickup_collision(win,hero,pickups):
    info_string = ""
    pickup_list = pickups.copy()
    for pickup in pickups:
        pickup_range = hero["graphics"].getRadius() + pickup["radius"]
        distance = distance_between_objects(hero,pickup)
        if distance <= pickup_range:
            hero,info_string = hero_pickup(hero,pickup)
            pickup["graphics"].undraw()
            pickup_list.remove(pickup)
    pickups = pickup_list
    return(hero,pickups,info_string)


def hero_pickup(hero,pickup):
    if pickup["p_type"] == "Gun":
        gun_list = []
        gun_present = False
        for gun in hero["guns"]:
            if gun["name"] == pickup["name"]:
                gun["ammo"] += pickup["value"]
                print("Picked Up: {}".format(pickup))
                print("Gave ammo to {}".format(gun))
                gun_present=True
        if not gun_present:
            gun = {
                "name":pickup["name"],"type":pickup["type"],"damage":pickup["damage"],"ammo":pickup["ammo"],
                "fire_rate":pickup["fire_rate"],"angle":pickup["angle"],"range":pickup["range"],
                "passthru": pickup["passthru"],"n":pickup["n"],"radius":pickup["p_radius"],"speed":pickup["speed"]}
            hero["guns"].append(gun)
            hero["gun"] = gun
            hero = set_hero_gun_settings(hero,gun)
        info_string="Picked up {}! +{} ammo".format(pickup["name"],pickup["value"])
    elif pickup["p_type"] == "Health":
        hero["health"] += pickup["value"]
        info_string="Health increased! (+{})".format(pickup["value"])
    elif pickup["p_type"] == "Speed":
        if pickup["use"] == "perm":
            hero["speed"] += pickup["value"]
            hero["base_speed"] += pickup["value"]
            info_string = "Permanent speed boost!"
        elif pickup["use"] == "temp":
            hero["boosts"].append(
                {"p_type":"boost","type":"speed","dur":pickup["value"][1],"tick":0,"value":pickup["value"][0],
                 "name":"Speed Boost"})
            info_string = "Temporary speed boost!"
    elif pickup["p_type"] == "Cash":
        hero["cash"] += pickup["cash"]
        info_string = "Picked up ${} cash!".format(pickup["cash"])
    return(hero,info_string)


def hero_boosts(hero):
    boosts_copy = boosts.copy()
    for boost in boosts:
        boost["tick"] += 1
        if boost["tick"] >= boost["dur"] and boost["dur"] != -1:
            boosts_copy.remove(boost)
        else:
            if boost["type"] == "speed":
                hero["speed"] = hero["base_speed"] + boost["value"]
    return(hero)
    

def set_hero_gun_settings(hero,gun):
    hero["fire_rate"] = gun["fire_rate"]
    hero["damage"] = gun["damage"]
    return(hero)


def calc_pickups_decay(pickups):
    pickups_list = pickups.copy()
    for pickup in pickups:
        if pickup["decay"] >= pickup["decay_time"]:
            pickup["graphics"].undraw()
            pickups_list.remove(pickup)
        else:
            pickup["decay"] += 1
            #print(pickup["decay"])
    pickups = pickups_list
    return(pickups)


## Rather than type out 11 lines of code per button, use this function to do it in 1 line ##
def new_button(x1,y1,x_size,y_size,text,function,fill_color,text_color,outline_color,text_size):
    button = {}
    button["button"] = Rectangle(Point(x1, y1),Point(x1+x_size,y1+y_size))
    button["button"].setFill(fill_color)
    button["button"].setOutline(outline_color)
    button["button"].setWidth(2)
    button["text"] = Text(Point(x1+(x_size/2),y1+(y_size/2)),text)
    button["text"].setTextColor(text_color)
    button["text"].setSize(text_size)
    button["function"] = function
    button["fill_color"] = fill_color
    button["text_color"] = text_color
    
    return(button)


def confirm_box(win,text,subtext):
    x,y = get_screen_size()
    
    to_draw, buttons = [], []
    
    box = Rectangle(
        Point((x/2)-200,(y/2)-300),Point((x/2)+200,(y/2)+300))
    box.setFill("black")
    box.setOutline("yellow")
    box.setWidth(4)
    to_draw.append(box)
    
    box_text = Text(
        Point(x/2,(y/2)-265),text)
    box_text.setTextColor("white")
    box_text.setStyle("bold")
    box_text.setSize(24)
    to_draw.append(box_text)
    
    box_subtext = Text(
        Point(x/2,(y/2)+30),subtext)
    box_subtext.setTextColor("white")
    box_subtext.setSize(16)
    to_draw.append(box_subtext)
    
    confirm_button = new_button((x/2)-150,(y/2)+250,300,60,"CONFIRM","confirm","blue","white","yellow",18)
    buttons.append(confirm_button)
    to_draw.append(confirm_button["button"])
    to_draw.append(confirm_button["text"])
    
    for item in to_draw:
        item.draw(win)
    
    click = win.getMouse()
    clicked_on = interpret_click(win,buttons,click)
    if clicked_on != None:
        choice = True
    else:
        choice = False
    
    for item in to_draw:
        item.undraw()
    
    return(choice)


def info_box(win,text,subtext):
    x,y = get_screen_size()
    
    to_draw, buttons = [], []
    
    box = Rectangle(
        Point((x/2)-200,(y/2)-300),Point((x/2)+200,(y/2)+300))
    box.setFill("black")
    box.setOutline("yellow")
    box.setWidth(4)
    to_draw.append(box)
    
    box_text = Text(
        Point(x/2,(y/2)-265),text)
    box_text.setTextColor("white")
    box_text.setStyle("bold")
    box_text.setSize(24)
    to_draw.append(box_text)
    
    box_subtext = Text(
        Point(x/2,(y/2)+30),subtext)
    box_subtext.setTextColor("white")
    box_subtext.setSize(16)
    to_draw.append(box_subtext)
    
    for item in to_draw:
        item.draw(win)
    
    click = win.getMouse()
    
    for item in to_draw:
        item.undraw()
    
    return



## Takes a list of buttons and a click ##
## Returns the function of the button, if any, that was clicked on ##
## Otherwise returns None ##
def interpret_click(win,buttons,click):
    click_x, click_y = click.getX(), click.getY()
    for button in buttons:
        x1 = button["button"].getP1().getX()
        y1 = button["button"].getP1().getY()
        x2 = button["button"].getP2().getX()
        y2 = button["button"].getP2().getY()
        
        if x1 > x2:
            x1,x2 = x2,x1
        if y1 > y2:
            y1,y2 = y2,y1
        
        if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
            button["button"].setFill("white")
            button["text"].setTextColor("black")
            update()
            time.sleep(0.15)
            button["button"].setFill(button["fill_color"])
            button["text"].setFill(button["text_color"])
            update()
            time.sleep(0.05)
            print("Clicked on {}".format(button["function"]))
            return(button["function"])
    
    return(None)


def draw_game_choice_menu(win):
    for item in win.items.copy():
        item.undraw()
    buttons,to_draw = [],[]
    
    center_x = settings["window_x"]["value"]/2
    center_y = settings["window_y"]["value"]/2
    
    horde_button = new_button(center_x-400,150,800,100,"Horde Mode","horde","black","white","white",30)
    buttons.append(horde_button)
    to_draw.append(horde_button["button"])
    to_draw.append(horde_button["text"])
    
    wave_button = new_button(center_x-400,350,800,100,
                                  "Wave Mode","wave","black","white","white",30)
    buttons.append(wave_button)
    to_draw.append(wave_button["button"])
    to_draw.append(wave_button["text"])
    
    adventure_button = new_button(center_x-400,550,800,100,
                                  "Adventure Mode","adventure","black","white","white",30)
    buttons.append(adventure_button)
    to_draw.append(adventure_button["button"])
    to_draw.append(adventure_button["text"])
    
    back_button = new_button(center_x-100,750,200,100,"Go Back","go back","red3","white","white",24)
    buttons.append(back_button)
    to_draw.append(back_button["button"])
    to_draw.append(back_button["text"])
        
    for item in to_draw:
        item.draw(win)
    
    play = True
    while play:
        click = win.getMouse()
        clicked_on = interpret_click(win,buttons,click)
        if clicked_on == "horde":
            for item in win.items.copy():
                item.undraw()
            score = horde(win)
            check_new_high_score(win,score)
            high_score_ui = draw_high_score(win)
            play = False
        
        elif clicked_on == "wave":
            player = build_hero(win)
            player["guns"].append(all_guns[0].copy())
            win,player = draw_wave_menu(win,player)
            
            for item in to_draw:
                item.draw(win)
        
        elif clicked_on == "adventure":
            player = build_hero(win)
            player["guns"].append(all_guns[0].copy())
            win,player = draw_adventure_map(win,player)
            
            for item in to_draw:
                item.draw(win)

        elif clicked_on == "go back":
            choice = "go back"
            play = False
    
    return(win)


def draw_wave_menu(win,player):
    print("\n Player:")
    for item in player.keys():
        print("{}: {}".format(item, player[item]))
    print("\n")
    #print(player)
    win.setBackground("black")
    
    for item in win.items.copy():
        item.undraw()
    buttons,to_draw = [],[]
    
    wave_number = 1
    right = settings["window_x"]["value"]
    bottom = settings["window_y"]["value"]
    
    center_x = right/2
    center_y = bottom/2
    
    title_box = new_button(center_x-(center_x/2),100,center_x,50,
                          "Wave Mode","title","black","white","black",30)
    to_draw.append(title_box["button"])
    to_draw.append(title_box["text"])
    
    wave_box = new_button(center_x-(center_x/2),150,center_x,50,
                          "Wave {}".format(wave_number),"wave","black","white","black",24)
    to_draw.append(wave_box["button"])
    to_draw.append(wave_box["text"])
    
    
    fight_button = new_button(center_x-(center_x/2),300,center_x,100,"Fight","fight","blue1","white","white",30)
    buttons.append(fight_button)
    to_draw.append(fight_button["button"])
    to_draw.append(fight_button["text"])
    
    shop_button = new_button(center_x-(center_x/2),500,center_x,100,"Shop","shop","green","white","white",30)
    buttons.append(shop_button)
    to_draw.append(shop_button["button"])
    to_draw.append(shop_button["text"])
    
    back_button = new_button(center_x-100,700,200,100,"Go Back","go back","red3","white","white",24)
    buttons.append(back_button)
    to_draw.append(back_button["button"])
    to_draw.append(back_button["text"])
    
    for item in to_draw:
        item.draw(win)
    
    play = True
    mode = "buy"
    while play:
        click = win.getMouse()
        clicked_on = interpret_click(win,buttons,click)
        if clicked_on == "shop":
            win,player = draw_shop_menu(win,player)
            for item in to_draw:
                item.draw(win)
                
            print("\n Player in wave_menu after shop_menu:")
            for item in player.keys():
                print("{}: {}".format(item, player[item]))
            print("\n")
                
        elif clicked_on == "fight":
            mobs = 50 + (wave_number * 20)
            biome = random.choice(["grass","desert","snow"])
            win,player,wave_number = wave(win,player,wave_number,mobs,biome)
            win.setBackground("black")
            for item in to_draw:
                item.draw(win)
            wave_box["text"].setText("Wave {}".format(wave_number))
            
            print("\n Player:")
            for item in player.keys():
                print("{}: {}".format(item, player[item]))
            print("\n")
            
        elif clicked_on == "go back":
            choice = "go back"
            play = False
    
    for item in win.items.copy():
        item.undraw()
    return(win,player)


def does_player_own_gun(item,player):
    owned_id = 0
    for p_item in player["guns"]:
        if item["name"] == p_item["name"]:
            return(True,p_item["ammo"],owned_id)
        owned_id += 1
    return(False,0,0)


def does_player_own_boost(item,player):
    owned_id = 0
    for p_item in player["boosts"]:
        if item["name"] == p_item["name"]:
            return(True,p_item["ammo"],owned_id)
        owned_id += 1
    return(False,0,0)


def draw_shop_menu(win,player):
    for item in win.items.copy():
        item.undraw()
    buttons,to_draw = [],[]
    
    player_items = []
    for gun in player["guns"]:
        player_items.append(gun)
    
    #print("Start of shop_menu\nPlayer guns:")
    #for item in player["guns"]:
    #    print(item)
    #print("\nBoosts:")
    for boost in player["boosts"]:
    #    print(boost)
        player_items.append(boost)
    
    shop_items = all_guns
    selected_item = shop_items[0]
    item_id = 0
    
    right = settings["window_x"]["value"]
    bottom = settings["window_y"]["value"]
    border = 20
    
    column_l = int(right*0.75)
    column_r = right - column_l - border
    
    center_x = settings["window_x"]["value"]/2
    center_y = settings["window_y"]["value"]/2
    
    title_bar = new_button(border,border,column_l,80,"Guns & Stuff","title","bisque","black","white",28)
    to_draw.append(title_bar["button"])
    to_draw.append(title_bar["text"])
    
    player_cash_bar = new_button(column_l,border,column_r,80,"Cash: $0","cash","black","green1","white",20)
    to_draw.append(player_cash_bar["button"])
    to_draw.append(player_cash_bar["text"])
    
    buy_mode_button = new_button(border,border+100,center_x-border,80,"Buy Mode","buy mode","green","black","green",18)
    buttons.append(buy_mode_button)
    to_draw.append(buy_mode_button["button"])
    to_draw.append(buy_mode_button["text"])
    
    sell_mode_button = new_button(center_x+(border/2),border+100,center_x-(border*1.5),80,
                                  "Sell Mode","sell mode","blue","black","blue",18)
    buttons.append(sell_mode_button)
    to_draw.append(sell_mode_button["button"])
    to_draw.append(sell_mode_button["text"])
    
    item_name_bar = new_button(20,220,column_l-column_r,80,"Item Name","item_name","black","white","white",30)
    to_draw.append(item_name_bar["button"])
    to_draw.append(item_name_bar["text"])
    
    item_price_bar = new_button(center_x+border,220,column_r,80,
                                "Item Price","item_price","black","white","white",22)
    to_draw.append(item_price_bar["button"])
    to_draw.append(item_price_bar["text"])
    
    item_ammo_bar = new_button(20,320,column_r,50,
                                "Item Ammo","item_ammo","black","white","white",22)
    to_draw.append(item_ammo_bar["button"])
    to_draw.append(item_ammo_bar["text"])
    
    item_owned_bar = new_button(center_x+border,320,column_r,50,
                                "Item Owned","item_owned","black","white","white",22)
    to_draw.append(item_owned_bar["button"])
    to_draw.append(item_owned_bar["text"])
    
    item_desc_bar = new_button(20,390,column_l-border,center_y+(border/2),
                               "Item Description","item_desc","black","white","white",16)
    to_draw.append(item_desc_bar["button"])
    to_draw.append(item_desc_bar["text"])
    
    next_item_button = new_button(column_l+border,220,column_r-border,80,
                                  "Next Item >","next item","black","green1","white",18)
    buttons.append(next_item_button)
    to_draw.append(next_item_button["button"])
    to_draw.append(next_item_button["text"])
    
    prev_item_button = new_button(column_l+border,320,column_r-border,80,
                                  "Previous Item <","prev item","black","green1","white",18)
    buttons.append(prev_item_button)
    to_draw.append(prev_item_button["button"])
    to_draw.append(prev_item_button["text"])
    
    transact_button = new_button(column_l+border,420,column_r-border,80,
                                 "Transact","transact","white","white","white",18)
    buttons.append(transact_button)
    to_draw.append(transact_button["button"])
    to_draw.append(transact_button["text"])
    
    go_back_button = new_button(column_l+border,bottom-120,column_r-border,80,
                                "Go Back","go back","red3","white","white",18)
    buttons.append(go_back_button)
    to_draw.append(go_back_button["button"])
    to_draw.append(go_back_button["text"])
    
    
    for item in to_draw:
        item.draw(win)
    
    play = True
    mode = "buy"
    while play:
        player_cash_bar["text"].setText("Cash: ${}".format(player["cash"]))
        if mode == "buy":
            if shop_items[item_id]["p_type"] == "Gun":
                owned,owned_ammo,owned_id = does_player_own_gun(shop_items[item_id],player)
                
            elif shop_items[item_id]["p_type"] == "AutoGun":
                owned,owned_ammo,owned_id = does_player_own_boost(shop_items[item_id],player)
                
            item_name_bar["text"].setText(shop_items[item_id]["name"])
            item_price_bar["text"].setText("Price: ${}".format(shop_items[item_id]["price"]))
            item_ammo_bar["text"].setText("Ammo: {}".format(shop_items[item_id]["ammo"]))
            if owned:
                item_owned_bar["text"].setText("OWNED ({})".format(owned_ammo))
            else:
                item_owned_bar["text"].setText("")
            item_desc_bar["text"].setText(
                "P_Type: {}\nType: {}\nDamage: {}\nProjectiles: {}\nRange: {}\nFire Rate: {}\nPassthru: {}\nProjectile Speed: {}".format(
                shop_items[item_id]["p_type"],shop_items[item_id]["type"],shop_items[item_id]["damage"],
                shop_items[item_id]["n"],shop_items[item_id]["range"],shop_items[item_id]["fire_rate"],
                shop_items[item_id]["passthru"],shop_items[item_id]["speed"]))
            
        else:
            print("Selected item: {}".format(player_items[item_id]))
            
            item_name_bar["text"].setText(player_items[item_id]["name"])
            item_price_bar["text"].setText("Price: ${}".format(int(player_items[item_id]["price"]/2)))
            item_owned_bar["text"].setText("OWNED")
            item_ammo_bar["text"].setText("Ammo: {}".format(player_items[item_id]["ammo"]))
            item_desc_bar["text"].setText(
                "Type: {}\nDamage: {}\nProjectiles: {}\nRange: {}\nFire Rate: {}\nPassthru: {}\nProjectile Speed: {}".format(
                player_items[item_id]["type"],player_items[item_id]["damage"],player_items[item_id]["n"],
                player_items[item_id]["range"],player_items[item_id]["fire_rate"],player_items[item_id]["passthru"],
                player_items[item_id]["speed"]))
            
        
        
        ## Show toggles ##
        if mode == "buy":
            transact_button["text"].setText("Buy")
            transact_button["button"].setFill("green")
            
            buy_mode_button["button"].setFill(buy_mode_button["fill_color"])
            buy_mode_button["text"].setTextColor(buy_mode_button["text_color"])
            
            sell_mode_button["button"].setFill("black")
            sell_mode_button["text"].setTextColor("white") 
            
        else:
            transact_button["text"].setText("Sell")
            transact_button["button"].setFill("blue")
            
            sell_mode_button["button"].setFill(sell_mode_button["fill_color"])
            sell_mode_button["text"].setTextColor(sell_mode_button["text_color"])
            
            buy_mode_button["button"].setFill("black")
            buy_mode_button["text"].setTextColor("white")
        ## ##
        update()
            
        click = win.getMouse()
        clicked_on = interpret_click(win,buttons,click)
        
        #print("\n\nAfter interpret click, before clicked_on actions in shop_menu\nPlayer guns:")
        #for p_gun in player["guns"]:
        #    print(p_gun)
        #print("Boosts:")
        #for boost in player["boosts"]:
        #    print(boost)
            
        #1
        if clicked_on == "buy mode":
            mode = "buy"
            item_id = 0
        #2
        elif clicked_on == "sell mode":
            item_id = 0
            mode = "sell"
        #3
        elif clicked_on == "next item":
            item_id += 1
            if mode == "buy":
                if item_id > len(shop_items)-1:
                    item_id = 0
            else:
                if item_id > len(player_items)-1:
                    item_id = 0
        #4
        elif clicked_on == "prev item":
            item_id -= 1
            if mode == "buy":
                if item_id < 0:
                    item_id = len(shop_items)-1
            else:
                if item_id < 0:
                    item_id = len(player_items)-1
        #5
        elif clicked_on == "transact":
            if mode == "buy":
                if player["cash"] >= shop_items[item_id]["price"]: #Check if player has enough cash
                    player["cash"] -= shop_items[item_id]["price"] #Remove cash from player account
                    if shop_items[item_id]["p_type"] == "Gun":
                        if owned:
                            player["guns"][owned_id]["ammo"] += shop_items[item_id]["ammo"]
                        else:
                            player["guns"].append(shop_items[item_id].copy())
                            
                    elif shop_items[item_id]["p_type"] == "AutoGun":
                        if owned:
                            player["boosts"][owned_id]["ammo"] += shop_items[item_id]["ammo"]
                        else:
                            player["boosts"].append(shop_items[item_id].copy())
                            
            else:
                if player_items[item_id]["price"] > 0:
                    player["cash"] += int(player_items[item_id]["price"]/2)
                    del(player_items[item_id])
                    item_id -= 1
        #6
        elif clicked_on == "go back":
            choice = "go back"
            play = False
    
        print("\n\nEnd of clicked_on actions\nPlayer guns:")
        for p_gun in player["guns"]:
            print(p_gun)
    
    for item in win.items.copy():
        item.undraw()
    return(win,player)


def decorate_map(win,biome):
    deco_list = []
    
    if biome == "grass" or biome == "default" or biome == "":
        win.setBackground("green4")
        deco_amount = 40
        deco_types = ["img/Tree.png","img/Rock.png","img/Grass.png","img/Bush.png"]
    elif biome == "desert":
        win.setBackground("bisque")
        deco_amount = 15
        deco_types = ["img/Rock.png","img/Grass.png"]
    elif biome == "snow":
        win.setBackground("snow")
        deco_amount = 60
        deco_types = ["img/Tree.png","img/Tree.png","img/Rock.png"]
        
        
    for i in range(deco_amount):
        deco = Image(Point(random.randrange(0,settings["window_x"]["value"]),
                           random.randrange(100,settings["window_y"]["value"])),
                     random.choice(deco_types))
        deco_list.append(deco)
    
    return(win,deco_list)



def draw_adventure_map(win,player):
    for item in win.items.copy():
        item.undraw()
    win.setBackground("green4")
    
    buttons,to_draw,aoi_list = [],[],[]
    
    
    ## Prepare Menu Button ##
    menu = {}
    menu["button"] = Rectangle(Point(0,0),Point(120,100))
    menu["button"].setFill("blue2")
    menu["button"].setOutline("white")
    menu["button"].setWidth(4)
    menu["text"] = Text(Point(60,50),"MENU")
    menu["text"].setTextColor("black")
    menu["text"].setSize(20)
    menu["function"] = "menu"
    menu["fill_color"] = "blue2"
    menu["text_color"] = "white"
    buttons.append(menu)
    to_draw.append(menu["button"])
    to_draw.append(menu["text"])
    
    
    ## Prepare Title Bar for player context ##
    title = {}
    title["button"] = Rectangle(Point(120,0),Point(settings["window_x"]["value"],100))
    title["button"].setFill("black")
    title["button"].setOutline("white")
    title["button"].setWidth(4)
    title["text"] = Text(Point(settings["window_x"]["value"]/2,50),"WORLD MAP")
    title["text"].setTextColor("white")
    title["text"].setSize(36)
    title["fill_color"] = "black"
    title["text_color"] = "white"
    title["function"] = "title"
    to_draw.append(title["button"])
    to_draw.append(title["text"])
    
    
    ## Prepare roads on map between aois ##
    for item in adv_map:
        if len(item["unlocks"]) > 0:
            for r in item["unlocks"]:
                road = Line(Point(item["loc"][0],item["loc"][1]),Point(r[0],r[1]))
                road.setOutline("black")
                road.setWidth(3)
                to_draw.append(road)
    
    
    ## Prepare map Areas of Interest (aoi) ##
    for item in adv_map:
        aoi = item.copy()
        aoi["button"] = Circle(Point(item["loc"][0],item["loc"][1]),item["size"])
        aoi["button"].setOutline("black")
        aoi["button"].setWidth(2)
        aoi["text"] = Text(Point(item["loc"][0],item["loc"][1]),"")
        
        if item["faction"] == "Friendly":
            aoi["fill_color"] = "blue"
        elif item["faction"] == "Hostile":
            aoi["fill_color"] = "red"
        elif item["faction"] == "Empty":
            aoi["fill_color"] = "white"
        aoi["function"] = item
        aoi["text_color"] = "black"
        aoi["button"].setFill(aoi["fill_color"])
        buttons.append(aoi)
        to_draw.append(aoi["button"])
        aoi_list.append(aoi)
        
        
    for item in to_draw:
        item.draw(win)
        
    update()
        
    play = True
    while play:
        #print("Updating faction colors")
        for aoi in aoi_list:
            #print("Checking aoi: {}".format(aoi))
            ## Update faction color assignment ##
            if aoi["faction"] == "Friendly":
                aoi["fill_color"] = "blue"
            elif aoi["faction"] == "Hostile":
                aoi["fill_color"] = "red"
            elif aoi["faction"] == "Empty":
                aoi["fill_color"] = "silver"
                #print("{} should be white".format(aoi))
                
            ## Black out nodes that are locked ##
            if aoi["locked"]:
                aoi["button"].setFill("black")
            else:
                aoi["button"].setFill(aoi["fill_color"])
        update()
        
        click = win.getMouse()
        clicked_on = interpret_click(win,buttons,click)
        
        if clicked_on == "menu":
            play=False
        elif type(clicked_on) == dict:
            name = clicked_on["name"]
            for n_aoi in aoi_list:
                if name == n_aoi["name"]:
                    aoi = n_aoi
            if clicked_on["faction"] == "Hostile":
                if clicked_on["locked"]:
                    info_box(win,"Node locked!","You must find a path\nto this node!")
                else:
                    ## Ask player to confirm if they want to attack this aoi ##
                    if confirm_box(win,"Attack?","{}\n{} tier {} mobs".format(aoi["name"],aoi["mobs"],aoi["tier"])):
                        win,player,wave_number = wave(win,player,aoi["tier"],aoi["mobs"],"grass")
                        
                        ## Check if player won ##
                        if wave_number > aoi["tier"]:
                            info_box(win,"Reward!","Received ${}".format(aoi["rewards"]["cash"]))
                            player["cash"] += aoi["rewards"]["cash"]
                            aoi["faction"] = "Empty"
                            aoi["function"]["faction"] = "Empty"
                            aoi["mobs"] = 0
                            unlocks = aoi["unlocks"]
                            #print("aoi: {}".format(aoi))
                            #print("Unlocks: {}".format(unlocks))
                            ## If so, unlock nodes ##
                            for n_aoi in aoi_list:
                                #print("n_aoi loc: {}".format(n_aoi["loc"]))
                                if n_aoi["loc"] in unlocks and n_aoi["locked"]:
                                    n_aoi["locked"] = False
                                    n_aoi["function"]["locked"] = False
                                    info_box(win,"Unlocked!","Unlocked {}".format(n_aoi["name"]))
                        
                        ## Reset adv map ##    
                        win.setBackground("green4")
                        for item in to_draw:
                            item.draw(win)
                            
            elif clicked_on["faction"] == "Empty":
                info_box(win,clicked_on["name"],"This town has been\nemptied of hostiles.")
            
            elif clicked_on["faction"] == "Friendly":
                if "Shop" in clicked_on["features"]:
                    win.setBackground("black")
                    win,player = draw_shop_menu(win,player)
                    
                    win.setBackground("green4")
                    for item in to_draw:
                        item.draw(win)
                
                
    ## Reset window back to default and erase all drawn items ##    
    win.setBackground("black")
    for item in win.items.copy():
        item.undraw()
    
    return(win,player)


    
    
def draw_main_menu(win):
    win_ui = []
    start_box,title_box,highscore_box,exit_box = {},{},{},{}
    
    ## Calculate middle of screen, and size of buttons ##
    button_height = settings["window_y"]["value"]/8
    button_width = round(settings["window_x"]["value"]/3)
    button_gap = button_height
    centerx,centery=settings["window_x"]["value"]/2,settings["window_y"]["value"]/2
    
    ## Calculate box corner points ##
    title_box_P1 = [centerx-(button_width/2),button_height/2]
    title_box_P2 = [centerx+(button_width/2),title_box_P1[1]+button_height]
    
    ## Place start box below title ##
    start_box_P1 = [title_box_P1[0],title_box_P1[1]+(button_gap*2)]
    start_box_P2 = [title_box_P2[0],title_box_P2[1]+(button_gap*2)]
    
    ## Place highscore box below start box ##
    highscore_box_P1 = [start_box_P1[0],start_box_P1[1]+(button_gap*2)]
    highscore_box_P2 = [start_box_P2[0],start_box_P2[1]+(button_gap*2)]
    
    ## Place exit box below highscore box ##
    exit_box_P1 = [highscore_box_P1[0],highscore_box_P1[1]+(button_gap*2)]
    exit_box_P2 = [highscore_box_P2[0],highscore_box_P2[1]+(button_gap*2)]
    
    ## Build and modify items as needed ##
    title_box = build_ui_box(title_box,title_box_P1,title_box_P2)
    title_box["text"].setSize(36)
    title_box["text"].setTextColor(settings["fg_color"]["value"])
    title_box["text"].setText("Shooter.py\nSlam Jones 2022")
    title_box["box"].setOutline(settings["bg_color"]["value"])
    
    start_box = build_ui_box(start_box,start_box_P1,start_box_P2)
    start_box["text"].setSize(36)
    start_box["text"].setTextColor(settings["fg_color"]["value"])
    start_box["text"].setText("Start!")
    start_box["box"].setWidth(3)
    
    highscore_box = build_ui_box(highscore_box,highscore_box_P1,highscore_box_P2)
    highscore_box["text"].setSize(36)
    highscore_box["text"].setTextColor(settings["fg_color"]["value"])
    highscore_box["text"].setText("High Scores")
    highscore_box["box"].setWidth(3)
    
    exit_box = build_ui_box(exit_box,exit_box_P1,exit_box_P2)
    exit_box["text"].setSize(36)
    exit_box["text"].setTextColor(settings["fg_color"]["value"])
    exit_box["text"].setText("Exit")
    exit_box["box"].setWidth(3)
    
    ## Draw items ##
    title_box["box"].draw(win)
    title_box["text"].draw(win)
    start_box["box"].draw(win)
    start_box["text"].draw(win)
    highscore_box["box"].draw(win)
    highscore_box["text"].draw(win)
    exit_box["box"].draw(win)
    exit_box["text"].draw(win)
    
    win_ui = [title_box,start_box,highscore_box,exit_box]
    return(win_ui)


def undraw_ui(ui):
    for item in ui:
        item["box"].undraw()
        item["text"].undraw()
    
    
def main_menu(win):
    exit = False
    start = False
    while not exit:
        menu_ui = draw_main_menu(win)
        clickPoint = win.getMouse()
        action = check_click(clickPoint,menu_ui)
        #print(clickPoint)
        #print(action)
        if action == "Start!":
            start = True
        elif action == "High Scores":
            start = False
            high_score_ui = draw_high_score(win)
            win.getMouse()
            for item in high_score_ui:
                item.undraw()
        elif action == "Exit":
            exit = True
        if start:
            win = draw_game_choice_menu(win)
            clear_screen_all(win)
            start = False
            
            
def check_click(clickPoint,ui):
    #print(clickPoint)
    clickX,clickY = clickPoint.getX(),clickPoint.getY()
    for item in ui:
        P1x,P1y = item["box"].getP1().getX(),item["box"].getP1().getY()
        P2x,P2y = item["box"].getP2().getX(),item["box"].getP2().getY()
        #print(P1x,P2x,P1y,P2y)
        if clickX >= P1x and clickX <= P2x and clickY >= P1y and clickY <= P2y:
            flash_ui_item(item)
            return(item["text"].getText())
    return()


def flash_ui_item(ui_item):
    wait_time = 0.1
    ui_item["box"].setFill(settings["fg_color"]["value"])
    update()
    time.sleep(wait_time)
    ui_item["box"].setFill(settings["bg_color"]["value"])
    update()
    time.sleep(wait_time/2)
    
    
def check_new_high_score(win,score):
    index = 0
    if score > 0:
        for item in high_scores:
            if score >= item["score"]:
                name = get_score_name(win)
                high_score = {"name": name, "score":score}
                high_scores.insert(index,high_score)
                high_scores.remove(high_scores[-1])
                return
            index += 1

        
def get_score_name(win):
    ## Reset xset so that entering name is easier for player ##
    reset_xset()
    #_=os.system('xset r rate')
    ## Determine where to draw the items ##
    centerx,centery=settings["window_x"]["value"]/2,settings["window_y"]["value"]/2
    topy = round(settings["window_y"]["value"] * 0.25)
    box_size_x,box_size_y = settings["window_x"]["value"]/2,settings["window_y"]["value"]/2
    input_title = Text(Point(centerx,topy), "Enter your name, click when done: ")
    input_title.setTextColor(settings["fg_color"]["value"])
    input_title.setSize(26)
    input_box = Entry(Point(centerx,centery), settings["max_name_len"]["value"])
    input_title.draw(win)
    input_box.draw(win)
    win.getMouse()
    input_box.undraw()
    input_title.undraw()
    set_xset()
    #_=os.system('xset r rate 70')
    return(input_box.getText())
    
    
def draw_high_score(win):
    high_score_ui = []
    centerx,centery=settings["window_x"]["value"]/2,settings["window_y"]["value"]/2
    topy = round(settings["window_y"]["value"] * 0.25)
    scores_string = ""
    scores_title = Text(Point(centerx,topy),"High Scores")
    scores_title.setSize(30)
    scores_title.setTextColor(settings["fg_color"]["value"])
    scores_text = Text(Point(centerx,centery),scores_string)
    for item in high_scores:
        scores_string += str(item["name"])+": "+str(item["score"])+"\n"
    scores_text.setText(scores_string)
    scores_text.setTextColor(settings["fg_color"]["value"])
    box_width = round(settings["window_x"]["value"]*0.15)
    box_height = round(settings["window_y"]["value"]*0.35)
    scores_box_P1 = (centerx-box_width,centery-box_height)
    scores_box_P2 = (centerx+box_width,centery+box_height)
    scores_box = Rectangle(
        Point(scores_box_P1[0],scores_box_P1[1]),Point(scores_box_P2[0],scores_box_P2[1]))
    scores_box.setFill(settings["bg_color"]["value"])
    scores_box.setOutline(settings["fg_color"]["value"])
    scores_box.setWidth(3)
    scores_box.draw(win)
    scores_text.draw(win)
    scores_title.draw(win)
    high_score_ui.append(scores_box)
    high_score_ui.append(scores_text)
    high_score_ui.append(scores_title)
    return(high_score_ui)


def clear_screen_all(win):
    for item in win.items:
        #print(item)
        item.undraw()
    x = Rectangle(Point(0,0),
                  Point(settings["window_x"]["value"],settings["window_y"]["value"]))
    x.setFill("black")
    to_draw = [x]
    draw_to_draw(win,to_draw)
    

def clear_playfield(win,mobs,ui):
    x = Rectangle(Point(0,settings["window_y"]["value"]/10),
                  Point(settings["window_x"]["value"],settings["window_y"]["value"]))
    x.setFill("black")
    to_draw = [x]
    draw_to_draw(win,to_draw)
    redraw_item_group(win,mobs)
    ui = redraw_ui(win,ui)
    return(ui)


def clear_screen(win,mobs,ui):
    ui = clear_playfield(win,mobs,ui)
    ui = ""
    return(ui)

    
def init():
    clear()
    collect_screen_info()
    calculate_top_boundary()
    set_xset()
    global high_scores
    high_scores = load_high_scores()
    
    
def main():
    win = open_window()
    main_menu(win)
    
    
def wave(win,hero,wave_number,mobs_to_spawn,biome):
    for item in win.items.copy():
        item.undraw()
        
    ui = build_ui(win)
    projectiles = []
    mobs = []
    play = True
    mouse = False
    pause = False
    shoot = True
    timer = 1
    lowest_fps = settings["frame_rate"]["value"]
    last_x_frames = []
    recent_fps,avg_fps,frames,ticks,efps,last_ms,score,max_proj_counted,max_mob_counted,last_autoshot = 0,0,0,0,0,0,0,0,0,0
    shoot_ticks = 100
    ms_times = {}
    ms_max = {}
    start_time = time.time()
    mob_speed = settings["mob_speed"]["value"]
    text_queue = []
    pickups = []
    fps_factor = 1.0
    debug_ui = build_debug_ui(win)
    print(debug_ui)
    
    mobs_spawned = 0
    mob_level = 1
    mobs_killed = 0

    win,deco_list = decorate_map(win,biome)    
    for item in deco_list:
        item.draw(win)
    
    info_box(win,"Wave "+str(wave_number),"Get ready!")
    
    while play:
        ## Calculate FPS ##
        timer = time.time()
        start_time = time.time()
        if recent_fps > 0:
            fps_factor = (settings["frame_rate"]["value"]/recent_fps)
        
        ## Set UI Text ##
        ui["fps_box"]["text"].setText(
            str(round(recent_fps,1))+" avg fps\n"+str(lowest_fps)+" lowest\n"+str(round(last_ms*1000,1))+" ms")
        ui["score_box"]["text"].setText("Cash:\n$"+str(hero["cash"]))
        max_proj_counted = return_higher(max_proj_counted,len(projectiles))
        max_mob_counted = return_higher(max_proj_counted,len(mobs))
        ui["count_box"]["text"].setText("{}({}) projectiles\n{}({}) mobs".format(
            str(len(projectiles)),str(max_proj_counted),str(len(mobs)),str(max_mob_counted)))
        ui = set_weapon_text(win,ui,hero)
        ui["hp_box"]["text"].setText("Health:\n{}".format(hero["health"]))
        
        ms_times = {}
        ms_times["ui"] = round((time.time() - start_time)*1000)
        
        projectiles = move_projectiles(win,projectiles)
        ## PROCESS MOVEMENT AND STUFF ##
        ## Take a copy of the mobs list before we modify it for this tick ##
        mobs_before = mobs.copy()
        projectiles,mobs = check_for_projectile_hits(win,projectiles,mobs)
        mobs = move_mobs(win,mobs,hero)
        if len(mobs) != len(mobs_before):
            mobs_spawned -= len(mobs_before) - len(mobs)
        ms_times["move"] = round(((time.time() - start_time)*1000)-ms_times["ui"])
        hero = check_hero_mob_collisions(win,hero,mobs)
        if len(hero["animation"]) > 0:
            hero["tangible"] = False
        else:
            hero["tangible"] = True
            
        ms_times["mhits"] = round(((time.time() - start_time)*1000)-ms_times["move"])
            
        ## Check if hero is dead, or play should be stopped ##
        if hero["health"] <= 0:
            play = False
            
            for item in win.items.copy():
                item.undraw()
            info_box(win,"You lose!","You have defeated")

            ## Reset hero stats ##
            hero["cash"] = 0
            hero["health"] = 3
            hero["damage"] = 1
            hero["fire_rate"] = 4
            max_dist = settings["projectile_max_distance"]["value"]*2
            hero["guns"] = [{"name":"Basic Pistol","type":"Basic","damage": 1,"ammo":100000,
                             "fire_rate":4,"range":max_dist,"n":1,"passthru":0,"price":0}]
            hero["gun"] = hero["guns"][0]
            hero["boosts"] = []
            
            wave_number = 1
            return(win,hero,wave_number)
        
        ## Process current pickups, start counter for spawning a new one if needed ##
        hero,pickups,info_string = check_pickup_collision(win,hero,pickups)
        if info_string != "":
            text_queue=[(timed_info_text(info_string,45))]
        hero = check_hero_ammo(hero)
        pickups = calc_pickups_decay(pickups)
        
        ## Check for autoguns on player; use if present ##
        for boost in hero["boosts"]:
            if boost["p_type"] == "AutoGun":
                boost["last_shot"] += 1
                ## Fire at last fire direction ##
                if boost["last_shot"] >= boost["fire_rate"]:
                    
                    new_projectiles=fire_auto_projectile(win,hero,boost,mobs)
                    for p in new_projectiles:
                        projectiles.append(p)
                    #new_projectiles,score=shoot_autoshot(win,hero,score,projectiles,mobs)
                    boost["last_shot"] = 0
                
        ms_times["pkps"] = round(((time.time() - start_time)*1000)-ms_times["mhits"])
        
        ## Process animations once we have checked for and collected collisions ##
        ui,text_queue = text_animation_queue(win,ui,text_queue)
        mobs.append(hero)
        mobs = animation_queue(win,mobs)
        mobs.remove(hero)
        
        ms_times["anim"] = round(((time.time() - start_time)*1000)-ms_times["pkps"])
        
        ## Copy mob list with current modifications ##
        mobs_after = mobs.copy()
        for mob in mobs:
            ## If any are marked for deletion, do so now ##
            if mob["delete"]:
                #mob["graphics"].undraw()
                mobs_after.remove(mob)
                score += mob["score"]
                mobs_killed += 1
                mobs_now -= 1
                hero["cash"] += 100
                #print("Mob {} killed".format(mobs_killed))
        ## Overwrite mob list with new mob list ##
        mobs = mobs_after
        
        ## Use spawn controller to spawn more mobs if needed ##
        ## First check if we have the same list of mobs as before we started this tick ##
        max_mobs = 50
        if mobs != mobs_before:
            ## If mobs have changed, redraw hero, ui, and mobs so they appear on top ##
            if settings["debug_mode"]["value"]:
                print("Redrawing hero")
            redraw_item_group(win,mobs)
            ui = redraw_ui(win,ui)
        hero["graphics"] = redraw_graphic(win,hero["graphics"])
        if len(pickups) > 0:
            for pickup in pickups:
                pickup["graphics"].undraw()
                pickup["graphics"].draw(win)
        mobs_now = len(mobs)
        if mobs_spawned < mobs_to_spawn:
            fn_score = mobs_killed + (wave_number-1)*10
            mobs = spawn_controller(win,mobs,max_mobs,fn_score)
            if len(mobs) > mobs_now:
                mobs_spawned += 1
                ## Pickups have a chance to spawn when a mob spawns ##
                if mobs_spawned < mobs_to_spawn:
                    pickups = pickup_spawn_controller_wave(win,hero,pickups,wave_number,["health","speed","cash"])
                    
        if mobs_killed >= mobs_to_spawn:
            ## WIN CONDITION ##
            wave_number += 1
            
            for item in win.items.copy():
                item.undraw()
                
            info_box(win,"You win!","Your foes have been defeated")
            return(win,hero,wave_number)
        
        ms_times["mobs"] = round(((time.time() - start_time)*1000)-ms_times["anim"])
        
        ## Check if player can shoot ##
        shoot_ticks += 1
        if shoot_ticks >= hero["fire_rate"]:
            shoot=True
            ui["weapon_box"]["box"].setFill("black")
        else:
            shoot=False
            ui["weapon_box"]["box"].setFill("gray41")
        
        ms_times["ticks"] = round(((time.time() - start_time)*1000)-ms_times["mobs"])
            
        ## THEN, PROCESS PLAYER CONTROLS ##
        if pause:
            win.getKey()
        else:
            inp = win.checkKey()
            click = win.checkMouse()
            
        ms_times["input1"] = round(((time.time() - start_time)*1000)-ms_times["ticks"])
            
        ## BASIC CONTROLS ##
        ## ESCAPE
        if inp == "Escape":
            play = False
            for item in win.items.copy():
                item.undraw()
            return(win,hero,wave_number)
        ## SHOOT
        elif inp == settings["keys"]["shoot"]["value"]:
            if shoot:
                new_projectiles,score=shoot_button(win,hero,score,projectiles)
                shoot_ticks=0
        elif click != None:
            if shoot:
                hero["direction"] = coords_to_direction(click.getX()-hero["graphics"].getCenter().getX(),
                                                        hero["graphics"].getCenter().getY()-click.getY())+90
                new_projectiles,score=shoot_button(win,hero,score,projectiles)
                shoot_ticks=0
        ## SWITCH WEAPON
        elif inp == settings["keys"]["switch_weapon"]["value"]:
            hero = switch_weapons(hero)
            ui = set_weapon_text(win,ui,hero)
            #text_queue=[(timed_info_text(hero["gun"],45))]
        ## PAUSE
        elif inp == settings["keys"]["pause"]["value"]:
            pause = bool_switch(pause)
            time.sleep(0.2)
            if pause:
                ui = set_info_text(win,ui,"Paused")
            else:
                ui = set_info_text(win,ui,"")
            
        ms_times["input2"] = round(((time.time() - start_time)*1000)-ms_times["input1"])
            
        
        ## ## MOVEMENT CONTROLS ##    
        if inp == settings["keys"]["move_up"]["value"] or inp == "w":
            hero["direction"] = 180
            hero = move_hero(win,hero)
        elif inp == settings["keys"]["move_down"]["value"] or inp == "s":
            hero["direction"] = 0
            hero = move_hero(win,hero)
        elif inp == settings["keys"]["move_right"]["value"] or inp == "d":
            hero["direction"] = 90
            hero = move_hero(win,hero)
        elif inp == settings["keys"]["move_left"]["value"] or inp == "a":
            hero["direction"] = 270
            hero = move_hero(win,hero)
            
            
        ## ## OTHER CONTROLS ## ##
        elif inp == "x":
            for item in win.items:
                item.undraw()
            #print(win.items)
            ui = clear_playfield(win,mobs,ui)
        elif inp == "z":
            toggle_debug_ui(win,debug_ui)
        elif inp == "c":
            win.setBackground(settings["bg_flash"]["value"])
        #elif inp != "" and inp != None:
        #    pass
            #print(type(inp))
            #print(inp)
            #mouse = False
            
        ms_times["input3"] = round(((time.time() - start_time)*1000)-ms_times["input2"])
            
        ## FINALLY, UPDATE THE SCREEN ACCORDING TO FRAME RATE ##
        update(settings["frame_rate"]["value"])
        
        ## AND THEN CHECK FPS CALCULATIONS ##
        ms_times["update"] = round(((time.time() - start_time)*1000)-ms_times["input3"])
        string = str(ms_times)
        update_debug_ui(win,debug_ui,string)
        timer = time.time() - start_time
        last_ms = timer
        
        ### Calculate effective fps for this tick
        efps = int(1/timer)
        frames += efps
        ticks += 1
        avg_fps = frames/ticks
        if efps < lowest_fps:
            lowest_fps = efps
        
        ## Calculate average fps for past x ticks, where x is settings["frame_rate"]["value"] ##
        last_x_frames.append(efps)
        total_frames = 0
        if len(last_x_frames) >= settings["frame_rate"]["value"]:
            for i in range(0,len(last_x_frames)-1):
                total_frames += last_x_frames[i]
            recent_fps = total_frames/settings["frame_rate"]["value"]
            last_x_frames.remove(last_x_frames[0])
        
    
    return(win,hero,wave_number)
    
    
## MAIN CURRENT WORKING GAME MODE ##
def horde(win):
    hero = build_hero(win)
    ui = build_ui(win)
    projectiles = []
    mobs = []
    play = True
    mouse = False
    pause = False
    shoot = True
    timer = 1
    lowest_fps = settings["frame_rate"]["value"]
    last_x_frames = []
    recent_fps,avg_fps,frames,ticks,efps,last_ms,score,max_proj_counted,max_mob_counted = 0,0,0,0,0,0,0,0,0
    shoot_ticks = 100
    ms_times = {}
    ms_max = {}
    start_time = time.time()
    mob_speed = settings["mob_speed"]["value"]
    text_queue = []
    pickups = []
    fps_factor = 1.0
    debug_ui = build_debug_ui(win)
    print(debug_ui)
    
    ## MAIN PLAY LOOP ##
    while play:
        ## Calculate FPS ##
        timer = time.time()
        start_time = time.time()
        if recent_fps > 0:
            fps_factor = (settings["frame_rate"]["value"]/recent_fps)
        
        ## Set UI Text ##
        ui["fps_box"]["text"].setText(
            str(round(recent_fps,1))+" avg fps\n"+str(lowest_fps)+" lowest\n"+str(round(last_ms*1000,1))+" ms")
        ui["score_box"]["text"].setText("Score:\n"+str(score))
        max_proj_counted = return_higher(max_proj_counted,len(projectiles))
        max_mob_counted = return_higher(max_proj_counted,len(mobs))
        ui["count_box"]["text"].setText("{}({}) projectiles\n{}({}) mobs".format(
            str(len(projectiles)),str(max_proj_counted),str(len(mobs)),str(max_mob_counted)))
        ui = set_weapon_text(win,ui,hero)
        ui["hp_box"]["text"].setText("Health:\n{}".format(hero["health"]))
        
        ms_times = {}
        ms_times["ui"] = round((time.time() - start_time)*1000)
        
        projectiles = move_projectiles(win,projectiles)
        ## PROCESS MOVEMENT AND STUFF ##
        ## Take a copy of the mobs list before we modify it for this tick ##
        mobs_before = mobs.copy()
        projectiles,mobs = check_for_projectile_hits(win,projectiles,mobs)
        mobs = move_mobs(win,mobs,hero)
        ms_times["move"] = round(((time.time() - start_time)*1000)-ms_times["ui"])
        hero = check_hero_mob_collisions(win,hero,mobs)
        if len(hero["animation"]) > 0:
            hero["tangible"] = False
        else:
            hero["tangible"] = True
            
        ms_times["mhits"] = round(((time.time() - start_time)*1000)-ms_times["move"])
            
        ## Check if hero is dead, or play should be stopped ##
        if hero["health"] <= 0:
            play = False
            return(score)
        
        ## Process current pickups, start counter for spawning a new one if needed ##
        hero,pickups,info_string = check_pickup_collision(win,hero,pickups)
        if info_string != "":
            text_queue=[(timed_info_text(info_string,45))]
        hero = check_hero_ammo(hero)
        pickups = calc_pickups_decay(pickups)
        pickups = pickup_spawn_controller(win,hero,pickups,score,["health","speed","guns"])
        
        ms_times["pkps"] = round(((time.time() - start_time)*1000)-ms_times["mhits"])
        
        ## Process animations once we have checked for and collected collisions ##
        ui,text_queue = text_animation_queue(win,ui,text_queue)
        mobs.append(hero)
        mobs = animation_queue(win,mobs)
        mobs.remove(hero)
        
        ms_times["anim"] = round(((time.time() - start_time)*1000)-ms_times["pkps"])
        
        ## Copy mob list with current modifications ##
        mobs_after = mobs.copy()
        for mob in mobs:
            ## If any are marked for deletion, do so now ##
            if mob["delete"]:
                #mob["graphics"].undraw()
                mobs_after.remove(mob)
                score += mob["score"]
        ## Overwrite mob list with new mob list ##
        mobs = mobs_after
        
        ## Use spawn controller to spawn more mobs if needed ##
        ## First check if we have the same list of mobs as before we started this tick ##
        max_mobs = 24
        if mobs != mobs_before:
            ## If mobs have changed, redraw hero, ui, and mobs so they appear on top ##
            if settings["debug_mode"]["value"]:
                print("Redrawing hero")
            redraw_item_group(win,mobs)
            ui = redraw_ui(win,ui)
        hero["graphics"] = redraw_graphic(win,hero["graphics"])
        if len(pickups) > 0:
            for pickup in pickups:
                pickup["graphics"].undraw()
                pickup["graphics"].draw(win)
        mobs = spawn_controller(win,mobs,max_mobs,score)
        
        ms_times["mobs"] = round(((time.time() - start_time)*1000)-ms_times["anim"])
        
        ## Check if player can shoot ##
        shoot_ticks += 1
        if shoot_ticks >= hero["fire_rate"]:
            shoot=True
        else:
            shoot=False
        
        ms_times["ticks"] = round(((time.time() - start_time)*1000)-ms_times["mobs"])
            
        ## THEN, PROCESS PLAYER CONTROLS ##
        if pause:
            win.getKey()
        else:
            inp = win.checkKey()
            click = win.checkMouse()
            
        ms_times["input1"] = round(((time.time() - start_time)*1000)-ms_times["ticks"])
            
        ## BASIC CONTROLS ##
        ## ESCAPE
        if inp == "Escape":
            hero["health"] = 0
            play = False
            return(score)
        ## SHOOT
        elif inp == settings["keys"]["shoot"]["value"]:
            if shoot:
                new_projectiles,score=shoot_button(win,hero,score,projectiles)
                shoot_ticks=0
        elif click != None:
            if shoot:
                hero["direction"] = coords_to_direction(click.getX()-hero["graphics"].getCenter().getX(),
                                                        hero["graphics"].getCenter().getY()-click.getY())+90
                new_projectiles,score=shoot_button(win,hero,score,projectiles)
                shoot_ticks=0
        ## SWITCH WEAPON
        elif inp == settings["keys"]["switch_weapon"]["value"]:
            hero = switch_weapons(hero)
            ui = set_weapon_text(win,ui,hero)
            #text_queue=[(timed_info_text(hero["gun"],45))]
        ## PAUSE
        elif inp == settings["keys"]["pause"]["value"]:
            pause = bool_switch(pause)
            time.sleep(0.2)
            if pause:
                ui = set_info_text(win,ui,"Paused")
            else:
                ui = set_info_text(win,ui,"")
            
        ms_times["input2"] = round(((time.time() - start_time)*1000)-ms_times["input1"])
            
        
        ## ## MOVEMENT CONTROLS ##    
        if inp == settings["keys"]["move_up"]["value"] or inp == "w":
            hero["direction"] = 180
            hero = move_hero(win,hero)
        elif inp == settings["keys"]["move_down"]["value"] or inp == "s":
            hero["direction"] = 0
            hero = move_hero(win,hero)
        elif inp == settings["keys"]["move_right"]["value"] or inp == "d":
            hero["direction"] = 90
            hero = move_hero(win,hero)
        elif inp == settings["keys"]["move_left"]["value"] or inp == "a":
            hero["direction"] = 270
            hero = move_hero(win,hero)
            
            
        ## ## OTHER CONTROLS ## ##
        elif inp == "x":
            for item in win.items:
                item.undraw()
            #print(win.items)
            ui = clear_playfield(win,mobs,ui)
        elif inp == "z":
            toggle_debug_ui(win,debug_ui)
        elif inp == "c":
            win.setBackground(settings["bg_flash"]["value"])
        #elif inp != "" and inp != None:
        #    pass
            #print(type(inp))
            #print(inp)
            #mouse = False
            
        ms_times["input3"] = round(((time.time() - start_time)*1000)-ms_times["input2"])
            
        ## FINALLY, UPDATE THE SCREEN ACCORDING TO FRAME RATE ##
        update(settings["frame_rate"]["value"])
        
        ## AND THEN CHECK FPS CALCULATIONS ##
        ms_times["update"] = round(((time.time() - start_time)*1000)-ms_times["input3"])
        string = str(ms_times)
        update_debug_ui(win,debug_ui,string)
        timer = time.time() - start_time
        last_ms = timer
        
        ### Calculate effective fps for this tick
        efps = int(1/timer)
        frames += efps
        ticks += 1
        avg_fps = frames/ticks
        if efps < lowest_fps:
            lowest_fps = efps
        
        ## Calculate average fps for past x ticks, where x is settings["frame_rate"]["value"] ##
        last_x_frames.append(efps)
        total_frames = 0
        if len(last_x_frames) >= settings["frame_rate"]["value"]:
            for i in range(0,len(last_x_frames)-1):
                total_frames += last_x_frames[i]
            recent_fps = total_frames/settings["frame_rate"]["value"]
            last_x_frames.remove(last_x_frames[0])
    return(score)
    

def farewell():
    #clear()
    reset_xset()
    save_high_scores()


init()
main()
farewell()

