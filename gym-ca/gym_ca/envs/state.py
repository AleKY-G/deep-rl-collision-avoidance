from collections import namedtuple
import grid

ac_states = ['x', 'y']
AC_State = namedtuple('AC_State', ac_states)
State = namedtuple('State', ['agent', 'intruder'])

NUM_STATES = 4


def initial_state(n, m):
    agent, intruder, goal = grid.create_grid(n, m)
    return State(agent, intruder), goal

