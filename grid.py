from minheap import *
from cell import *
import sys
import time
sys.setrecursionlimit(1000000)

class Grid(object):
    """docstring for Grid"""
    def __init__(self, nx, ny):
        super(Grid, self).__init__()
        self.nx = nx
        self.ny = ny
        self.start_time= 0
        self.end_time = 0
        self.calc_time = 0
        self.calc_large_g_time = 0
        self.calc_small_g_time = 0
        self.count = 0
        self.cells = []
        self.frame = 0
        self.path_plan_list = []
        self.path_plan_center = []
        self.move_list = []

        for i in range(self.nx):
            self.cells.append([])
            for j in range(self.ny):
                self.cells[i].append(Cell(i,j))

        init_set = set()

        for j in range(self.ny):
            for i in range(self.nx):
                if self.cells[i][j].x == 0:
                    self.cells[i][j].neighbor["left"] = None
                else:
                    self.cells[i][j].neighbor["left"] = self.cells[i-1][j]

                if self.cells[i][j].x == self.nx-1:
                    self.cells[i][j].neighbor["right"] = None
                else:
                    self.cells[i][j].neighbor["right"] = self.cells[i+1][j]

                if self.cells[i][j].y == 0:
                    self.cells[i][j].neighbor["down"] = None
                else:
                    self.cells[i][j].neighbor["down"] = self.cells[i][j-1]

                if self.cells[i][j].y == self.ny-1:
                    self.cells[i][j].neighbor["up"] = None
                else:
                    self.cells[i][j].neighbor["up"] = self.cells[i][j+1]

                init_set.add(self.cells[i][j])

        #print("init...block")
        start_rand_x = random.randint(0, self.nx-1)
        start_rand_y = random.randint(0, self.ny-1)

        self.start = self.cells[start_rand_x][start_rand_y]
        self.start.blocked = False
        self.start.explored = True
        init_set.remove(self.start)

        goal_rand_x = random.randint(0, self.nx-1)
        goal_rand_y = random.randint(0, self.ny-1)

        while(start_rand_x == goal_rand_x and start_rand_y == goal_rand_y):
            goal_rand_x = random.randint(0, self.nx-1)
            goal_rand_y = random.randint(0, self.ny-1)

        self.goal =  self.cells[goal_rand_x][goal_rand_y]
        self.goal.blocked = False
        self.goal.explored = True
        init_set.remove(self.goal)

        while(len(init_set) > 0):
            rand = init_set.pop()
            rand.dfs(init_set)

    def visual_frame(self, s, c):
        if s == "path_plan_center":
            self.path_plan_center.append([])
            self.path_plan_center[self.frame].append((c.x, c.y))
            self.path_plan_list.append([])
            self.move_list.append([])
        if s == "path_plan_list":
            self.path_plan_center.append([])
            self.path_plan_list.append([])
            self.path_plan_list[self.frame].append((c.x, c.y))
            self.move_list.append([])
        if s == "move_list":
            self.path_plan_center.append([])
            self.path_plan_list.append([])
            self.move_list.append([])
            self.move_list[self.frame].append((c.x, c.y))
        self.frame += 1

    def repeated_forward_astar(self):
        self.start_time = time.time()
        self.count = 0
        print("set h")
        for vector in self.cells:
            for c in vector:
                c.h = abs(c.x - self.goal.x) + abs(c.y - self.goal.y)

        self.goal.g = float("inf")

        state = self.start

        while(state.x != self.goal.x or state.y != self.goal.y):
            print(self.count)
            self.count += 1
            state.g = 0
            state.search = self.count
            self.goal.search = self.count

            openlist = []
            closelist = []
            heap = MinHeap(openlist)
            heap.insert(state)

            self.visual_frame("path_plan_list", state)

            print("debug1")
            while self.goal.g > heap.min().f():
                potential_state = heap.extract_min()
                self.visual_frame("path_plan_center", potential_state)
                closelist.append(potential_state)
                print("debug2")
                print(potential_state)
                for n in potential_state.neighbor:
                    if potential_state.neighbor[n] != None and not potential_state.neighbor[n] in closelist:
                        if potential_state.neighbor[n].search < self.count:
                            potential_state.neighbor[n].g = float("inf")
                            potential_state.neighbor[n].search = self.count
                        if (not potential_state.neighbor[n].blocked):
                            if potential_state.neighbor[n].g > potential_state.g + 1:
                                potential_state.neighbor[n].g = potential_state.g + 1
                                potential_state.neighbor[n].treeptr = potential_state
                                print("--------")
                                print(potential_state.neighbor[n].treeptr)

                                if potential_state.neighbor[n] in heap.list:
                                    heap.decrease_key(heap.list.index(potential_state.neighbor[n]), potential_state.neighbor[n].g)
                                else:
                                    heap.insert(potential_state.neighbor[n])
                            
                                self.visual_frame("path_plan_list", potential_state.neighbor[n])

            if len(heap.list) == 0:
                print("Cannot reach the target")
                return 1

            print(self.goal.treeptr)

            back = self.goal
            print("goal")
            print(self.goal.x,self.goal.y)
            trace_list = []
            print(back)
            print(self.goal)
            while back.x != state.x or back.y != state.y:
                trace_list.append(back)
                back = back.treeptr
            print(len(trace_list))

            print("back pointer")
            print(back.x, back.y)
            print(back)

            print("state")
            print(state.x, state.y)
            print(state)
            print("start")
            print(self.start.x, self.start.y)
            print(self.start)

            trace_list.reverse()
            print(trace_list[len(trace_list)-1]==self.goal)
            print(trace_list[0]==state)
            print(len(trace_list))

            i = 1
            while i<len(trace_list) and not trace_list[i].blocked:
                state = trace_list[i-1]
                self.visual_frame("move_list", state)
                print(i)
                i += 1
            if i == len(trace_list):
                state = self.goal
                print("final state")
                print(state.x, state.y)

        self.end_time = time.time()
        self.calc_time = self.end_time- self.start_time
        return 0

    def repeated_forward_astar_large_g(self):
        self.start_time = time.time()
        self.count = 0
        print("set h")
        for vector in self.cells:
            for c in vector:
                c.h = abs(c.x - self.goal.x) + abs(c.y - self.goal.y)

        self.goal.g = float("inf")

        state = self.start

        while(state.x != self.goal.x or state.y != self.goal.y):
            print(self.count)
            self.count += 1
            state.g = 0
            state.search = self.count
            self.goal.search = self.count

            openlist = []
            closelist = []
            heap = MinHeap_Large_g(openlist)
            heap.insert(state)

            self.visual_frame("path_plan_list", state)

            print("debug1")
            while self.goal.g > heap.min().f():
                potential_state = heap.extract_min()
                if potential_state in heap.list:
                    heap.list.remove(potential_state)
                self.visual_frame("path_plan_center", potential_state)
                closelist.append(potential_state)
                print("debug2")
                print(potential_state)
                for n in potential_state.neighbor:
                    if potential_state.neighbor[n] != None and not potential_state.neighbor[n] in closelist:
                        if potential_state.neighbor[n].search < self.count:
                            potential_state.neighbor[n].g = float("inf")
                            potential_state.neighbor[n].search = self.count
                        if (not potential_state.neighbor[n].blocked):
                            if potential_state.neighbor[n].g > potential_state.g + 1:
                                potential_state.neighbor[n].g = potential_state.g + 1
                                potential_state.neighbor[n].treeptr = potential_state
                                print("--------")
                                print(potential_state.neighbor[n].treeptr)

                                if potential_state.neighbor[n] in heap.list:
                                    heap.decrease_key(heap.list.index(potential_state.neighbor[n]), potential_state.neighbor[n].g)
                                else:
                                    heap.insert(potential_state.neighbor[n])
                            
                                self.visual_frame("path_plan_list", potential_state.neighbor[n])

            if len(heap.list) == 0:
                println("Cannot reach the target")
                return 1

            print(self.goal.treeptr)

            back = self.goal
            print("goal")
            print(self.goal.x,self.goal.y)
            trace_list = []
            print(back)
            print(self.goal)
            while back.x != state.x or back.y != state.y:
                print("state")
                print(state)
                print(state.x, state.y)
                print("back")
                print(back.treeptr)
                print(back.x, back.y)
                trace_list.append(back)
                back = back.treeptr
            print(len(trace_list))

            print("back pointer")
            print(back.x, back.y)
            print(back)

            print("state")
            print(state.x, state.y)
            print(state)
            print("start")
            print(self.start.x, self.start.y)
            print(self.start)

            trace_list.reverse()
            print(trace_list[len(trace_list)-1]==self.goal)
            print(trace_list[0]==state)
            print(len(trace_list))

            i = 1
            while i<len(trace_list) and not trace_list[i].blocked:
                state = trace_list[i-1]
                self.visual_frame("move_list", state)
                print(i)
                i += 1
            if i == len(trace_list):
                state = self.goal
                print("final state")
                print(state.x, state.y)

        self.end_time = time.time()
        self.calc_large_g_time = self.end_time- self.start_time
        return 0

    def repeated_forward_astar_small_g(self):
        self.start_time = time.time()
        self.count = 0
        print("set h")
        for vector in self.cells:
            for c in vector:
                c.h = abs(c.x - self.goal.x) + abs(c.y - self.goal.y)

        self.goal.g = float("inf")

        state = self.start

        while(state.x != self.goal.x or state.y != self.goal.y):
            print(self.count)
            self.count += 1
            state.g = 0
            state.search = self.count
            self.goal.search = self.count

            openlist = []
            closelist = []
            heap = MinHeap_Small_g(openlist)
            heap.insert(state)

            self.visual_frame("path_plan_list", state)

            print("debug1")
            while self.goal.g > heap.min().f():
                potential_state = heap.extract_min()
                self.visual_frame("path_plan_center", potential_state)
                closelist.append(potential_state)
                print("debug2")
                print(potential_state)
                for n in potential_state.neighbor:
                    if potential_state.neighbor[n] != None and not potential_state.neighbor[n] in closelist:
                        if potential_state.neighbor[n].search < self.count:
                            potential_state.neighbor[n].g = float("inf")
                            potential_state.neighbor[n].search = self.count
                        if (not potential_state.neighbor[n].blocked):
                            if potential_state.neighbor[n].g > potential_state.g + 1:
                                potential_state.neighbor[n].g = potential_state.g + 1
                                potential_state.neighbor[n].treeptr = potential_state
                                print("--------")
                                print(potential_state.neighbor[n].treeptr)

                                if potential_state.neighbor[n] in heap.list:
                                    heap.decrease_key(heap.list.index(potential_state.neighbor[n]), potential_state.neighbor[n].g)
                                else:
                                    heap.insert(potential_state.neighbor[n])
                            
                                self.visual_frame("path_plan_list", potential_state.neighbor[n])

            if len(heap.list) == 0:
                println("Cannot reach the target")
                return 1

            print(self.goal.treeptr)

            back = self.goal
            print("goal")
            print(self.goal.x,self.goal.y)
            trace_list = []
            print(back)
            print(self.goal)
            while back.x != state.x or back.y != state.y:
                trace_list.append(back)
                back = back.treeptr
            print(len(trace_list))

            print("back pointer")
            print(back.x, back.y)
            print(back)

            print("state")
            print(state.x, state.y)
            print(state)
            print("start")
            print(self.start.x, self.start.y)
            print(self.start)

            trace_list.reverse()
            print(trace_list[len(trace_list)-1]==self.goal)
            print(trace_list[0]==state)
            print(len(trace_list))

            i = 1
            while i<len(trace_list) and not trace_list[i].blocked:
                state = trace_list[i-1]
                self.visual_frame("move_list", state)
                print(i)
                i += 1
            if i == len(trace_list):
                state = self.goal
                print("final state")
                print(state.x, state.y)

        self.end_time = time.time()
        self.calc_small_g_time = self.end_time- self.start_time
        return 0

    def repeated_backward_astar(self):
        self.start_time = time.time()
        self.count = 0
        print("set h")
        for vector in self.cells:
            for c in vector:
                c.h = abs(c.x - self.start.x) + abs(c.y - self.start.y)

        self.start.g = float("inf")

        state = self.goal

        while(state.x != self.start.x or state.y != self.start.y):
            self.count += 1
            state.g = 0
            state.search = self.count
            self.start.search = self.count

            openlist = []
            closelist = []
            heap = MinHeap(openlist)
            heap.insert(state)

            self.visual_frame("path_plan_list", state)

            while self.start.g > heap.min().f():
                potential_state = heap.extract_min()
                self.visual_frame("path_plan_center", potential_state)
                closelist.append(potential_state)
                for n in potential_state.neighbor:
                    if potential_state.neighbor[n] != None and not potential_state.neighbor[n] in closelist:
                        if potential_state.neighbor[n].search < self.count:
                            potential_state.neighbor[n].g = float("inf")
                            potential_state.neighbor[n].search = self.count
                        if not potential_state.neighbor[n].blocked:
                            if potential_state.neighbor[n].g > potential_state.g +1:
                                potential_state.neighbor[n].g = potential_state.g +1
                                potential_state.neighbor[n].treeptr = potential_state

                                if potential_state.neighbor[n] in heap.list:
                                    heap.decrease_key(heap.list.index(potential_state.neighbor[n]), potential_state.neighbor[n].g)
                                else:
                                    heap.insert(potential_state.neighbor[n])

                                self.visual_frame("path_plan_list", potential_state.neighbor[n])

            if len(heap.list) == 0:
                print("Cannot reach the target")
                return 1

            back = self.start
            trace_list = []

            while back.x != state.x or back.y != state.y:
                trace_list.append(back)
                back = back.treeptr

            trace_list.reverse()

            i = 1
            while i<len(trace_list) and not trace_list[i].blocked:
                state = trace_list[i-1]
                self.visual_frame("move_list", state)
                i += 1
            if i == len(trace_list):
                state = self.start

        self.end_time = time.time()
        self.calc_time = self.end_time - self.start_time
        return 0

    def repeated_backward_astar_large_g(self):
        self.start_time = time.time()
        self.count = 0
        print("set h")
        for vector in self.cells:
            for c in vector:
                c.h = abs(c.x - self.start.x) + abs(c.y - self.start.y)

        self.start.g = float("inf")

        state = self.goal

        while(state.x != self.start.x or state.y != self.start.y):
            self.count += 1
            state.g = 0
            state.search = self.count
            self.start.search = self.count

            openlist = []
            closelist = []
            heap = MinHeap_Large_g(openlist)
            heap.insert(state)

            self.visual_frame("path_plan_list", state)

            while self.start.g > heap.min().f():
                potential_state = heap.extract_min()
                self.visual_frame("path_plan_center", potential_state)
                closelist.append(potential_state)
                for n in potential_state.neighbor:
                    if potential_state.neighbor[n] != None and not potential_state.neighbor[n] in closelist:
                        if potential_state.neighbor[n].search < self.count:
                            potential_state.neighbor[n].g = float("inf")
                            potential_state.neighbor[n].search = self.count
                        if not potential_state.neighbor[n].blocked:
                            if potential_state.neighbor[n].g > potential_state.g +1:
                                potential_state.neighbor[n].g = potential_state.g +1
                                potential_state.neighbor[n].treeptr = potential_state

                                if potential_state.neighbor[n] in heap.list:
                                    heap.decrease_key(heap.list.index(potential_state.neighbor[n]), potential_state.neighbor[n].g)
                                else:
                                    heap.insert(potential_state.neighbor[n])

                                self.visual_frame("path_plan_list", potential_state.neighbor[n])

            if len(heap.list) == 0:
                print("Cannot reach the target")
                return 1

            back = self.start
            trace_list = []

            while back.x != state.x or back.y != state.y:
                trace_list.append(back)
                back = back.treeptr

            trace_list.reverse()

            i = 1
            while i<len(trace_list) and not trace_list[i].blocked:
                state = trace_list[i-1]
                self.visual_frame("move_list", state)
                i += 1
            if i == len(trace_list):
                state = self.start

        self.end_time = time.time()
        self.calc_large_g_time = self.end_time - self.start_time
        return 0

#g = Grid(101, 101)
#g.repeated_forward_astar()


        