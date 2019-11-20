import random
from collections import namedtuple
from .grid import create_grid
from .fixedgrid import create_grid_predefined, create_obstacle_grid_predefined
from .intruder_predefinedMotion import get_intruder_info


ac_states = ['x', 'y']
AC_State = namedtuple('AC_State', ac_states)
State = namedtuple('State', ['agent', 'intruder'])
Observation = namedtuple('Observation', ['x0', 'y0', 'x1', 'y1'])

NUM_STATES = 4


def initial_state(n, m):
    agent, intruder, goal = create_grid(n, m)
    return State(agent, intruder), goal

def fixed_initial_state(n, m, path=[]):
	obstacles = []
	intruder_motion = []
	# agent, intruder, goal = create_grid_predefined(n, m)
	agent, intruder, goal, obstacles = create_obstacle_grid_predefined(n, m)

	# Load predefined intruder motion if necessary
	intruder_predefined, intruder_motion = get_intruder_info(path)
	if intruder_predefined:
		intruder = intruder_predefined

	return State(agent, intruder), goal, obstacles, intruder_motion


def state_to_obs(s):
    return Observation(*s[0], *s[1])


def decision_dropbout(probability):
    return random.random() < probability
