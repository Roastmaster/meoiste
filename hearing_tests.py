import numpy as np
import random
import math

def random_z_test(one_shot=True):
    if one_shot:
        x = 2*(random.random()-0.5) # random panning along left and right axis
        y = 2*(random.random()-0.5) # random panning along north and south axis
        z = math.sqrt(x**2 + y**2)
        return [x,y,z]

def get_z_score(predicted=[0,0], actual=[0,0,0]):
    vec = np.array(predicted)
    dist = math.sqrt(vec[0]**2 + vec[1]**2)
    true_predictions = np.array([vec[0], vec[1], dist])
    return np.linalg.norm(actual - true_predictions)
