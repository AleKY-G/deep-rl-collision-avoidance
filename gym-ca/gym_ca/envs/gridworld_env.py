from random import randrange

import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

from .state import NUM_STATES, State, initial_state, state_to_obs, fixed_initial_state
from .action import NUM_ACTIONS, NUM_ACTIONS_intr, act, act_intr


class GridworldEnv(gym.Env):

    def __init__(self, n=10, m=10, seed=0):
        super(GridworldEnv, self).__init__()

        self.dims = (n, m)

        # Define observation and action spaces
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0]), 
            high=np.array([m, n, m, n]),
            dtype=np.float32
        )
        self.action_space = spaces.Discrete(NUM_ACTIONS)

        # Seed environment
        np.random.seed(seed)

        # Set up the the initial state and time 
        self.reset()

    def step(self, a, last_act_intr):
        """
        Advance one timestep, taking an action.

        Return the new state, the reward, and whether 
        the episode is over.
        """
        new_agent_pos = act(self.state.agent, 
            a, *self.dims)
        # new_intruder_pos = act(self.state.intruder, 
        #     randrange(NUM_ACTIONS), *self.dims)
        new_intruder_pos, last_act_intr = act_intr(self.state.intruder, 
            randrange(NUM_ACTIONS_intr), *self.dims, last_act_intr)
        new_state = State(new_agent_pos, new_intruder_pos)

        # print("Here: "+last_act_intr)

        r = self._r(new_state, a, self.obstacle)
        done = self.state.agent == self.goal
        
        self.state = new_state
        obs = state_to_obs(self.state)

        return np.array(obs), r, done, {}, last_act_intr

    def reset(self):
        """
        Reset state of environment to initial state.

        Returns the initial state.
        """
        # self.state, self.goal = initial_state(*self.dims)
        self.state, self.goal, self.obstacle = fixed_initial_state(*self.dims)
        self.t = 0
        return state_to_obs(self.state)

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
                elif (col, row) == intr:
                    render_str.append('I')
                elif (col, row) == self.goal:
                    render_str.append('G')
                elif (col, row) in self.obstacle:
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

        # add a negaive reward for collisions with intruder
        if new_state.agent == new_state.intruder:
            # r += -10
            r += -50

        # add a negaive reward for collisions with obstacle
        if new_state.agent in obstacle:
            print(obstacle)
            print(new_state.agent)
            # r += -10
            r += -50

        return r
