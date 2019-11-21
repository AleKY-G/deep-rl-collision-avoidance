import random
from random import randrange

import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

from .state import (NUM_STATES, State, initial_state, 
    state_to_obs, fixed_initial_state, decision_dropbout)
from .action import NUM_ACTIONS, NUM_ACTIONS_intr, act, act_intr
from .intruder_predefinedMotion import act_intr_predefined


class GridworldEnv(gym.Env):

    def __init__(self, n=10, m=10, p_ignore=0, 
        intruder_start=(5, 5), intruder_actions=None, seed=0):
        super(GridworldEnv, self).__init__()

        self.dims = (n, m)

        # Define observation and action spaces
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0]), 
            high=np.array([m, n, m, n]),
            dtype=np.float32
        )
        self.action_space = spaces.Discrete(NUM_ACTIONS)
        self.p_ignore = p_ignore

        # Seed environment
        np.random.seed(seed)
        random.seed(seed)

        # Intruder predifined actions
        self.intruder_actions = intruder_actions
        self.intruder_start = intruder_start

        # Set up the the initial state and time 
        self.reset()


    def step(self, a):
        """
        Advance one timestep, taking an action.

        Return the new state, the reward, and whether 
        the episode is over.
        """

        # With probability p_ignore take random action.
        if decision_dropbout(self.p_ignore):
            a = randrange(NUM_ACTIONS)

        # Advance ownship according to given action
        new_agent_pos = act(self.state.agent, 
            a, *self.dims)
        
        # Determine next intruder action according to 
        # given plan, or randomly
        if self.intruder_actions is None:
            next_a_int = randrange(NUM_ACTIONS_intr)
        else:
            n = len(self.intruder_actions)
            next_a_int = self.intruder_actions[self.t % n]
        
        # Advance intruder state with given action
        new_int_pos = act(self.state.intruder, 
            next_a_int, *self.dims)

        # Update environment values
        new_state = State(new_agent_pos, new_int_pos)

        r = self._r(new_state, a, self.obstacles)
        done = self._is_done()
        
        self.state = new_state
        obs = state_to_obs(self.state)

        return np.array(obs), r, done, {'state': self.state}


    def reset(self):
        """
        Reset state of environment to initial state.

        Returns the initial state.
        """
        # Initialize state, goal, and obstacle locations
        self.state, self.goal, self.obstacles = \
            fixed_initial_state(*self.dims, self.intruder_start)

        # Record number of collisions and episode timestep
        self.t = 0
        self.num_mac = 0

        return state_to_obs(self.state)


    def render(self, mode='human'):
        """
        Render state of the environment to the screen.
        """
        n, m = self.dims
        render_str = ['']
        own, intr = self.state

        for row in range(n-1, -1, -1):
            for col in range(m):
                if (col, row) == own:
                    render_str.append('O')
                elif (col, row) == intr:
                    render_str.append('I')
                elif (col, row) == self.goal:
                    render_str.append('G')
                elif (col, row) in self.obstacles:
                    render_str.append('X')
                else:
                    render_str.append('*')
            render_str.append('\n')

        render_str = ' '.join(render_str)
        print(render_str)


    def _r(self, new_state, action, obstacle):
        """
        Compute reward obtained by transitioning
        to the new state.
        """
        r = 0

        # add a negative reward for each timestep
        r += -1

        # add a negative reward for collisions with intruder
        if new_state.agent == new_state.intruder:
            r += -50

        # add a negative reward for collisions with obstacle
        if new_state.agent in obstacle:
            r += -50

        return r


    def _is_done(self):
        return self.state.agent == self.goal