from mdp.action import a_rate
from mdp.state import AC
from mdp.util import advance_pos, wrap_angle
from math import sin, cos

def advance_ac(ac, a):
    # Change angle due to action
    d_phi = a_rate(a)
    phi = wrap_angle(ac.phi + d_phi)
    
    # Advance position
    speed_x, speed_y = (ac.speed * cos(phi), 
                        ac.speed * sin(phi))
    x, y = ac.x + speed_x, ac.y + speed_y
    
    # Return new AC state
    return AC(x, y, phi, ac.speed, d_phi)
