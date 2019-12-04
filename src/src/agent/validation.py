import random
from random import randrange

import pandas as pd

from src.encounter import validation_encounter
from src.agent.train import load
from src.reward import is_nmac, is_alert, is_reversal, is_alert_start
from gym_ca.envs import ValCAEnv


def create_encounter_set(n, seed=0):
    random.seed(seed)

    encounters = []

    for _ in range(n):
        tca = randrange(25, 40)
        encounters.append(validation_encounter(tca))

    return encounters


def collect_encounter_data(encounter_set, model_name):
    policy = load(model_name)
    env = ValCAEnv(encounter_set)
    all_encs = []

    for i in range(len(encounter_set)):
        done, obs = False, env.reset()
        enc_info = []

        while not done:
            obs, rw, done, info = env.step(policy([obs])[0])
            st, obs, a0, a1 = \
                info['state'], info['obs'], info['a0'], info['a1']
            enc_info.append((st.ac0, a0, st.ac1, a1, obs))


        all_encs.append(enc_info)

    return all_encs


def extract_encounter_metrics(encounter_data):
    """
    From this data we can determine all the metrics of interest. 
    The main ones we're concerned about are:
    - Proportion of episodes with NMAC.
    - Proportion of episodes with alerts.
    - Proportion of episodes with reversal.
    """
    for step_info in encounter_data:
        nmac = False
        alert = False
        reversal = False
        segments = 0

        ac0, a0, ac1, a1, obs = step_info

        # NMAC
        if is_nmac(obs):
            nmac = True

        # ALERT
        if is_alert(a0):
            alert = True

        # REVERSAL
        if is_reversal(obs.prev_a, a0):
            reversal = True

        # SEGMENTS
        if is_alert_start(obs.prev_a, a0):
            segments += 1

    return nmac, alert, reversal, segments


def extract_all_metrics(all_encounters_data):
    all_metrics = [extract_encounter_metrics(enc) 
        for enc in all_encounters_data]

    nmacs, alerts, reversals, segments = zip(*all_metrics)
    metrics_df = pd.DataFrame({
        'nmac': nmacs, 
        'alert': alerts,
        'reversal': reversals,
        'segments': segments
    })

    return metrics_df
