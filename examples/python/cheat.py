from graphics import *

# Id to color mapping
nameToColor = {
    "DoomPlayer": "blue",

    "Medikit": "green",
    "Stimpack": "green",

    "HealthBonus": "dark green",
    "ArmorBonus": "dark green",

    "GreenArmor": "lime green",
    "BlueArmor": "lime green",

    "ClipBox": "red",
    "ShellBox": "red",
    "RocketBox": "red",
    "CellPack": "red",

    "Chainsaw": "purple",
    "RocketLauncher": "purple",
    "SuperShotgun": "purple",
    "PlasmaRifle": "purple",
    "Chaingun": "purple",

    "Zombieman": "saddle brown",
    "ChaingunGuy": "saddle brown",
    "ShotgunGuy": "saddle brown",
    "ScriptedMarine": "saddle brown",
    "BaronOfHell": "saddle brown",
    "Demon": "saddle brown",
    "DoomImp": "saddle brown",
    "Cacodemon": "saddle brown",


    # we may want these at some point
    "Rocket": "white",
    "PlasmaBall": "white",
    "BaronBall": "white",
    "DoomImpBall": "white",

    # We don't want these
    "TeleportFog": "white",
    "Blood": "white",
    "BulletPuff": "white",
    "RocketSmokeTrail": "white",
}

# Map init
screen_width, screen_height = 512.0, 512.0
screen_border_x, screen_border_y = 20.0,20.0

# Prevent redoing the same things again and again
win = None
wall_plotted = False
plotted_walls = []
scale_x, scale_y, pad_x, pad_y = None, None, None, None
obj_list = []


def info_print(game):
    info_wall_print(game)
    info_thing_print(game)

def info_wall_print(game):
    print(info_wall_str(game))

def info_thing_print(game):
    print(info_thing_str(game))

def info_wall_str(game):
    output = ""
    wall_count = game.get_wall_count()
    output += "Nb walls: "+str(wall_count)+"\n"
    for j in range(0,wall_count):
        output += "Wall "+str(j)+" seen: "+str(game.get_wall_seen(j))+" starts at ("+str(game.get_wall_start_pos_x(j))+";"+str(game.get_wall_start_pos_y(j))+") and ends at ("+str(game.get_wall_end_pos_x(j))+";"+str(game.get_wall_end_pos_y(j))+")"+"\n"
    return output

def info_thing_str(game):
    output = ""
    thing_count = game.get_thing_count()
    output += "Nb thing: "+str(thing_count)+"\n"
    for j in range(0, thing_count):
        output += "Thing "+str(j)+" is at ("+str(game.get_thing_pos_x(j))+";"+str(game.get_thing_pos_y(j))+"), has id "+str(game.get_thing_type(j))+" and is named: "+game.get_thing_name(j)+"\n"
    return output

def plot_map(game, partial_walls=False, only_visible_things=False):
    global wall_plotted, plotted_walls
    global scale_x, scale_y, pad_x, pad_y
    global obj_list

    global win
    if not win:
        win = GraphWin("Map", screen_width, screen_height)

    wall_count = game.get_wall_count()

    if not wall_plotted:
        # Compute min and max values for the map
        map_x_min, map_x_max = 0, 0
        map_y_min, map_y_max = 0, 0
        for j in range(0,wall_count):
            if(game.get_wall_start_pos_x(j) < map_x_min):
                map_x_min = game.get_wall_start_pos_x(j)
            if(game.get_wall_end_pos_x(j) < map_x_min):
                map_x_min = game.get_wall_end_pos_x(j)
            if(game.get_wall_start_pos_y(j) < map_y_min):
                map_y_min = game.get_wall_start_pos_y(j)
            if(game.get_wall_end_pos_y(j) < map_y_min):
                map_y_min = game.get_wall_end_pos_y(j)

            if(game.get_wall_start_pos_x(j) > map_x_max):
                map_x_max = game.get_wall_start_pos_x(j)
            if(game.get_wall_end_pos_x(j) > map_x_max):
                map_x_max = game.get_wall_end_pos_x(j)
            if(game.get_wall_start_pos_y(j) > map_y_max):
                map_y_max = game.get_wall_start_pos_y(j)
            if(game.get_wall_end_pos_y(j) > map_y_max):
                map_y_max = game.get_wall_end_pos_y(j)

        map_width = map_x_max - map_x_min
        map_height = map_y_max - map_y_min
        map_offset_x = -map_x_min
        map_offset_y = -map_y_min

        # Scaling
        scale_x = (screen_width-screen_border_x) / map_width
        scale_y = (screen_height-screen_border_y) / map_height
        pad_x = screen_border_x/2 + map_offset_x * scale_x
        pad_y = screen_border_y/2 + map_offset_y * scale_y

        # Add the walls
        for j in range(0,wall_count):
            if j in plotted_walls:
                continue
            if (not partial_walls) or game.get_wall_seen(j):
                sx = game.get_wall_start_pos_x(j) * scale_x + pad_x
                sy = game.get_wall_start_pos_y(j) * scale_y + pad_y
                ex = game.get_wall_end_pos_x(j) * scale_x + pad_x
                ey = game.get_wall_end_pos_y(j) * scale_y + pad_y

                line = Line(Point(sx,sy), Point(ex,ey))
                line.draw(win)
                plotted_walls.append(j)

        if not partial_walls:
            wall_plotted = True

    # Remove
    while obj_list:
        item = obj_list.pop()
        item.undraw()

    # Add the new things
    thing_count = game.get_thing_count()
    for j in range(0, thing_count):
        thingName = game.get_thing_name(j)
        if only_visible_things and not game.get_thing_is_visible(j):
            # Special case for the Player that we should always display
            if thingName != "DoomPlayer":
                continue
        if thingName in nameToColor.keys():
            if nameToColor[thingName] == "white":
                continue
            x = game.get_thing_pos_x(j) * scale_x + pad_x
            y = game.get_thing_pos_y(j) * scale_y + pad_y
            circle = Circle(Point(x, y), 10*scale_x)
            circle.setFill(nameToColor[thingName])
            circle.draw(win)
            obj_list.append(circle)
        else:
            print(thingName+" is unknown !!")
