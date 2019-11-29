from mdp.action import a_int

NMAC_R = 500
rw_vals = {
    'nmac': -50,
    'alert': -.1,
    'distance': 1e-3
}


def reward(obs, obs_new, a):
    r = 0

    # Penalize NMAC
    if is_nmac(obs_new):
        r += rw_vals['nmac']

    # Penalize alerts
    if is_alert(a):
        r += rw_vals['alert']

    # Shaping reward
    r += rw_vals['distance'] * shaping_rw(obs, obs_new)

    return r


def is_nmac(obs_new):
    return obs_new.r <= NMAC_R


def is_alert(a):
    return a != a_int('NOOP')


def shaping_rw(obs, obs_new):
    return obs_new.r - obs.r
