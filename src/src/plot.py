from math import pi
from itertools import product
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from src.agent.train import load
from src.mdp.action import a_int
from src.mdp.state import (AC, State, Observation, 
    state_to_obs, process_obs)


def policy_plot():
    # Define interval we'd like to plot
    x_interval = (-5000, 15000)
    y_interval = (-10000, 10000)
    phi1 = pi

    # Number of samples per dimension
    x_num, y_num = 100, 100

    # Create array to store sample policy
    a = np.empty((x_num, y_num), dtype=np.uint8)

    # Make x and y edges
    xs = np.linspace(*x_interval, x_num)
    ys = np.linspace(*y_interval, y_num)

    # Load policy
    policy = load('model')

    # Evaluate policy on each point
    phi = pi

    for x_i, y_i in product(range(x_num), range(y_num)):
        # Create dummy observations
        obs = dummy_obs(x_i, y_i, phi)

        a[x_i, y_i] = policy(obs)

    # Plot the sample policy
    fig, ax = plt.subplots()
    ax.imshow(a)
    plt.show()
    


def dummy_obs(x, y, phi):
    # Create dummy observation from x,y coords
    x0, y0, phi0, sp0, d_phi0 = 0, 0, 0, 200, 0
    x1, y1, phi1, sp1, d_phi1 = x, y, phi, 200, 0
    prev_a = a_int('NOOP')

    ac0 = AC()
    ac1 = AC()
    st = State(ac0, ac1, prev_a)
    obs = state_to_obs(st)

    return process_obs(obs)