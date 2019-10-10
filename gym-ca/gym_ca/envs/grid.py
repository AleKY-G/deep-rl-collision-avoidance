from random import randrange

def create_grid(n, m):
    """
    Creates a grid with n rows, m cols.

    The grid defines the set of states the agent 
    can occupy, a goal cell, and a starting cell 
    for the agent and intruder.
    """
    agent = (0,0)
    goal = (n-1, m-1)
    intruder = (randrange(n), randrange(m))

    return agent, intruder, goal
