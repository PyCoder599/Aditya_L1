import numpy as np
from constants import M_SUN, M_EARTH, AU


def compute_L1_distance():
    r_L1 = AU * (M_EARTH / (3 * M_SUN))**(1/3)
    return r_L1


def compute_L1_position():
    r_L1 = compute_L1_distance()
    x_L1 = AU - r_L1
    return x_L1
