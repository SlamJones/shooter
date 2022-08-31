#!/usr/bin/env python3

import random
import os
import math
import time

from graphics import GraphWin, Circle, Point, update, Rectangle, Text
from screeninfo import get_monitors


settings = {
    "window_x": {"value": 1280,"modifiable": False},
    "window_y": {"value": 960,"modifiable": False},
    "top_boundary": {"value": 100,"modifiable":False},
    "frame_rate": {"value": 30,"modifiable": True},
    "debug_mode": {"value": False,"modifiable": True},
    "bg_color": {"value": "black","modifiable": True},
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
    "keys": {"modifiable":True,    
        "move_up": {"value": "Up","modifiable": True},
        "move_down": {"value": "Down","modifiable": True},
        "move_left": {"value": "Left","modifiable": True},
        "move_right": {"value": "Right","modifiable": True},
        "shoot": {"value": "Control_L","modifiable": True},
        "pause": {"value": "p","modifiable": True},
        "switch_weapon": {"value": "Shift_L","modifiable": True},
    },
}


all_guns = [
    {"p_type":"Gun","name":"Shotgun","type":"Spread","use":"immediate","value":50,"tier":1,
     "decay_time":300,"decay":0,"passthru":0,
     "damage":0.5,"fire_rate":12,"angle":45,"n":7,"range":settings["projectile_max_distance"]["value"]/2},
    {"p_type":"Gun","name":"Shatter","type":"Shatter","use":"immediate","value":50,"tier":1,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":0,
     "damage":1,"fire_rate":6,"angle":30,"n":3,"range":settings["projectile_max_distance"]["value"]},
    {"p_type":"Gun","name":"Split","type":"Split","use":"immediate","value":50,"tier":1,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":0,
     "damage":1,"fire_rate":6,"angle":30,"n":3,"range":settings["projectile_max_distance"]["value"]},
    {"p_type":"Gun","name":"Wide","type":"Wide","use":"immediate","value":50,"tier":2,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":1,
     "damage":1,"fire_rate":6,"angle":10,"n":4,"range":settings["projectile_max_distance"]["value"]},
    {"p_type":"Gun","name":"Heavy Pistol","type":"Basic","use":"immediate","value":50,"tier":2,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":1,
     "damage":2,"fire_rate":9,"angle":30,"n":1,"range":settings["projectile_max_distance"]["value"]},
    {"p_type":"Gun","name":"Rifle","type":"Basic","use":"immediate","value":50,"tier":2,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":2,
     "damage":1,"fire_rate":9,"angle":30,"n":1,"range":settings["projectile_max_distance"]["value"]*2},
    {"p_type":"Gun","name":"Heavy Shotgun","type":"Spread","use":"immediate","value":50,"tier":2,
     "decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":1,
     "damage":1,"fire_rate":8,"angle":45,"n":7,"range":settings["projectile_max_distance"]["value"]/2},
    {"p_type":"Gun","name":"Split > Shatter","type":"Split > Shatter","use":"immediate","tier":2,
     "value":50,"decay_time":300,"decay":0,"hit_box":10,"border":5,"passthru":0,
     "damage":1,"fire_rate":6,"angle":30,"n":3,"range":settings["projectile_max_distance"]["value"]}
]


def clear():
    _ = os.system('clear')
    
    
def calculate_top_boundary():
    settings["top_boundary"]["value"] = settings["window_y"]["value"] / 10
    
    
def collect_screen_info():
    print("Monitor info:")
    try:
        for m in get_monitors():
            print(m)
        settings["window_x"]["value"] = m.width
        settings["window_y"]["value"] = m.height - 100
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
    hero["graphics"].setOutline(settings["hero_color"]["value"])
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
        
##def calculate_end_point(direction,speed,origin_x,origin_y):
        

def move_hero(win,hero):
    if check_hero_border(win,hero):
        move_x,move_y = calculate_move_xy(hero["direction"],settings["hero_speed"]["value"])
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
    hero["direction"] = 0
    hero["health"] = 3
    hero["damage"] = 1
    hero["fire_rate"] = 4
    max_dist = settings["projectile_max_distance"]["value"]
    #hero["gun"] = {"name":"Basic","type":"Basic","damage":1,"ammo":10000,"fire_rate":4}
    hero["guns"] = [{"name":"Basic Pistol","type":"Basic","damage": 1,"ammo":10000,
                     "fire_rate":4,"range":max_dist,"n":1,"passthru":0},
                    #{"name":"Spread","type":"Spread","damage":1,"ammo":10,
                    # "fire_rate":6,"angle":30,"n":3,"range":max_dist,"passthru":0},
                    #{"name":"Shotgun","type":"Spread","damage":0.5,"ammo":10000,
                    # "fire_rate":8,"angle":45,"n":7,"range":int(max_dist/2),"passthru":1},
                    #{"name": "Wide","type":"Wide","damage": 1, "ammo": 10000,
                    # "fire_rate": 6,"width":10,"n":3,"range":max_dist,"passthru":0},
                    #{"name": "Shatter","type":"Shatter","damage": 1, "ammo": 10000,
                    # "fire_rate": 6,"angle":30,"n":3,"range":max_dist,"passthru":0},
                    #{"name": "Split > Shatter","type":"Split > Shatter","damage": 1, "ammo": 10000,
                    # "fire_rate": 8,"range":max_dist,"passthru":0},
                   ]
    hero["gun"] = hero["guns"][0]
    hero["color"] = settings["hero_color"]["value"]
    hero["animation"] = []
    hero["tangible"] = True
    hero["boosts"] = []
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
    if spawn_side == "top":
        centerX = random.randrange(
            mob["radius"]+settings["top_boundary"]["value"],settings["window_x"]["value"]-mob["radius"])
        centerY = mob["radius"]+settings["top_boundary"]["value"]
    elif spawn_side == "bottom":
        centerX = random.randrange(mob["radius"],settings["window_x"]["value"]-mob["radius"])
        centerY = settings["window_y"]["value"]-mob["radius"]
    elif spawn_side == "left":
        centerX = mob["radius"]
        centerY = random.randrange(mob["radius"],settings["window_y"]["value"]-mob["radius"])
    elif spawn_side == "right":
        centerX = settings["window_x"]["value"]-mob["radius"]
        centerY = random.randrange(mob["radius"],settings["window_y"]["value"]-mob["radius"])
    
    mob["graphics"] = Circle(Point(centerX,centerY), mob["size"])
    mob["graphics"].setFill(mob["color"])
    mob["graphics"].setOutline("red")
    mob["graphics"].setWidth(border_width)
    to_draw.append(mob["graphics"])
    draw_to_draw(win,to_draw)
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
        if gun["ammo"] <= 0:
            if gun["name"] != "Basic":
                guns_copy.remove(gun)
                hero["guns"] = guns_copy
                hero = switch_weapons(hero)
                
            else:
                gun["ammo"] = 10000
    return(hero)
        
        
def set_damage(char):
    return(char["gun"]["damage"])
    

def fire_projectile(win,char):
    radius = settings["projectile_size"]["value"]
    char["gun"]["ammo"] -= 1
    #passthru = False
    passthru = char["gun"]["passthru"]
    char_dir = char["direction"]
    o = ""
    max_dist = char["gun"]["range"]
    #max_dist = settings["projectile_max_distance"]["value"]
    
    if char["gun"]["type"] == "Basic":
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o)]
        
    elif char["gun"]["type"] == "Spread":
        number = char["gun"]["n"]
        angle = char["gun"]["angle"]
        angles = calc_angles_from_max(number,angle)
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = []
        for i in range(number):
            projectile = spawn_projectile(
                win,char,ox,oy,radius,passthru,char_dir+angles[i],char["damage"],max_dist,o)
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
        projectile1 = spawn_projectile(win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o)
        projectile2 = spawn_projectile(win,char,ox2,oy2,radius,passthru,char_dir,char["damage"],max_dist,o)
        projectile3 = spawn_projectile(win,char,ox3,oy3,radius,passthru,char_dir,char["damage"],max_dist,o)
        projectiles = [projectile1,projectile2,projectile3]
        
    elif char["gun"]["type"] == "Big":
        radius = settings["projectile_size"]["value"]*3
        passthru = True
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o)]
    
    elif char["gun"]["type"] == "Split":
        o = [{"type":"split","delay":0,"projectiles":4,"recursion":0}]
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o)]
    
    elif char["gun"]["type"] == "Split (Recursive 1)":
        o = [{"type":"split","delay":0,"projectiles":4,"recursion":1}]
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o)]
    
    elif char["gun"]["type"] == "Shatter":
        o = [{"type":"shatter","delay":0,"projectiles":3,"max_angle":30,"recursion":0}]
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o)]
    
    elif char["gun"]["type"] == "Split Shatter":
        o = [{"type":"shatter","delay":0,"projectiles":3,"max_angle":30,"recursion":0},
            {"type":"split","delay":0,"projectiles":4,"recursion":0}]
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o)]
    
    elif char["gun"]["type"] == "Split > Shatter":
        o = [{"type":"shatter","delay":1,"projectiles":3,"max_angle":30,"recursion":0},
            {"type":"split","delay":0,"projectiles":4,"recursion":0}]
        ox,oy = char["graphics"].getCenter().getX(),char["graphics"].getCenter().getY()
        projectiles = [spawn_projectile(win,char,ox,oy,radius,passthru,char_dir,char["damage"],max_dist,o)]
        
    return(projectiles)
    
    
def spawn_projectile(win,origin,origin_x,origin_y,radius,passthru,direction,damage,max_dist,other):
    to_draw = []
    projectile = {}
    #origin_x, origin_y = origin["graphics"].getCenter().getX(),origin["graphics"].getCenter().getY()
    projectile["graphics"] = Circle(Point(origin_x,origin_y), radius)
    projectile["graphics"].setFill(settings["hero_color"]["value"])
    projectile["origin_x"],projectile["origin_y"] = origin_x,origin_y
    projectile["direction"] = direction
    projectile["damage"] = damage
    projectile["speed"] = settings["projectile_speed"]["value"]
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
                                    "type":"split","projectiles":4,"recursion":recursion,"delay":0}
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
                            #offset = hit[0]["graphics"].getRadius() + radius + 5
                            offset = hit[0]["radius"] + 5
                            passthru = hit[1]["passthru"]
                            max_dist = round(hit[1]["max_distance"]*0.75)
                            if settings["debug_mode"]["value"]:
                                print(instruction)
                                print(hit[1])
                            ox,oy = hit[0]["graphics"].getCenter().getX(),hit[0]["graphics"].getCenter().getY()
                            projectile_list = [
                                spawn_projectile(
                                    win,hit[1],ox,oy-offset,radius,passthru,180,hit[1]["damage"],max_dist,o),
                                spawn_projectile(
                                    win,hit[1],ox,oy+offset,radius,passthru,0,hit[1]["damage"],max_dist,o),
                                spawn_projectile(
                                    win,hit[1],ox+offset,oy,radius,passthru,90,hit[1]["damage"],max_dist,o),
                                spawn_projectile(
                                    win,hit[1],ox-offset,oy,radius,passthru,270,hit[1]["damage"],max_dist,o),]
                            for p in projectile_list:
                                projectiles.append(p)
                        if instruction["type"] == "shatter":
                            i_copy = instruction.copy()
                            max_angle = instruction["max_angle"]
                            if instruction["recursion"] > 0:
                                recursion = instruction["recursion"] - 1
                                instruction = {
                                    "type":"split","projectiles":4,"recursion":recursion,"max_angle":max_angle,"delay":0}
                            else:
                                instruction = {"type":"none","recursion":0,"max_angle":max_angle,"delay":0}
                            o = []
                            if len(hit[1]["other"]) > 1:
                                for i in hit[1]["other"]:
                                    if i != i_copy:
                                        #o.append(instruction)
                                        o.append(i)
                            o.append(instruction)
                            radius = hit[1]["graphics"].getRadius()
                            #offset = hit[0]["graphics"].getRadius() + radius + 5
                            offset=hit[0]["radius"] + 5
                            passthru = hit[1]["passthru"]
                            max_dist = round(hit[1]["max_distance"]*0.75)
                            if settings["debug_mode"]["value"]:
                                print(instruction)
                                print(hit[1])
                            ndir1 = hit[1]["direction"]
                            ndir2 = hit[1]["direction"] + instruction["max_angle"]
                            ndir3 = hit[1]["direction"] - instruction["max_angle"]
                            ox,oy = hit[0]["graphics"].getCenter().getX(),hit[0]["graphics"].getCenter().getY()
                            ox1,oy1 = calculate_end_point(ndir1,offset,ox,oy)
                            ox2,oy2 = calculate_end_point(ndir2,offset,ox,oy)
                            ox3,oy3 = calculate_end_point(ndir3,offset,ox,oy)
                            projectile_list = [
                                spawn_projectile(
                                    win,hit[1],ox1,oy1,radius,passthru,ndir1,hit[1]["damage"],max_dist,o),
                                spawn_projectile(
                                    win,hit[1],ox2,oy2,radius,passthru,ndir2,hit[1]["damage"],max_dist,o),
                                spawn_projectile(
                                    win,hit[1],ox3,oy3,radius,passthru,ndir3,hit[1]["damage"],max_dist,o)]
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
                        item["graphics"].undraw()
                        item["speed"] = 0
                    item["size"] += item["animation"]["step_value"]
                    size = item["size"]

                    item["graphics"] = Circle(
                        Point(item["graphics"].getCenter().getX(),item["graphics"].getCenter().getY()),size)
                    item_id = item["index"]
                    item["graphics"].setFill(settings["mob_splat_color"]["value"][item_id])
                    if instruction == "explode":
                        item["graphics"].setOutline(settings["mob_splat_color"]["value"][item_id])
                    elif instruction == "pop":
                        item["graphics"].setOutline(item["color"])
                    item["graphics"].draw(win)
                
                ## Once it has reached full size, remove it from items to help iteration speed ##
                if item["size"] >= item["animation"]["max_value"]:
                    item["delete"] = True
                    item["graphics"].setOutline(settings["mob_splat_color"]["value"][item_id])
                    if instruction == "pop":
                        pass
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
                else:
                    item["graphics"].setFill(item["color"])
                item["animation"]["tick"] += 1
                item["tangible"] = False
            elif instruction == "speed_flash":
                pass
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
    fps_box_center = [fps_box_x/2,fps_box_y/2]
    fps_box["box"] = Rectangle(Point(0,0),Point(fps_box_P2[0],fps_box_P2[1]))
    fps_box["box"].setFill(settings["bg_color"]["value"])
    fps_box["box"].setOutline(settings["fg_color"]["value"])
    to_draw.append(fps_box["box"])
    fps_box["text"] = Text(Point(fps_box_center[0],fps_box_center[1]),"")
    fps_box["text"].setTextColor(settings["fg_color"]["value"])
    to_draw.append(fps_box["text"])
    ui["fps_box"] = fps_box
    
    score_box = {}
    score_box_x,score_box_y = settings["window_x"]["value"]/10,settings["window_y"]["value"]/10
    score_box_P1 = [settings["window_x"]["value"],0]
    score_box_P2 = [settings["window_x"]["value"]*0.9,settings["window_y"]["value"]/10]
    score_box_center = [(score_box_P1[0] + score_box_P2[0]) / 2,(score_box_P1[1] + score_box_P2[1]) / 2]
    score_box["box"] = Rectangle(
        Point(score_box_P1[0],score_box_P1[1]),Point(score_box_P2[0],score_box_P2[1]))
    score_box["box"].setFill(settings["bg_color"]["value"])
    score_box["box"].setOutline(settings["fg_color"]["value"])
    to_draw.append(score_box["box"])
    score_box["text"] = Text(Point(score_box_center[0],score_box_center[1]),"")
    score_box["text"].setTextColor(settings["fg_color"]["value"])
    score_box["text"].setSize(20)
    to_draw.append(score_box["text"])
    ui["score_box"] = score_box
    
    weapon_box = {}
    weapon_box_x,weapon_box_y = settings["window_x"]["value"]*0.15,settings["window_y"]["value"]/10
    weapon_box_P1 = [score_box_P2[0],0]
    weapon_box_P2 = [score_box_P2[0]-weapon_box_x,settings["window_y"]["value"]/10]
    weapon_box_center = [
        (weapon_box_P1[0] + weapon_box_P2[0]) / 2,(weapon_box_P1[1] + weapon_box_P2[1]) / 2]
    weapon_box["box"] = Rectangle(
        Point(weapon_box_P1[0],weapon_box_P1[1]),Point(weapon_box_P2[0],weapon_box_P2[1]))
    weapon_box["box"].setFill(settings["bg_color"]["value"])
    weapon_box["box"].setOutline(settings["fg_color"]["value"])
    to_draw.append(weapon_box["box"])
    weapon_box["text"] = Text(Point(weapon_box_center[0],weapon_box_center[1]),"")
    weapon_box["text"].setTextColor(settings["fg_color"]["value"])
    weapon_box["text"].setSize(18)
    to_draw.append(weapon_box["text"])
    ui["weapon_box"] = weapon_box
    
    hp_box = {}
    hp_box_x,hp_box_y = settings["window_x"]["value"]*0.1,settings["window_y"]["value"]/10
    hp_box_P1 = [weapon_box_P2[0],0]
    hp_box_P2 = [weapon_box_P2[0]-hp_box_x,settings["window_y"]["value"]/10]
    hp_box_center = [
        (hp_box_P1[0] + hp_box_P2[0]) / 2,(hp_box_P1[1] + hp_box_P2[1]) / 2]
    hp_box["box"] = Rectangle(
        Point(hp_box_P1[0],hp_box_P1[1]),Point(hp_box_P2[0],hp_box_P2[1]))
    hp_box["box"].setFill(settings["bg_color"]["value"])
    hp_box["box"].setOutline(settings["fg_color"]["value"])
    to_draw.append(hp_box["box"])
    hp_box["text"] = Text(Point(hp_box_center[0],hp_box_center[1]),"")
    hp_box["text"].setTextColor(settings["fg_color"]["value"])
    hp_box["text"].setSize(18)
    to_draw.append(hp_box["text"])
    ui["hp_box"] = hp_box
    
    count_box = {}
    count_box_x,count_box_y = settings["window_x"]["value"]*0.1,settings["window_y"]["value"]/10
    count_box_P1 = [fps_box_P2[0],0]
    count_box_P2 = [fps_box_P2[0]+count_box_x,settings["window_y"]["value"]/10]
    count_box_center = [
        (count_box_P1[0] + count_box_P2[0]) / 2,(count_box_P1[1] + count_box_P2[1]) / 2]
    count_box["box"] = Rectangle(
        Point(count_box_P1[0],count_box_P1[1]),Point(count_box_P2[0],count_box_P2[1]))
    count_box["box"].setFill(settings["bg_color"]["value"])
    count_box["box"].setOutline(settings["fg_color"]["value"])
    to_draw.append(count_box["box"])
    count_box["text"] = Text(Point(count_box_center[0],count_box_center[1]),"")
    count_box["text"].setTextColor(settings["fg_color"]["value"])
    count_box["text"].setSize(14)
    to_draw.append(count_box["text"])
    ui["count_box"] = count_box
    
    info_box = {}
    info_box_x,score_box_y = settings["window_x"]["value"]*0.8,settings["window_y"]["value"]/10
    info_box_P1 = [hp_box_P2[0],0]
    info_box_P2 = [count_box_P2[0],settings["window_y"]["value"]/10]
    #info_box_P2 = [weapon_box_P2[0]-info_box_x,settings["window_y"]["value"]/10]
    info_box_center = [(info_box_P1[0] + info_box_P2[0]) / 2,(info_box_P1[1] + info_box_P2[1]) / 2]
    info_box["box"] = Rectangle(
        Point(info_box_P1[0],info_box_P1[1]),Point(info_box_P2[0],info_box_P2[1]))
    info_box["box"].setFill(settings["bg_color"]["value"])
    info_box["box"].setOutline(settings["fg_color"]["value"])
    to_draw.append(info_box["box"])
    info_box["text"] = Text(Point(info_box_center[0],info_box_center[1]),"")
    info_box["text"].setTextColor(settings["fg_color"]["value"])
    info_box["text"].setSize(24)
    to_draw.append(info_box["text"])
    ui["info_box"] = info_box
    
    draw_to_draw(win,to_draw)
    return(ui)


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


def low_fps_factor(fps,target_fps):
    return(target_fps/fps)


def return_higher(a,b):
    if a > b:
        return(a)
    return(b)


def pickup_spawn_controller(win,hero,pickups,score):
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
            pickup = spawn_pickup(origin_x,origin_y,tier)
            pickups.append(pickup)
            pickup["graphics"].draw(win)
    return(pickups)


def spawn_pickup(origin_x,origin_y,tier):
    roll = random.randrange(0,100)
    max_dist = settings["projectile_max_distance"]["value"]
    if roll >= 75:
        pickup = {"p_type":"Health","name":"HP+1","use":"immediate","value":1,
                  "decay_time":300,"decay":0,"hit_box":20,"border":5}
        pickup["radius"] = pickup["hit_box"]+pickup["border"]
        fill,outline = "red","cyan"
    else:
        gun_choices = []
        fill,outline = "green3","cyan"
        max_roll = 100
        gun_roll = random.randrange(0,max_roll)
        
        for gun in all_guns:
            if gun["tier"] <= tier:
                gun_choices.append(gun)
        
        pickup = random.choice(gun_choices)
        pickup["hit_box"] = 15
        pickup["border"] = 5
        pickup["radius"] = pickup["hit_box"]+pickup["border"]
        
    if origin_x <= pickup["radius"]:
        origin_x = pickup["radius"]+5
    elif origin_x >= settings["window_x"]["value"]-pickup["radius"]:
        origin_x = settings["window_x"]["value"]-pickup["radius"]-5
        
    if origin_y <= pickup["radius"]:
        origin_y = pickup["radius"]+5
    elif origin_y >= settings["window_y"]["value"]-pickup["radius"]:
        origin_y = settings["window_y"]["value"]-pickup["radius"]-5
            
    pickup["graphics"] = Circle(Point(origin_x,origin_y),pickup["hit_box"])
    pickup["graphics"].setFill(fill)
    pickup["graphics"].setOutline(outline)
    pickup["graphics"].setWidth(pickup["border"])
    pickup["decay"] = 0
    print("New pickup: {}".format(pickup))
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
                "name":pickup["name"],"type":pickup["type"],"damage":pickup["damage"],"ammo":pickup["value"],
                "fire_rate":pickup["fire_rate"],"angle":pickup["angle"],"range":pickup["range"],
                "passthru": pickup["passthru"],"n":pickup["n"]}
            hero["guns"].append(gun)
            hero["gun"] = gun
            hero = set_hero_gun_settings(hero,gun)
        info_string="Picked up {}! +{} ammo".format(pickup["name"],pickup["value"])
    elif pickup["p_type"] == "Health":
        hero["health"] += pickup["value"]
        info_string="Health increased! (+{})".format(pickup["value"])
    return(hero,info_string)


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

    
def init():
    clear()
    collect_screen_info()
    calculate_top_boundary()
    
    
def main():
    win = open_window()
    hero = build_hero(win)
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
    start_time = time.time()
    mob_speed = settings["mob_speed"]["value"]
    text_queue = []
    pickups = []
    ui = build_ui(win)
    fps_factor = 1.0
    
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
        
        projectiles = move_projectiles(win,projectiles)
        ## PROCESS MOVEMENT AND STUFF ##
        ## Take a copy of the mobs list before we modify it for this tick ##
        mobs_before = mobs.copy()
        projectiles,mobs = check_for_projectile_hits(win,projectiles,mobs)
        mobs = move_mobs(win,mobs,hero)
        hero = check_hero_mob_collisions(win,hero,mobs)
        if len(hero["animation"]) > 0:
            hero["tangible"] = False
        else:
            hero["tangible"] = True
        
        ## Process current pickups, start counter for spawning a new one if needed ##
        hero,pickups,info_string = check_pickup_collision(win,hero,pickups)
        if info_string != "":
            text_queue=[(timed_info_text(info_string,45))]
        hero = check_hero_ammo(hero)
        pickups = calc_pickups_decay(pickups)
        pickups = pickup_spawn_controller(win,hero,pickups,score)
        
        ## Process animations once we have checked for and collected collisions ##
        ui,text_queue = text_animation_queue(win,ui,text_queue)
        mobs.append(hero)
        mobs = animation_queue(win,mobs)
        mobs.remove(hero)
        
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
        
        ## Check if player can shoot ##
        shoot_ticks += 1
        if shoot_ticks >= hero["fire_rate"]:
            shoot=True
        else:
            shoot=False
            
        ## THEN, PROCESS PLAYER CONTROLS ##
        if pause:
            win.getKey()
        elif not mouse and not pause:
            inp = win.checkKey()
        elif mouse and not pause:
            inp = win.checkMouse()
        if settings["debug_mode"]["value"] and inp != "":
            print(inp)
            
        ## BASIC CONTROLS ##
        ## ESCAPE
        if inp == "Escape":
            play=False
        ## SHOOT
        if inp == settings["keys"]["shoot"]["value"]:
            if shoot:
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
            if pause:
                ui = set_info_text(win,ui,"Paused")
            else:
                ui = set_info_text(win,ui,"")
            
        
        ## ## MOVEMENT CONTROLS ##    
        elif inp == settings["keys"]["move_up"]["value"]:
            hero["direction"] = 180
            hero = move_hero(win,hero)
        elif inp == settings["keys"]["move_down"]["value"]:
            hero["direction"] = 0
            hero = move_hero(win,hero)
        elif inp == settings["keys"]["move_right"]["value"]:
            hero["direction"] = 90
            hero = move_hero(win,hero)
        elif inp == settings["keys"]["move_left"]["value"]:
            hero["direction"] = 270
            hero = move_hero(win,hero)
        elif inp != "" and inp != None:
            print(type(inp))
            print(inp)
            mouse = False

            
        ## FINALLY, UPDATE THE SCREEN ACCORDING TO FRAME RATE ##
        update(settings["frame_rate"]["value"])
        
        ## AND THEN CHECK FPS CALCULATIONS ##
        timer = time.time() - start_time
        last_ms = timer
        
        ### Calculate effective fps for this tick
        efps = int(1/timer)
        frames += efps
        ticks += 1
        avg_fps = frames/ticks
        if efps < lowest_fps:
            lowest_fps = efps
        last_x_frames.append(efps)
        total_frames = 0
        if len(last_x_frames) >= settings["frame_rate"]["value"]:
            for i in range(0,len(last_x_frames)-1):
                total_frames += last_x_frames[i]
            recent_fps = total_frames/settings["frame_rate"]["value"]
            last_x_frames.remove(last_x_frames[0])
    

def farewell():
    clear()


init()
main()
farewell()

