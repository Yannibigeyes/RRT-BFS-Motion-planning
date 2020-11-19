'''
Authors:    Yongyang Liu <liuyongyang@gatech.edu>
            
Date:       3 Oct 2020
'''

import math
import numpy as np
from scipy.optimize import minimize_scalar

def Steering(x_rand, x_nearest_pos, x_nearest_orient):
    # generate randome point with no less than 2 meters, so t = 2s
    
    # f is the function of distance from x_new to x_rand over variable x, i.e. u
    f = lambda x: ((x_rand.x-x_nearest_pos.x-sum([0.02*math.cos(x_nearest_orient + 0.02*x*i) for i in range(1,101)])*10)**2 + (x_rand.y-x_nearest_pos.y-sum([0.02*math.sin(x_nearest_orient + 0.02*x*i) for i in range(1,101)])*10)**2)
    # scicy.optimize package
    res = minimize_scalar(f, bounds=(-np.pi/4, np.pi/4), method='bounded')
    return res.x

