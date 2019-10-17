from random import randrange

import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

import action
from state import initial_state, State, NUM_STATES


class GridworldEnv(gym.Env):

    def __init__(self, n, m, seed=0):
        super(GridworldEnv, self).__init__()

        self.dims = (n, m)

        # Define observation and action spaces
        self.observation_space = spaces.Discrete(NUM_STATES)
        self.action_space = spaces.Discrete(action.NUM_ACTIONS)

        # Seed environment
        np.random.seed(seed)

        # Set up the the initial state and time 
        self.reset()

    def step(self, a):
        """
        Advance one timestep, taking an action.

        Return the new state, the reward, and whether 
        the episode is over.
        """
        new_agent_pos = action.act(self.state.agent, 
            a, *self.dims)
        new_intruder_pos = action.act(self.state.intruder, 
            randrange(action.NUM_ACTIONS), *self.dims)
        new_state = State(new_agent_pos, new_intruder_pos)

        r = self._r(new_state, a)
        done = self.state.agent == self.goal
        
        self.state = new_state

        return self.state, r, done, {}

    def reset(self):
        """
        Reset state of environment to initial state.

        Returns the initial state.
        """
        self.state, self.goal = initial_state(*self.dims)
        self.t = 0
        return self.state

    def render(self, mode='human'):
        """
        Render state of the environment to the screen.
        """
        n, m = self.dims
        render_str = ['']
        own, intr = self.state

        for row in range(n):
            for col in range(m):
                if (col, row) == own:
                    render_str.append('O')
                elif(col, row) == intr:
                    render_str.append('I')
                else:
                    render_str.append('*')
            render_str.append('\n')

        render_str = ' '.join(render_str)
        print(render_str)


    def _r(self, new_state, action):
        """
        Compute reward obtained by transitioning
        to the new state.
        """
        r = 0

        # add a negative reward for each timestep
        r += -1

        # add a negaive reward for collisions
        if new_state.agent == new_state.intruder:
            r += -10

        return r
