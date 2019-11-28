from math import sin, cos, sqrt, pi

angle_parts = lambda x: (cos(x), sin(x))
wrap_angle = lambda x: (x + pi) % (2*pi) - pi
normalize = lambda x, x_ran, x_min: (x - x_min) / x_ran
advance_pos = lambda x, dx: x + dx
norm2 = lambda x, y: sqrt(x**2 + y**2)
