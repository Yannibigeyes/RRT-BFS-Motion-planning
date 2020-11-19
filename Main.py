'''
Authors:    Yongyang Liu <liuyongyang@gatech.edu>
            
Date:       3 Oct 2020
'''

import math
import random
import pygame
import time
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

from ObstacleFree import Obstaclfree
from Steer import Steering
from Path import BFS_Yes_paths
from Display import Display

class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def distance(self, new):
        return math.sqrt((self.x - new.x) * (self.x - new.x) + (self.y - new.y) * (self.y - new.y))

class Node:
    def __init__(self, point, orient, index):
        self.pos = point
        self.neighbours = []
        self.orient = orient
        self.index = index
        
class Tree:
    def __init__(self, point, orient):
        self.nodes = [Node(point, orient, 0)]

    def create_new_node(self):
        
        # generate a random sample with no less than 2 meters to current nodes, and with collision_free
        while True:
            x_rand = Vec2d(random.uniform(1, size - 1)*10, random.uniform(1, size - 1)*10)
            got_new = True
            if Obstaclfree(x_rand, Obst) == False:
                got_new = False
            
            if got_new:    
                for node in self.nodes:
                    if node.pos.distance(x_rand) < 2*10:  # smaller than 2 meters 
                        #print('too close')
                        got_new = False
                        break
            if got_new:
                break
                
        # get the neareat node
        nearest = self.nodes[0].pos.distance(x_rand)
        x_nearest = self.nodes[0]
        for node in self.nodes[1:]:
            if node.pos.distance(x_rand) < nearest:
                nearest = node.pos.distance(x_rand)
                x_nearest = node
        
        # Steering control 
        orient_new = Steering(x_rand, x_nearest.pos, x_nearest.orient)
    
        path_temp = []
        get_path = True
        for j in range(1,101):
            x_tmp = x_nearest.pos.x+sum([0.02*math.cos(x_nearest.orient + 0.02*orient_new*i) for i in range(1,j+1)])*10
            y_tmp = x_nearest.pos.y+sum([0.02*math.sin(x_nearest.orient + 0.02*orient_new*i) for i in range(1,j+1)])*10
            orient_tmp  = x_nearest.orient + 0.02*orient_new*j
            x_temp = Vec2d(x_tmp, y_tmp)
            if Obstaclfree(x_temp, Obst) == False:
                get_path = False
                break     
            x_temp = Node(x_temp, orient_tmp, self.nodes[-1].index + j)
            path_temp.append(x_temp)
    
        # add new paths
        if get_path == True:
            self.nodes.append(path_temp[0])
            x_nearest.neighbours.append(self.nodes[-1])
            self.nodes[-1].neighbours.append(x_nearest)
            #self.show_tree()
            x_new = self.nodes[-1]
            for i in range(1, 100):
                self.nodes.append(path_temp[i])
                x_new.neighbours.append(self.nodes[-1])
                self.nodes[-1].neighbours.append(x_new)
                x_new = self.nodes[-1]  
    
    def goal(self, goal):
        # distane from the last new point to goal
        output = self.nodes[-1].pos.distance(goal)
        return output
        
# read map
obst = pd.read_csv('env/obstacles.txt', sep='\t', header = None)
N, _ = obst.shape
Obst = np.zeros([N,3],dtype = np.int)
for i in range(N):
    temp = obst[0][i].split(',')
    Obst[i,:] = temp[:]

start = pd.read_csv('env/start.txt', sep='\t', header = None)
N, _ = start.shape
Start = np.zeros([N,3],dtype = np.int)
for i in range(N):
    temp = start[0][i].split(',')
    Start[i,:] = temp[:]

goal = pd.read_csv('env/goal.txt', sep='\t', header = None)
N, _ = goal.shape
Goal = np.zeros([N,2],dtype = np.int)
for i in range(N):
    temp = goal[0][i].split(',')
    Goal[i,:] = temp[:]

goal = Vec2d(Goal[0,0]*10, Goal[0,1]*10)
start = Vec2d(Start[0,0]*10, Start[0,1]*10)

# define tree
size = 101
tree = Tree(start, Start[0,2])


start_time = time.time()
done = False
N = 1
while not done:
    # call RRT
    tree.create_new_node()
    
    # distance from new point to goal
    res = tree.goal(goal)
    if res <= 5*10:
        done = True
    
    if N >1000:
        done = True 
        print('need more iterations')
    N+=1

time_point1 = time.time()
elapsed_time1 = time_point1-start_time              # time for rrt running

# optimal path - BFS
path_idx = BFS_Yes_paths(tree.nodes, tree.nodes[0].index, tree.nodes[-1].index)
elapsed_time2 = time.time()-time_point1             # time for optimal path - BFS

if path_idx == None:
    print('Returned Path: Infeasible')
else:
    path = []
    for item in path_idx:
        path.append([tree.nodes[item].pos.x, tree.nodes[item].pos.y])
    
    # display
    Display(Obst, Start, Goal, tree, path, size)

print('RRT Time (s): %1.12f' % (elapsed_time1))
print('BFS Time (s): %1.12f' % (elapsed_time2))
