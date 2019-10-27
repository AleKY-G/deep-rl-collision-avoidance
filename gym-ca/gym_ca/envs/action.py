from itertools import count
from .state import AC_State


acts = ['NOOP', 'UP', 'DOWN', 'LEFT', 'RIGHT']
NUM_ACTIONS = len(acts)

a_int_to_str = dict(zip(count(), acts))
a_str_to_int = dict(zip(acts, count()))

def a_int(a_str):
    return a_str_to_int[a_str]


def a_str(a_int):
    return a_int_to_str[a_int]


def act(pos, a, n, m):
    a = a_str(a)
    x, y = pos

    if a == 'NOOP':
        return AC_State(x,y)
    elif a == 'UP':
        return AC_State(x, y+1) if y+1 < n else pos
    elif a == 'DOWN':
        return AC_State(x, y-1) if 0 <= y-1 else pos
    elif a == 'LEFT':
        return AC_State(x-1, y) if 0 <= x-1 else pos
    elif a == 'RIGHT':
        return AC_State(x+1, y) if x+1 < m else pos
    else:
        raise Exception('Invalid action.')


def act_intr(pos, a, n, m, a_last):
    a = a_str(a)
    x, y = pos

    if a == 'NOOP':
        return AC_State(x,y), a_last
    elif a == 'UP':
        if a_last == 'DOWN':
            return AC_State(x,y), a_last
        else:
            return AC_State(x, y+1) if y+1 < n else pos, a
    elif a == 'DOWN':
        if a_last == 'UP':
            return AC_State(x,y), a_last
        else:
            return AC_State(x, y-1) if 0 <= y-1 else pos, a
    elif a == 'LEFT':
        if a_last == 'RIGHT':
            return AC_State(x,y), a_last
        else:
            return AC_State(x-1, y) if 0 <= x-1 else pos, a
    elif a == 'RIGHT':
        if a_last == 'LEFT':
            return AC_State(x,y), a_last
        else:
            return AC_State(x+1, y) if x+1 < m else pos, a
    else:
        raise Exception('Invalid action.')


def act_obstacles(pos, a, grid):
    n, m, obstacles = grid
    new_pos = act(pos, a, n, m)

    return new_pos if new_pos not in obstacles else pos
