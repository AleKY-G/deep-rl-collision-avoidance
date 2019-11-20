import gym
import tensorflow as tf
# from baselines import deepq
import deepq_mod


import time


def run(load_path, env_name='gym_ca:ca-gridworld-v0'):
    env = gym.make(env_name)
    policy = deepq_mod.learn(
        env, 
        network='mlp',
        num_layers=2,
        num_hidden=64,
        activation=tf.nn.relu,
        total_timesteps=0,
        load_path=load_path
    )


    while True:
        obs, done = env.reset(), False

        last_act_intr = 'NOOP'
        while not done:
            env.render()
            time.sleep(.2)
            obs, _, done, _ = env.step(policy([obs])[0])


if __name__ == '__main__':
    # run('gridworld_policy_1573098048.pkl')
    run('gridworld_policy.pkl')
