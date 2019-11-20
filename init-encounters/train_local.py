import gym
import tensorflow as tf
from baselines import deepq

from time import time
import numpy as np


def train(env_name='gym_ca:ca-gridworld-v0', steps=2e4):
    env = gym.make(env_name)
    policy = deepq.learn(
        env,
        network='mlp',
        lr=1e-3,
        total_timesteps=int(steps),
        buffer_size=int(5e3),
        exploration_fraction=.1,
        exploration_final_eps=.01,
        print_freq=10,
        num_layers=2,
        num_hidden=64,
        activation=tf.nn.relu
    )

    # policy.save('gridworld_policy_'+str(int(time()))+'.pkl')
    policy.save('gridworld_policy.pkl')
    return policy


if __name__ == '__main__':
    train()
