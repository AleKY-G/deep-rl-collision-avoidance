from math import pi, sin, cos
from itertools import product
from pathlib import Path

import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches


from src.agent.train import load
from src.mdp.action import a_int, a_str, NUM_A, is_left, is_right
from src.mdp.state import (AC, State, Observation, 
    state_to_obs, process_obs)


def policy_plot(phi, model_name):
    # Define interval we'd like to plot
    x_interval = (-5000, 15000)
    y_interval = (-10000, 10000)
    phi1 = pi

    # Number of samples per dimension
    x_num, y_num = 100, 100

    # Create array to store sample policy
    a = np.empty((y_num, x_num), dtype=np.uint8)

    # Make x and y edges
    xs = np.linspace(*x_interval, x_num)
    ys = np.linspace(*y_interval, y_num)

    # Load policy
    policy = load(model_name)

    for x_i, y_i in tqdm(product(range(x_num), range(y_num))):
        # Create dummy observations
        obs = dummy_obs(xs[x_i], ys[y_i], phi)
        a[y_i, x_i] = policy([obs], stochastic=False)[0]

    # Plot the sample policy
    acts = values = np.unique(a)
    act_strs = [a_str(i) for i in range(NUM_A)]

    fig, ax = plt.subplots()
    im = ax.imshow(a, origin='lower', 
        extent=[xs[0], xs[-1], ys[0], ys[-1]])
    ax.plot(0, 0, 'w>', markeredgecolor='k', ms=10)

    colors = [im.cmap(im.norm(act)) for act in acts]
    patches = [mpatches.Patch(color=colors[i], label=act_strs[acts[i]]) 
            for i in range(len(acts))]

    plt.legend(handles=patches)

    plt.xlabel('X (ft)')
    plt.ylabel('Y (ft)')
    plt.title('Policy Plot')
    plt.show()


def q_plot(phi, model_name):
    # Define interval we'd like to plot
    x_interval = (-5000, 15000)
    y_interval = (-10000, 10000)
    phi1 = pi

    # Number of samples per dimension
    x_num, y_num = 100, 100

    # Create array to store state values
    v = np.empty((x_num, y_num), dtype='float')

    # Make x and y edges
    xs = np.linspace(*x_interval, x_num)
    ys = np.linspace(*y_interval, y_num)

    # Load model
    model = load(model_name)
    policy = model.step_model

    for x_i, y_i in tqdm(product(range(x_num), range(y_num))):
        # Create dummy observations
        obs = dummy_obs(xs[x_i], ys[y_i], phi)
        _, q_vals, _ = policy.step([obs])
        v[x_i, y_i] = max(q_vals[0])

    fig, ax = plt.subplots()
    im = ax.imshow(v, origin='lower', 
        extent=[xs[0], xs[-1], ys[0], ys[-1]])
    fig.colorbar(im, ax=ax)
    ax.plot(0, 0, 'w>', markeredgecolor='k', ms=10)

    plt.xlabel('X (ft)')
    plt.ylabel('Y (ft)')
    plt.title('State Values')
    plt.show()


def encounter_plot(encounter):
    """
    Plot an encounter trajectory
    """
    ac0s, a0s, ac1s, a1s, _ = zip(*encounter)
    x0, y0, phi0 = [], [], []
    x1, y1, phi1 = [], [], []


    for i in range(len(ac0s)):
        x0.append(ac0s[i].x)
        y0.append(ac0s[i].y)
        phi0.append(ac0s[i].phi)

        x1.append(ac1s[i].x)
        y1.append(ac1s[i].y)
        phi1.append(ac1s[i].phi)

    
    # Build arrows based on actions
    u0, v0 = [], []
    u1, v1 = [], []


    # Draw arrows for each action
    for i in range(len(a0s)):
        a0, a1 = a0s[i], a1s[i]

        # Ownship action arrows
        if is_left(a0):
            u0.append(cos(phi0[i] + pi/2))
            v0.append(sin(phi0[i] + pi/2))
        elif is_right(a0):
            u0.append(cos(phi0[i] - pi/2))
            v0.append(sin(phi0[i] - pi/2))
        else:
            u0.append(0)
            v0.append(0)

        # Intruder action arrows
        if is_left(a1):
            u1.append(cos(phi1[i] + pi/2))
            v1.append(sin(phi1[i] + pi/2))
        elif is_right(a1):
            u1.append(cos(phi1[i] - pi/2))
            v1.append(sin(phi1[i] - pi/2))
        else:
            u1.append(0)
            v1.append(0)

    
    # Make encounter plot
    f, ax = plt.subplots()

    # Positions
    ax.plot(x0, y0, 'C0', marker='.', ms=3, label='ownship')
    ax.plot(x1, y1, 'C1', marker='.', ms=3, label='intruder')
    
    # Mark start
    ax.plot(x0[0], y0[0], 'C2o', ms=5)
    ax.plot(x1[0], y1[0], 'C2o', ms=5)

    # Mark end
    ax.plot(x0[-1], y0[-1], 'C3*', ms=7)
    ax.plot(x1[-1], y1[-1], 'C3*', ms=7)


    # Action arrrow
    ax.quiver(x0, y0, u0, v0, color='k', width=.003, scale=30)
    ax.quiver(x1, y1, u1, v1, color='k', width=.003, scale=30)

    # Launch plot
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Encounter')
    ax.legend()
    ax.set_aspect('equal')
    plt.plot()



def dummy_obs(x, y, phi):
    # Create dummy observation from x,y coords
    x0, y0, phi0, sp0, d_phi0 = 0, 0, 0, 210, 0
    x1, y1, phi1, sp1, d_phi1 = x, y, phi, 210, 0
    prev_a = a_int('NOOP')

    ac0 = AC(x0, y0, phi0, sp0, d_phi0)
    ac1 = AC(x1, y1, phi1, sp1, d_phi1)
    st = State(ac0, ac1, prev_a)
    obs = state_to_obs(st)

    return process_obs(obs)
