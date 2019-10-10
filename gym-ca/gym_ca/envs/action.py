from itertools import count

acts = ['NOOP', 'UP', 'DOWN', 'LEFT', 'RIGHT']
NUM_ACTIONS = len(acts)

a_int_to_str = dict(zip(count(), acts))
a_str_to_int = dict(zip(acts, count()))

def a_int(a_str):
    return a_str_to_int[a_str]


def a_str(a_int):
    return a_int_to_str[a_int]


def act(pos, a, n, m):
    pass
