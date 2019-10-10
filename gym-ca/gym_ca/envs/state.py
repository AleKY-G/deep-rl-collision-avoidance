from collections import namedtuple
import grid

ac_states = ['x', 'y']
AC_State = namedtuple('AC_State', ac_states)
State = namedtuple('State', ['agent', 'intruder'])


def initial_state():
    agent, intruder, goal = grid.create_grid()
    return State(agent, intruder), goal

