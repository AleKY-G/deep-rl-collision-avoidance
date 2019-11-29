import random
from random import randrange

import numpy as np
from gym import Env

from mdp.state import (get_obs_space, State, state_to_obs,
                       get_var_interval, process_obs)
from mdp.action import get_act_space
from mdp.transition import advance_ac
from mdp.reward import reward
from mdp.encounter import mc_encounter


class CAEnv(Env):

    def __init__(self, seed=0):
        super(CAEnv, self).__init__()

        # Define observation and action spaces
        self.observation_space = get_obs_space()
        self.action_space = get_act_space()

        # Seed environment
        np.random.seed(seed)
        random.seed(seed)
        
        # Declare environment variables
        self.state = None
        self.obs = None
        self.t = None
        
        # Intruder action generator
        self.int_acts = None
        
        # Time of closest approach interval
        self.tca = (35, 50)
        
        # Define encounter limits
        self.max_r = get_var_interval('r')[1]


    def step(self, a):
        """
        Advance one timestep, taking an action.

        Return the new state, the reward, and whether 
        the episode is over.
        """
        # Advance ownship
        own_st_new = advance_ac(self.state.ac0, a)
        
        # Advance intruder
        a_int = next(self.int_acts)
        int_st_new = advance_ac(self.state.ac1, a_int)
        
        # Make new state and observation
        st_new = State(own_st_new, int_st_new, a)
        obs_new = state_to_obs(st_new)
        
        # Calculate reward
        rw = reward(self.obs, obs_new, a)
        
        # Update variables and return
        self.state = st_new
        self.obs = obs_new
        self.t += 1
        
        done = self._is_done()
        
        return process_obs(self.obs), rw, done, {}


    def reset(self):
        """
        Reset state of environment to initial state.

        Returns the initial state.
        """
        # Reset timestep counter
        self.t = 0
        
        # Reset state and observation
        tca = randrange(*self.tca)
        self.state, self.int_acts = \
            mc_encounter(tca)
        self.obs = state_to_obs(self.state)
        
        # Return initial observation
        return process_obs(self.obs)


    def render(self, mode='human'):
        """
        Render state of the environment to the screen.
        """
        pass


    def _is_done(self):
        return self.obs.r > self.max_r
