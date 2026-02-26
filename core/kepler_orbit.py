import numpy as np
from .constants import *


def kepler_initial_conditions(a=AU, e=e_earth):
    rp = a * (1 - e)

    v_rel = np.sqrt(G * (M_SUN + M_EARTH) * (1 + e) / (a * (1 - e)))

    # Barycentric distances
    r_s = (M_EARTH / (M_SUN + M_EARTH)) * rp
    r_e = (M_SUN / (M_SUN + M_EARTH)) * rp

    omega = v_rel / rp

    state = {
        "xs": -r_s,
        "ys": 0,
        "vxs": 0,
        "vys": -omega * r_s,
        "xe": r_e,
        "ye": 0,
        "vxe": 0,
        "vye": omega * r_e
    }

    return state
