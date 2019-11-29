from collections import namedtuple
from math import atan2

from gym import spaces
import numpy as np

from mdp.util import norm2, angle_parts
from mdp.action import TURN_LIM, NUM_A


ac_vars = ['x', 'y', 'phi', 'speed', 'd_phi']
obs_vars = ['r', 'theta_x', 'theta_y', 
            'psi_x', 'psi_y', 'sp0', 'sp1',
            'd_phi0', 'd_phi1', 'prev_a']
state_vars = ['own', 'int', 'prev_a']

AC = namedtuple('AC', ac_vars)
Observation = namedtuple('Observation', obs_vars)
State = namedtuple('State', state_vars)

# Observation variable value interval
obs_var_interval = {
    'r': (0, 25000),
    'theta_x': (-1, 1),
    'theta_y': (-1, 1),
    'psi_x': (-1, 1),
    'psi_y': (-1, 1),
    'sp0': (200, 225),
    'sp1': (200, 225),
    'd_phi0': (-TURN_LIM, TURN_LIM),
    'd_phi1': (-TURN_LIM, TURN_LIM),
    'prev_a': (0, NUM_A - 1)
}

# Observation variable range
obs_var_ran = {k: v[1] - v[0] 
               for k,v in obs_var_interval.items()}

# Gym observation space definition
low_vals, high_vals = zip(*[obs_var_interval[k] for k in obs_vars])

gym_obs_space = spaces.Box(
    low=np.array(low_vals),
    high=np.array(high_vals),
    dtype=np.float32
)


def get_var_interval(var):
    return obs_var_interval[var]


def get_obs_space():
    return gym_obs_space


def state_to_obs(st):
    # Extract state components
    ac0, ac1, prev_a = st

    # Calculate relative position
    x_rel, y_rel = ac1.x - ac0.x, ac1.y - ac0.y

    # Calculate relative position in polar coords
    r = norm2(x_rel, y_rel)

    theta = atan2(y_rel, x_rel)
    theta_x, theta_y = angle_parts(theta)

    psi = ac1.phi - ac0.phi
    psi_x, psi_y = angle_parts(psi)

    return Observation(r, theta_x, theta_y, psi_x, psi_y, 
        ac0.speed, ac1.speed, ac0.d_phi, ac1.d_phi, 
        prev_a)


def process_obs(obs):
    new_obs = {}

    for var_name, var_val in obs._asdict().items():
        val_min = obs_var_interval[var_name][0]
        val_ran = obs_var_ran[var_name]

        new_obs[var_name] = (var_val - val_min) / val_ran

    return Observation(**new_obs)
