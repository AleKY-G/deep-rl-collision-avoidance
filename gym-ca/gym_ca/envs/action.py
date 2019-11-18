from itertools import count
from .state import AC_State
from random import randrange


acts = ['NOOP', 'UP', 'DOWN', 'LEFT', 'RIGHT']
# acts = ['UP', 'DOWN', 'LEFT', 'RIGHT']
acts_int = ['DOWN', 'LEFT']
# acts_int = ['UP', 'DOWN', 'LEFT', 'RIGHT']
# acts_int = ['NOOP', 'UP', 'DOWN', 'LEFT', 'RIGHT']
NUM_ACTIONS = len(acts)
NUM_ACTIONS_intr = len(acts_int)

a_int_to_str = dict(zip(count(), acts))
a_int_to_str_intr = dict(zip(count(), acts_int))
a_str_to_int = dict(zip(acts, count()))
a_str_to_int_intr = dict(zip(acts_int, count()))

def a_int(a_str):
    return a_str_to_int[a_str]

def a_str(a_int):
    return a_int_to_str[a_int]

def a_int_intr(a_str_intr):
    return a_str_to_int_intr[a_str_intr]

def a_str_intr(a_int_intr):
    return a_int_to_str_intr[a_int_intr]


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

    # flag_backward = True
    # while flag_backward:
    #     if a == 'NOOP':
    #         new_state = AC_State(x,y)
    #         flag_backward = False
    #     elif a == 'UP':
    #         if y+1 < n:
    #             new_state = AC_State(x, y+1)
    #             flag_backward = False
    #         else:
    #             a = a_str(randrange(NUM_ACTIONS))
    #     elif a == 'DOWN':
    #         if 0 <= y-1:
    #             new_state = AC_State(x, y-1)
    #             flag_backward = False
    #         else:
    #             a = a_str(randrange(NUM_ACTIONS))
    #     elif a == 'LEFT':
    #         if 0 <= x-1:
    #             new_state = AC_State(x-1, y)
    #             flag_backward = False
    #         else:
    #             a = a_str(randrange(NUM_ACTIONS))
    #     elif a == 'RIGHT':
    #         if x+1 < m:
    #             new_state = AC_State(x+1, y)
    #             flag_backward = False
    #         else:
    #             a = a_str(randrange(NUM_ACTIONS))
    #     else:
    #         raise Exception('Invalid action.')

    # return new_state


def act_intr(pos, a, n, m, a_last):
    a = a_str_intr(a)
    x, y = pos

    # if a == 'NOOP':
    #     return AC_State(x,y), a
    # elif a == 'UP':
    #     return AC_State(x, y+1) if y+1 < n else pos, a
    # elif a == 'DOWN':
    #     return AC_State(x, y-1) if 0 <= y-1 else pos, a
    # elif a == 'LEFT':
    #     return AC_State(x-1, y) if 0 <= x-1 else pos, a
    # elif a == 'RIGHT':
    #     return AC_State(x+1, y) if x+1 < m else pos, a
    # else:
    #     raise Exception('Invalid action.')

    if a_last == 'UP':
        a_backwards = 'DOWN'
    elif a_last == 'DOWN':
        a_backwards = 'UP'
    elif a_last == 'RIGHT':
        a_backwards = 'LEFT'
    elif a_last == 'LEFT':
        a_backwards = 'RIGHT'
    elif a_last == 'NOOP':
        a_backwards = 'NOOP'


    # print('hello')
    # print(pos)
    # print('a_last: '+a_last)
    # print('a: '+a)
    # print(a == a_backwards)
    while True:
        # print(a)
        if y == n-1:
            new_state = AC_State(m-1, 0)
            a = 'NOOP'
            print('Reset intruder')
            break
        elif a == a_backwards:
            a = a_str_intr(randrange(NUM_ACTIONS_intr))
        else:
            if a == 'NOOP':
                new_state = AC_State(x,y)
                break
            elif a == 'DOWN':
                if y+1 < n:
                    new_state = AC_State(x, y+1)
                    break
                else:
                    a = a_str_intr(randrange(NUM_ACTIONS_intr))
            elif a == 'UP':
                if 0 <= y-1:
                    new_state = AC_State(x, y-1)
                    break
                else:
                    a = a_str_intr(randrange(NUM_ACTIONS_intr))
            elif a == 'LEFT':
                if 0 <= x-1:
                    new_state = AC_State(x-1, y)
                    break
                else:
                    a = a_str_intr(randrange(NUM_ACTIONS_intr))
            elif a == 'RIGHT':
                if x+1 < m:
                    new_state = AC_State(x+1, y)
                    break
                else:
                    a = a_str_intr(randrange(NUM_ACTIONS_intr))
            else:
                raise Exception('Invalid action.')
                break

    # print("new_state: "+str(new_state))
    # print("Now: "+a)
    # print('world')

    return new_state, a



def act_obstacles(pos, a, grid):
    n, m, obstacles = grid
    new_pos = act(pos, a, n, m)

    return new_pos if new_pos not in obstacles else pos
