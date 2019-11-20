import gym
import tensorflow as tf
from baselines import deepq
from gym_ca.envs import GridworldEnv


def ep_metrics(ep_states):
    num_collisions = 0

    for s in ep_states:
        num_collisions += is_collision(s)

    ep_len = len(ep_states)

    return num_collisions > 0, ep_len


def metrics(all_eps_metrics):
    collision_eps, ep_lens = zip(all_eps_metrics)

    mac_rate = sum(collision_eps) / len(collision_eps)
    avg_len = sum(ep_lens) / len(ep_lens)

    return mac_rate, avg_len


def is_collision(s):
    return s[0] == s[1]


def collect_metrics():
    # Probability of ignoring action
    ignore_probs = [0, .01, .03, .05, .1, .2, .3]

    steps = int(3e4)
    for p in ignore_probs:
        # Create environment with this ignore prob
        env = GridworldEnv(prob_droput=p)

        # Train policy on this environment
        policy = deepq.learn(
            env,
            network='mlp',
            lr=1e-3,
            total_timesteps=int(steps),
            buffer_size=int(5e3),
            exploration_fraction=.1,
            exploration_final_eps=0,
            print_freq=100,
            num_layers=2,
            num_hidden=64,
            activation=tf.nn.relu
        )
        policy.save('policy_ignore_p_{}.pkl'.format(p))

        # Run trained policy on 
