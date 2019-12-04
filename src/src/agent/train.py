from pathlib import Path
from time import time

import tensorflow as tf
from baselines import deepq

from gym_ca.envs import CAEnv
from src.mdp.reward import GAMMA
from src.encounter import (random_act_encounter, no_act_encounter, 
    sticky_act_encounter, single_act_encounter)
import src


save_dir = Path(src.__file__).parent / 'models'


def train(model_name='model'):
    env = CAEnv(encounter_gen_fun=random_act_encounter, p_nmac=.1)
    model_dir = save_dir / model_name

    hyperparams = {
        'network': 'mlp',
        'total_timesteps': int(1e5),
        'lr': 5e-4,
        'prioritized_replay': True,
        'buffer_size': int(3e4),
        'learning_starts': 1000,
        'batch_size': 64,
        'exploration_fraction': .3,
        'exploration_final_eps': .01,
        'target_network_update_freq': 500,
        'checkpoint_freq': 5000,
        'checkpoint_path': model_dir
        'print_freq': 20,
        'gamma': GAMMA,
        'seed': 0,
        'num_layers': 3,
        'num_hidden': 64,
        'activation': tf.nn.relu
    }

    policy, q_vals = deepq.learn(env, **hyperparams)
    policy.save(model_dir / f'{model_name}.pkl')

    return policy


def load(model_name):
    env = CAEnv()

    policy, _ = deepq.learn(
        env,
        network='mlp',
        num_layers=3,
        num_hidden=64,
        activation=tf.nn.relu,
        total_timesteps=0,
        load_path=save_dir / model_name
    )

    return policy


if __name__ == '__main__':
    train()
