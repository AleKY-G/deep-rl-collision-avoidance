from random import randrange

def create_grid_predefined(n, m):
    """
    Creates a grid with n rows, m cols.

    The grid defines the set of states the agent 
    can occupy, a goal cell, and a starting cell 
    for the agent and intruder based on pre-defined
    positions.
    """
    agent = (0,0)
    goal = (n-1, m-1)
    intruder = (m-2, 2)

    return agent, intruder, goal



def create_obstacle_grid_predefined(n, m):
    """
    Create a grid with a block of obstacles set in the 
    middle.
    """
    assert n > 3 and m > 3

    mid = (n/2, m/2)
    x0, x1, y0, y1 = int(m/2), int(m/2) + 1, int(n/2), int(n/2) + 1
    # x0, y0 = int(m/2), int(m/2)

    obstacles = [(x0, y0), (x0, y1), (x1, y0), (x1, y1)]
    # obstacles = (x0, y0)

    agent, intruder, goal = create_grid_predefined(n, m)

    return agent, intruder, goal, obstacles


