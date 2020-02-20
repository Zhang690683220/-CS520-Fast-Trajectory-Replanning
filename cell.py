import random

class Cell:
    def __init__(self, x, y):
        
        self.x = x
        self.y = y
        self.visited = False
        self.blocked = False
        self.explored = False
        self.color = 0
        self.neighbor = {
            "left" : 0,
            "right" : 0,
            "up" : 0,
            "down" : 0
        }
        self.search = 0
        self.g = 0
        self.h = 0
        self.treeptr = None

    def f(self):
        return self.g + self.h

    def f_large_g(self):
        return 300*self.f()- self.g

    def f_small_g(self):
        return 300*self.f()+ self.g
    
    def dfs(self, s):
        if self.explored == False:
            self.explored = True
            rand = random.randint(0, 99)
            if rand < 70:
                self.blocked = False
            else:
                self.blocked = True
            for n in self.neighbor:
                if self.neighbor[n] != None and self.neighbor[n].explored == False:
                    self.neighbor[n].dfs(s)




