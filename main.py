import imp
import time
import os
import json

from multiprocessing.connection import Listener
from operator import imod
from clouds import Clouds
from map import Map
from helicopter import Helicopter as Helico
from pynput import keyboard

TICK_SLEEP = 0.1
TREE_UPDATE = 10
FIRE_UPDATE = 20
CLOUDS_UPDATE = 22
MAP_W, MAP_H = 20,10

field = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
helico = Helico(MAP_W, MAP_H)
MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1,0), 'a': (0, -1)}
# f - сохранить g - загрузить

tick = 1


def on_press(key):
    try:
        global helico, tick, clouds, field
        c = key.char.lower()
        
        if c in MOVES.keys():
            dx, dy = MOVES[c][0], MOVES[c][1]
            helico.move(dx,dy)
            
        elif c == 'f':
            data = {
                "helicopter": helico.export_data(),
                "clouds": clouds.export_data(),
                "fields": field.export_data(),
                'tick' : tick
                }
            with open("level.json", "w") as lvl:
                json.dump(data, lvl)
        
        elif c == 'g':
            with open('level.json', 'r') as lvl:
                data = json.loads(lvl)
                helico.import_data(data['helicopter'])
                clouds.import_data(data['clouds'])
                field.import_data(data['fields'])
                tick = data['tick'] or 1 

        
    except AttributeError:
        print('special key {0} pressed '.format(key))


listener = keyboard.Listener(
    on_press=on_press
    )
listener.start()


while True:
   
    os.system("cls")

    print("Tick:", tick)    
   
    field.process_helicopter(helico, clouds)
    
    helico.print_stats()
    
    field.print_map(helico, clouds)
    
    tick += 1
    
    time.sleep(TICK_SLEEP)
    
    if (tick % TREE_UPDATE == 0):
        field.generate_tree()
    
    if (tick % FIRE_UPDATE == 0):
        field.update_fires()
    
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update()