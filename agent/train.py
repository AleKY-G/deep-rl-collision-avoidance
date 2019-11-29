from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import DQN

from gym_ca.envs import CAEnv

class CAPolicy(MlpPolicy):
    def __init__(self, *args, layers=3*[32], **kwargs):
        super(CAPolicy, self).__init__(*args, **kwargs,
                                       layers=layers)


if __name__ == '__main__':
    env = CAEnv()
    env = DummyVecEnv([lambda: env])

    hyperparams = {
        'prioritized_replay': True,
        'buffer_size': int(5e4),
        'verbose': 1,
        'learning_starts': 0
    }

    model = DQN(CAPolicy, env, **hyperparams)
    model.learn(total_timesteps=int(1e5))
