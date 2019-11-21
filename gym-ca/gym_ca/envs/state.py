import random
from collections import namedtuple
from .grid import create_grid
from .fixedgrid import create_grid_predefined, create_obstacle_grid_predefined


ac_states = ['x', 'y']
goal_vars = ['x', 'y']
AC_State = namedtuple('AC_State', ac_states)
Goal = namedtuple('Goal', goal_vars)
State = namedtuple('State', ['agent', 'intruder'])
Observation = namedtuple('Observation', ['x0', 'y0', 'x1', 'y1'])

NUM_STATES = 4


def initial_state(n, m):
    agent, intruder, goal = create_grid(n, m)
    return State(agent, intruder), goal

def fixed_initial_state(n, m, intruder):
	agent, _, goal, obstacles = create_obstacle_grid_predefined(n, m)

	return State(agent, intruder), goal, obstacles


def state_to_obs(s):
    return Observation(*s[0], *s[1])


def decision_dropbout(probability):
    return random.random() < probability
