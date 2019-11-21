import gym
import sys
from tqdm import tqdm
import tensorflow as tf
from baselines import deepq
from gym_ca.envs import (GridworldEnv, 
    intruder_predefinedMotion as ipm)
from pathlib import Path
import pickle
from matplotlib import pyplot as plt


def ep_metrics(ep_states):
    num_collisions = 0

    for s in ep_states:
        num_collisions += is_collision(s)

    ep_len = len(ep_states)

    return num_collisions > 0, ep_len


def metrics(all_eps_metrics):
    collision_eps, ep_lens = zip(*all_eps_metrics)

    mac_rate = sum(collision_eps) / len(collision_eps)
    avg_len = sum(ep_lens) / len(ep_lens)

    return mac_rate, avg_len


def is_collision(s):
    return s[0] == s[1]


def compare_exploration_p():
    # Probability of ignoring action
    ignore_probs = [0, .01, .03, .05, .1, .2, .3]
    empirical_metrics = {}

    for p in ignore_probs:
        steps = int(3e4)
        # Create environment with this ignore prob
        env = GridworldEnv(p_ignore=p)

        # Train policy on this environment
        with tf.Graph().as_default():
            policy = deepq.learn(
                env,
                network='mlp',
                lr=1e-3,
                total_timesteps=int(steps),
                buffer_size=int(2e4),
                exploration_fraction=.1,
                exploration_final_eps=0,
                print_freq=100,
                num_layers=2,
                num_hidden=64,
                activation=tf.nn.relu
            )
            policy.save('policy_ignore_p_{}.pkl'.format(p))

            # Run trained policy on validation set and 
            # collect metrics
            episodes = collect_metrics(policy)
            all_eps_metrics = [ep_metrics(ep_states) for ep_states in episodes]
            mac_rate, avg_ep_len = metrics(all_eps_metrics)

            empirical_metrics[p] = {'mac_rate': mac_rate, 
                'avg_ep_len': avg_ep_len}

        tf.reset_default_graph()
    
    with open('metrics.pkl', 'wb') as f:
        pickle.dump(empirical_metrics, f)

    return empirical_metrics


def collect_metrics_p(p):
    steps = int(3e4)
    # Create environment with this ignore prob
    env = GridworldEnv(p_ignore=p)

    # Train policy on this environment
    policy = deepq.learn(
        env,
        network='mlp',
        lr=1e-3,
        total_timesteps=int(steps),
        buffer_size=int(2e4),
        exploration_fraction=.1,
        exploration_final_eps=0,
        print_freq=100,
        num_layers=2,
        num_hidden=64,
        activation=tf.nn.relu
    )
    policy.save('policy_ignore_p_{}.pkl'.format(p))

    # Run trained policy on validation set and 
    # collect metrics
    episodes = collect_metrics(policy)
    all_eps_metrics = [ep_metrics(ep_states) for ep_states in episodes]
    mac_rate, avg_ep_len = metrics(all_eps_metrics)

    empirical_metrics = {'mac_rate': mac_rate, 
        'avg_ep_len': avg_ep_len}

    with open('metrics_{}.pkl'.format(p), 'wb') as f:
        pickle.dump(empirical_metrics, f)


def collect_metrics(policy):
    num_val_encs = 1000
    episodes = []

    for i in tqdm(range(num_val_encs)):
        # Create environment
        env = GridworldEnv(p_ignore=0.01)

        # Run policy on environment and collect metrics
        obs, done = env.reset(), False
        ep_states = []

        while not done:
            obs, _, done, info = env.step(policy([obs])[0])
            ep_states.append(info['state'])
        
        episodes.append(ep_states)
    
    return episodes


def unpack_metrics():
    ignore_probs = [0, .01, .03, .05, .1, .2, .3]
    name_temp = 'metrics_{}.pkl'
    mac_rate = {}
    avg_ep_len = {}

    for p in ignore_probs:
        with open(name_temp.format(float(p)), 'rb') as f:
            metrics_p = pickle.load(f)
            mac_rate[p] = metrics_p['mac_rate']
            avg_ep_len[p] = metrics_p['avg_ep_len']

    return mac_rate, avg_ep_len


def visualize_metrics(mac_rate, avg_ep_len):
    fix, ax = plt.subplots()

    x, y = zip(*mac_rate.items())
    plt.plot(x, y, '.-')
    plt.xlabel('Exploration Probability')
    plt.ylabel('Collision Rate')
    plt.title('Collision Rate by Exploration Probability')
    plt.savefig('mac_rate.png')
    plt.show()

    x, y = zip(*avg_ep_len.items())
    plt.plot(x, y, '.-')
    plt.xlabel('Exploration Probability')
    plt.ylabel('Avg Encounter Length')
    plt.title('Encounter Length by Exploration Probability')
    plt.savefig('ep_len.png')
    plt.show()


if __name__ == '__main__':
    # p = float(sys.argv[1])
    # collect_metrics_p(p)
    mac_rate, avg_ep_len = unpack_metrics()
    print(mac_rate)
    print(avg_ep_len)
    visualize_metrics(mac_rate, avg_ep_len)
