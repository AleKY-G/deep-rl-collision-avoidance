from collections import namedtuple
from itertools import count

ac_states = ['x', 'y']
AC_State = namedtuple('AC_State', ac_states)

acts_int = ['U', 'D', 'L', 'R']
a_str_to_int_intr = dict(zip(acts_int, count()))
a_int_to_str_intr = dict(zip(count(), acts_int))

def a_str_intr(a_int):
    return a_int_to_str_intr[a_int]

def a_int_intr(a_str_intr):
    return a_str_to_int_intr[a_str_intr]

def get_intruder_info(path=[]):

	# # Path to text file that defines intruder encounter behavior
 #    path = 'init-encounters/validation-encounters/left_right.txt'

	if path:

		# Load intruder behavior
		file = open(path, 'r')
		lines = file.readlines()
		file.close()

		# Set intruder starting location
		intruder_startingLocation = tuple(map(int,lines[0].split()))

		# intruder = (int(intruder_startingLocation[0]), int(intruder_startingLocation[1]))
		intruder = intruder_startingLocation

		intruder_motion_str = lines[1:]
		intruder_motion = []
		for item in intruder_motion_str:
			intruder_motion.append(a_int_intr(item.strip('\n')))

	else:

		intruder_startingLocation = []
		intruder_motion = []

	return intruder_startingLocation, intruder_motion



def act_intr_predefined(pos, a, n, m):

    a = a_str_intr(a)
    x, y = pos

    if a == 'NOOP':
        return AC_State(x,y)
    elif a == 'U':
        return AC_State(x, y-1) if 0 <= y-1 else pos
    elif a == 'D':
        return AC_State(x, y+1) if y+1 < n else pos
    elif a == 'L':
        return AC_State(x-1, y) if 0 <= x-1 else pos
    elif a == 'R':
        return AC_State(x+1, y) if x+1 < m else pos
    else:
        raise Exception('Invalid action.')