from src.mdp.action import a_int, a_str

NMAC_R = 500
GAMMA = .99

rw_vals = {
    'nmac': -10,
    'alert': -.1,
    'reversal': -.3,
    'distance': 0
}


def reward(obs, obs_new, a):
    r = 0

    # Penalize NMAC
    if is_nmac(obs_new):
        r += rw_vals['nmac']

    # Penalize alerts
    if is_alert(a):
        r += rw_vals['alert']

    # Penalize reversal
    if is_reversal(obs.prev_a, a):
        r += rw_vals['reversal']

    # Shaping reward
    r += rw_vals['distance'] * shaping_rw(obs, obs_new)

    return r


def is_nmac(obs_new):
    return obs_new.r <= NMAC_R


def is_alert(a):
    return a != a_int('NOOP')


def is_reversal(a_prev, a):
    a_prev, a = a_str(a_prev), a_str(a)

    return ((a_prev == 'RIGHT' and a == 'LEFT') 
        or (a_prev == 'LEFT' and a == 'RIGHT'))


def is_alert_start(a_prev, a):
    return (not is_alert(a_prev)) and is_alert(a)


def shaping_rw(obs, obs_new):
    return GAMMA * obs_new.r - obs.r
