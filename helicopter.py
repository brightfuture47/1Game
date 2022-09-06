from utils import randcell1
import os


CELL_TYPES = {'WB' : '\U0001F4A7', 'CUP' : '\U0001F3C6', 'HEART': '\U0001F49B'}

class Helicopter:

    def __init__(self, w, h):
        rc = randcell1(w, h)
        rx, ry = rc[0], rc[1]
        self.h = h
        self.w = w
        self.x = rx
        self.y = ry
        self.mxtank = 1
        self.tank = 0
        self.score = 0
        self.lives = 20

    
    def move(self, dx,dy):
        nx, ny = dx + self.x, dy + self.y
        if (nx >=0 and ny >= 0 and nx < self.h and ny < self.w):
            self.x, self.y = nx, ny
    
    def print_stats(self):
        print(CELL_TYPES['WB'], self.tank, "/", self.mxtank, sep="", end = "|")
        print(CELL_TYPES['CUP'], self.score,  end = "|")
        print(CELL_TYPES['HEART'], self.lives)
        
    
    def game_over(self):
        os.system("cls")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("X X X X X X         X X X X X  X")
        print("X  GAME OVER, YOUR SCORE IS", self.maxScore, " X")
        print("X X X X X X         X X X X X  X")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        exit(0)
    
    
    def export_data(self):
        return {
            "score": self.score,
            "lives": self.lives,
            "x": self.x, "y": self.y,
            "tank": self.tank,
            "mxtank": self.mxtank
        }
    
    def import_data(self, data):
        self.x, self.y = data["x"] or 0, data["y"] or 0
        self.tank = data["tank"] or 0
        self.mxtank = data["mxtank"] or 1
        self.score = data["score"] or 0
        self.lives = data["lives"] or 10