from collections import namedtuple
from .grid import create_grid


ac_states = ['x', 'y']
AC_State = namedtuple('AC_State', ac_states)
State = namedtuple('State', ['agent', 'intruder'])
Observation = namedtuple('Observation', ['x0', 'y0', 'x1', 'y1'])

NUM_STATES = 4


def initial_state(n, m):
    agent, intruder, goal = create_grid(n, m)
    return State(agent, intruder), goal


def state_to_obs(s):
    return Observation(*s[0], *s[1])
