# Aircraft Collision Avoidance Through Deep RL

<img align="right" width="500" height="400" src="encounter_path.png">

An environment for simulating encounters between aircraft for the purpose of creating collision avoidance systems. It is compatible with the collection of deep reinforcement learning models made available by OpenAI's `baselines` repo.

## Environment Setup Instructions

All of these packages are for Python, so make sure you have some version of Python 3 installed. I am running Python 3.7.4 for reference.

- __Install OpenAI Gym__: Follow installation instructions [here](https://github.com/openai/gym#installation). TL;DR run `pip install gym`.

- __Install OpenAI Baselines__: Instructions [here](https://github.com/openai/baselines#prerequisites). Requires that you have either Mac OS or Linux; you'll have to search around for instructions to run on Windows. Make sure you install TensorFlow with `pip install tensorflow` or `pip install tensorflow-gpu` if you have an NVidia GPU.

## Testing Installation

Run the commands below to check if installation worked.
```
# Train model and save the results to cartpole_model.pkl
python -m baselines.run --alg=deepq --env=CartPole-v0 --save_path=./cartpole_model.pkl --num_timesteps=1e5
# Load the model saved in cartpole_model.pkl and visualize the learned policy
python -m baselines.run --alg=deepq --env=CartPole-v0 --load_path=./cartpole_model.pkl --num_timesteps=0 --play
```

The first command trains a DQN model and the cartpole environment. This step might take ~20 minutes if you're running it on a CPU.

The the second uses the learned state value function to try to balance the pole on top of the cart. You should see a window pop up with a 2D rendering where the DQN model is trying to balance a pole on top of a cart in real time.

## Running GridWorld environment

After having installed `gym`, go to the repo directory and run `pip install -e gym-ca`. After this, you will be able to create the gridworld gym environment with `gym.make('gym_ca:ca-gridworld-v0')`.
