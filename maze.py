from grid import *
from visualizer import *
import sys
import copy
import time


maze = Grid(20, 20)
'''
maze1 = copy.deepcopy(maze)
maze2 = copy.deepcopy(maze)
'''
#maze.repeated_backward_astar()
'''
large_g_start = time.time()
maze1.repeated_forward_astar_large_g()
large_g_end = time.time()
small_g_start = time.time()
maze2.repeated_forward_astar_small_g()
small_g_end = time.time()

print("******************")
print("large_g_time:{} small_g_time:{}".format(large_g_end-large_g_start, small_g_end-small_g_start))
'''

maze3 = copy.deepcopy(maze)
maze4 = copy.deepcopy(maze)

forward_start = time.time()
maze3.repeated_forward_astar_large_g()
forward_end = time.time()

backward_start = time.time()
maze4.repeated_backward_astar_large_g()
backward_end = time.time()

print("******************")
print("Forward_time:{} Backward_time:{}".format(forward_end-forward_start, backward_end-backward_start))


visual = Visualizer(maze3, 1, "myFileName")
print("show start")
visual.show_maze()
visual.animate_maze_solution()
print("show ends")

