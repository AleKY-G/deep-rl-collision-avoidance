from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import DQN

from gym_ca.envs import CAEnv

class CAPolicy(MlpPolicy):
    def __init__(self, layers=3*[32], *args, **kwargs):
        super(CAPolicy, self).__init__(*args, **kwargs,
                                       layers=layers)


if __name__ == '__main__':
    env = CAEnv()
    env = DummyVecEnv([lambda: env])

    model = DQN(CAPolicy, env)
    model.learn(total_timesteps=1000)
