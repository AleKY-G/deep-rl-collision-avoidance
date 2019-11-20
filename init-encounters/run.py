import gym
import tensorflow as tf
from baselines import deepq


import time


def run(load_path, env_name='gym_ca:ca-gridworld-v0'):
    env = gym.make(env_name)
    policy = deepq.learn(
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
        position_file = open("../visualization/position.txt","a") 
        while not done:
            env.render()
            time.sleep(.2)
            obs, _, done, pos, last_act_intr = env.step(policy([obs])[0],last_act_intr)
            print(str(obs))
            position_file.write(str(obs[0]) + " " + str(obs[1]) + " " + str(obs[2]) + " " + str(obs[3]) + "\n")
           
        position_file.close() 


if __name__ == '__main__':
    run('gridworld_policy_1574112290.pkl')
