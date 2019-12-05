from random import sample
from math import pi
import sys

from src.agent.train import train, load
from src.agent.validation import validation
from src.encounter import (random_act_encounter, no_act_encounter, 
    sticky_act_encounter, single_act_encounter)

"""
What do we want to run in the experiments?

1. We want to have a function with only one parameter
that needs to be modified.

2. We want the result to contain: 
    - The policy file that will be run in the validation 
    encounters.
    - The training metrics with: avg. rewards, loss.
    - Hyperparameters and reward structure for report.
"""

VAL_ENCS_SEED = 44
NUM_ENCS = 5
PNMAC = .15

pnmacs = [.05, .1, .15, .25, .5, .75]
rw_shaping_coeffs = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2]
int_behaviors = [random_act_encounter, no_act_encounter, 
    sticky_act_encounter, single_act_encounter]


# # >>>>>> PNMAC EXPERIMENT <<<<<<<<<<<<<<<
# def pnmac_experiment():
#     pnmacs = [.05, .1, .15, .25, .5, .75]

#     for pnmac in pnmacs:
#         seeds = sample(range(10000), 3)
#         for seed in seeds:
#             # Train model
#             model_name = f'pnmac_exp_{pnmac}_s{seed}'
#             model_dir = train(model_name, p_nmac=pnmac)

#             # Run validation encounters on model and collect metrics
#             validation(model_name, NUM_ENCS, VAL_ENCS_SEED, PNMAC)

#             # Make policy plots
#             fig_dir = model_dir / 'plots'
#             fig_dir.mkdir(parents=True, exist_ok=True)

#             for phi in [-pi/2, 0, pi/2, pi]:
#                 policy_plot(phi, model_name, fig_dir)


# >>>>>> PNMAC EXPERIMENT <<<<<<<<<<<<<<<
def pnmac_train(pnmac, seed):
    model_name = f'pnmac_exp_{pnmac}_s{seed}'
    model_dir = train(model_name, p_nmac=pnmac)


def pnmac_validate(pnmac, seed):
    model_name = f'pnmac_exp_{pnmac}_s{seed}'
    validation(model_name, NUM_ENCS, VAL_ENCS_SEED, PNMAC)


# >>>>>> REWARD SHAPING EXPERIMENT <<<<<<<<<<
def rw_shaping_train(rw_shaping_coeff, seed):
    model_name = f'rw_shaping_exp{rw_shaping_coeff}_s{seed}'
    model_dir = train(model_name, 
        shaping_coeff=rw_shaping_coeff)

def rw_shaping_validate(rw_shaping_coeff, seed):
    model_name = f'rw_shaping_exp{rw_shaping_coeff}_s{seed}'
    validation(model_name, NUM_ENCS, VAL_ENCS_SEED, PNMAC)


# >>>>>> INTRUDER BEHAVIOR EXPERIMENT <<<<<<<<<<<<<<
def intruder_behavior_train(encounter_gen_fun, seed):
    model_name = f'int_behavior{encounter_gen_fun.__name__}_s{seed}'
    model_dir = train(model_name, 
        encounter_gen_fun=encounter_gen_fun)


def intruder_behavior_validate(encounter_gen_fun, seed):
    model_name = f'int_behavior{encounter_gen_fun.__name__}_s{seed}'
    validation(model_name, NUM_ENCS, VAL_ENCS_SEED, PNMAC)


if __name__ == '__main__':
    op_type = sys.argv[1]
    exp_type = sys.argv[2]
    seed = int(sys.argv[3])
    idx = int(sys.argv[4])


    if exp_type == 'pnmac':
        pnmac = pnmacs[idx]

        if op_type == 'train':
            pnmac_train(pnmac, seed)
        elif op_type == 'validate':
            pnmac_validate(pnmac, seed)

    elif exp_type == 'rw_shape':
        shaping_coeff = rw_shaping_coeffs[idx]

        if op_type == 'train':
            rw_shaping_train(shaping_coeff, seed)
        elif op_type == 'validate':
            rw_shaping_validate(shaping_coeff, seed)

    elif exp_type == 'int_behavior':
        enc_gen_fun = int_behaviors[idx]

        if op_type == 'train':
            intruder_behavior_train(enc_gen_fun, seed)
        elif op_type == 'validate':
            intruder_behavior_validate(enc_gen_fun, seed)
