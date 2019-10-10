from gym.envs.registration import register

register(
    id='ca-gridworld-v0',
    entry_point='gym_ca.envs:GridworldEnv'
)

