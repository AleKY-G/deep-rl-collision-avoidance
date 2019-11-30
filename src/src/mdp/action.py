from math import pi
from itertools import count

from gym import spaces


a_names = ['NOOP', 'LEFT', 'RIGHT']
NUM_A = len(a_names)

a_int_to_str = dict(zip(count(), a_names))
a_str_to_int = dict(zip(a_names, count()))

# Maneuver strength limits
TURN_LIM = 3 * (pi/180)    # 3 deg/s in rad/s
VERTICAL_LIM = 1000 / 60   # 1000 ft/min in ft/s

# Mapping from action to rate
a_to_rate = {
    'NOOP': 0,
    'LEFT': TURN_LIM,
    'RIGHT': -TURN_LIM
}

# Define action space
gym_act_space = spaces.Discrete(NUM_A)


def get_act_space():
    return gym_act_space

def a_int(a_str):
    return a_str_to_int[a_str]

def a_str(a_int):
    return a_int_to_str[a_int]

def a_rate(a_int):
    return a_to_rate[a_str(a_int)]
