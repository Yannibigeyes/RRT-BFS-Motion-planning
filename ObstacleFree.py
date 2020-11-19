'''
Authors:    Yongyang Liu <liuyongyang@gatech.edu>
            
Date:       3 Oct 2020
'''
import math
class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def distance(self, new):
        return math.sqrt((self.x - new.x) * (self.x - new.x) + (self.y - new.y) * (self.y - new.y))

def Obstaclfree(x_point, Obst):
	# input all points along a path and check the obstacle free

    for i in range(5):
        obs_temp = Vec2d(Obst[i,0]*10,Obst[i,1]*10)
        
        # check the distance to the center whether smaller than radius
        if obs_temp.distance(x_point)<= (Obst[i,2]*10 + 1*10):   #obstacle radius + robot radius
            return False
    return True
