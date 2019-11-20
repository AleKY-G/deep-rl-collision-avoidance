def ep_metrics(ep_states):
    num_collisions = 0

    for s in ep_states:
        num_collisions += is_collision(s)

    ep_len = len(ep_states)

    return num_collisions > 0, ep_len


def metrics(all_eps_metrics):
    collision_eps, ep_lens = zip(all_eps_metrics)

    mac_rate = sum(collision_eps) / len(collision_eps)
    avg_len = sum(ep_lens) / len(ep_lens)

    return mac_rate, avg_len


def is_collision(s):
    pass