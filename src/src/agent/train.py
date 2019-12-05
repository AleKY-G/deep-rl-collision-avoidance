from pathlib import Path
from time import time
import pickle
import os
from copy import copy

import tensorflow as tf
from baselines import deepq

from gym_ca.envs import CAEnv
from src.mdp.reward import GAMMA, rw_vals
from src.encounter import (random_act_encounter, no_act_encounter, 
    sticky_act_encounter, single_act_encounter)
import src


save_dir = Path(src.__file__).parent / 'models'


def train(model_name, 
          p_nmac=.1, 
          encounter_gen_fun=random_act_encounter, 
          shaping_coeff=0):
    env = CAEnv(encounter_gen_fun=encounter_gen_fun, 
                p_nmac=p_nmac, 
                shaping_coeff=shaping_coeff)
    model_dir = save_dir / model_name

    # Set logging formats and logs directory
    os.environ['OPENAI_LOG_FORMAT'] = 'stdout,csv,tensorboard'
    os.environ['OPENAI_LOGDIR'] = str(model_dir / 'logs')

    # Make model and logging directories
    model_dir.mkdir(parents=True, exist_ok=True)
    (model_dir / 'logs').mkdir(parents=True, exist_ok=True)

    hyperparams = {
        'network': 'mlp',
        'total_timesteps': int(5e3),
        'lr': 5e-4,
        'prioritized_replay': True,
        'buffer_size': int(3e4),
        'learning_starts': 1000,
        'batch_size': 64,
        'exploration_fraction': .3,
        'exploration_final_eps': .01,
        'target_network_update_freq': 500,
        'checkpoint_freq': 5000,
        'checkpoint_path': str(model_dir),
        'print_freq': 10,
        'gamma': GAMMA,
        'seed': 0,
        'num_layers': 3,
        'num_hidden': 64,
        'activation': tf.nn.relu
    }

    policy, q_vals = deepq.learn(env, **hyperparams)

    # Save policy
    policy.save(model_dir / f'{model_name}.pkl')

    # Save hyperparams
    save_obj(hyperparams, model_dir / f'{model_name}_hyperparams.pkl')

    # Save q vals
    # save_obj(q_vals, model_dir / f'{model_name}_qvals.pkl')

    # Save reward structure
    rws = copy(rw_vals)
    save_obj(rws, model_dir / f'{model_name}_rws.pkl')

    return model_dir


def load(model_name):
    env = CAEnv()
    model_dir = save_dir / model_name

    # Load hyperparams
    with open(model_dir / f'{model_name}_hyperparams.pkl', 'rb') as f:
        hyperparams = pickle.load(f)

    hyperparams['total_timesteps'] = 0

    policy, _ = deepq.learn(
        env,
        **hyperparams,
        load_path=model_dir / f'{model_name}.pkl'
    )

    return policy


def save_obj(obj, savepath):
    with open(savepath, 'wb') as f:
        pickle.dump(obj, f)


if __name__ == '__main__':
    train()
