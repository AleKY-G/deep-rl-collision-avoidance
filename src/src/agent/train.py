from pathlib import Path

from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import DQN

from gym_ca.envs import CAEnv


save_dir = Path('../models')


class CAPolicy(MlpPolicy):
    def __init__(self, *args, layers=2*[32], **kwargs):
        super(CAPolicy, self).__init__(*args, **kwargs,
                                       layers=layers)


def train(model_name='model'):
    env = CAEnv()
    env = DummyVecEnv([lambda: env])

    hyperparams = {
        'prioritized_replay': True,
        'buffer_size': int(5e4),
        'verbose': 1,
        'learning_starts': 0
    }

    learn_hyperparams = {
        'log_interval': 50,
        'total_timesteps': int(1e5)
    }

    model = DQN(CAPolicy, env, **hyperparams)
    model.learn(**learn_hyperparams)
    model.save(save_dir / model_name)

    return model


def load(model_name):
    model = DQN.load(save_dir / model_name)

    return model


if __name__ == '__main__':
    train()
