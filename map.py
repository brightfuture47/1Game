from pickle import TRUE
from clouds import Clouds
from utils import randbool
from utils import randcell
from utils import randcell1
from utils import randcell2



CELL_TYPES = ['\U0001F7E9', '\U0001F332', '\U0001F30A', '\U0001F3E5', '\U0001F3EB', '\U00002B1B', '\U0001F525', '\U0001F681', '\U000026FD', '\U0001F3E5', '\U000026AA', '\U0001F300']
TREE_BONUS = 100
UPGRADE_COST = 200
LIFE_COST = 400

EMPTY = 0
TREE = 1
RIVER = 2
BOUND = 5
FIRE = 6
HILICOPTER = 7
SHOP = 8
HOSP = 9
CLOUD = 10
SIKLON = 11


class Map:

    def __init__(self, w,h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generate_forest(3,10)

        self.generate_river(7)
        self.generate_river(10)
        self.generate_river(20)
        self.add_fire()
        self.add_fire()
        self.add_fire()
        self.add_fire()
        self.add_fire()
        self.generate_upgrade_shop()
        self.generate_upgrade_hosp()


    
    def print_map(self, helico, clouds):
        print(CELL_TYPES[BOUND] * (self.w + 2))
        for ri in range(self.h):
            print(CELL_TYPES[BOUND], end="")
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if (clouds.cells[ri][ci] == 1):
                    print(CELL_TYPES[CLOUD], end="")
                elif (clouds.cells[ri][ci] == 2):
                    print(CELL_TYPES[SIKLON], end="")
                elif (helico.x == ri and helico.y == ci):
                    print(CELL_TYPES[HILICOPTER], end="")
                elif (cell >= 0 and cell < len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end="")
            print(CELL_TYPES[BOUND])
        print(CELL_TYPES[BOUND] * (self.w + 2))

    
    def check_bounds(self, x,y):
        if(x < 0 or y < 0 or x >= self.h or y >= self.w):
            return False
        return True

    def generate_river(self, l):
        rc = randcell(self.cells, RIVER, self.w, self.h)
        rx, ry = rc[0], rc[1]
        self.cells[rx][ry] = RIVER
        while l > 0:
            rc2 = randcell2(self.cells, RIVER, rx, ry)
            rx2, ry2 = rc2[0], rc2[1]
            if self.check_bounds(rx2, ry2):
                self.cells[rx2][ry2] = RIVER
                rx, ry = rx2, ry2
                l -= 1

    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if (randbool(r,mxr)):
                    self.cells[ri][ci] = 1    
    
    def generate_tree(self):
        c = randcell1(self.w, self.h)
        cx, cy = c[0], c[1]
        if (self.check_bounds(cx,cy) and self.cells[cx][cy] == EMPTY):
            self.cells[cx][cy] = TREE
    
    def generate_upgrade_shop(self):
        c = randcell1(self.w, self.h)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] = SHOP

    def generate_upgrade_hosp(self):
        c = randcell1(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] != SHOP:
            self.cells[cx][cy] = HOSP
    
    def add_fire(self):
        c = randcell1(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == TREE:
            self.cells[cx][cy] = FIRE
    
    def update_fires(self):
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == FIRE:
                    self.cells[ri][ci] = EMPTY
        for i in range(5):
            self.add_fire()
    
    def process_helicopter(self, helico, clouds):
        c = self.cells[helico.x][helico.y]
        d = clouds.cells[helico.x][helico.y]
        if (c == RIVER):
            helico.tank = helico.mxtank
        if(c == FIRE and helico.tank > 0):
            helico.tank -= 1
            self.cells[helico.x][helico.y] = TREE
            helico.score += TREE_BONUS
        if(c == SHOP and helico.score >= UPGRADE_COST):
            helico.mxtank += 1
            helico.score -= UPGRADE_COST
        if(c == HOSP and helico.score >= LIFE_COST):
            helico.lives += 5
            helico.score -= LIFE_COST
        if (d == 2):
            helico.lives -= 1
            if helico.lives == 0:
                helico.game_over()
    
    def export_data(self):
        return {"cells" : self.cells}
    
    def import_data(self, data):
        self.cells = data['cells'] or [[0 for i in range(self.w)] for j in range(self.h)]