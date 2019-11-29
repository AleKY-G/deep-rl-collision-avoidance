from random import uniform, randrange, choices
from math import pi, sin, cos

import numpy as np

from mdp.action import NUM_A, a_int
from mdp.state import get_var_interval, AC, State
from mdp.transition import advance_ac
from mdp.reward import NMAC_R


def mc_encounter(tca, avg_maneuver_len=15, p_nmac=.1):
    # Make state transition matrix
    p_self = (avg_maneuver_len - 1) / avg_maneuver_len
    p_trans = (1 - p_self) / (NUM_A - 1)

    p_t = ((p_self - p_trans) * np.identity(NUM_A)
        + p_trans * np.ones((NUM_A, NUM_A)))

    # Initialize ownship and intruder state
    x0, y0, phi0, sp0, d_phi0 = \
        0, 0, 0, uniform(*get_var_interval('sp0')), 0
    x1, y1, phi1, sp1, d_phi1 = \
        0, 0, uniform(-pi, pi), uniform(*get_var_interval('sp1')), 0

    # Advance position of both ownship and intruder until tca
    ac0 = AC(x0, y0, phi0, sp0, d_phi0)
    ac1 = AC(x1, y1, phi1, sp1, d_phi1)

    # Create intruder action generator
    int_act_gen = action_generator(p_t)
    int_acts = []

    for _ in range(tca):
        ac0 = advance_ac(ac0, a_int('NOOP'))
        int_acts.append(next(int_act_gen))
        ac1 = advance_ac(ac1, int_acts[-1])

    # Adjust intruder starting position to collide at tca
    x1, y1 = ac0.x - ac1.x, ac0.y - ac1.y

    # Add randomness to starting position to vary number 
    # of encounters with NMAC
    d_angle = uniform(-pi, pi)
    d_magnitude = uniform(0, NMAC_R / p_nmac)

    x1, y1 = (x1 + d_magnitude * cos(d_angle), 
        y1 + d_magnitude * sin(d_angle))

    # Return starting state with action generator
    ac0 = AC(x0, y0, phi0, sp0, d_phi0)
    ac1 = AC(x1, y1, phi1, sp1, d_phi1)
    prev_a = a_int('NOOP')
    st = State(ac0, ac1, prev_a)

    return st, action_generator(p_t, int_acts)


def action_generator(p_t, init_acts=[]):
    # Consume all actions from initial list
    for a_init in init_acts:
        yield a_init
    
    # Continue generating Markov chain actions
    a_list = range(NUM_A)
    a = randrange(NUM_A)
    
    while True:
        yield a
        a = choices(a_list, weights=p_t[a])[0]
