import numpy as np
from .constants import G, M_SUN, M_EARTH


def compute_acceleration(state):
    dx = state["xe"] - state["xs"]
    dy = state["ye"] - state["ys"]

    r = np.sqrt(dx**2 + dy**2)

    ax_s = G * M_EARTH * dx / r**3
    ay_s = G * M_EARTH * dy / r**3

    ax_e = -G * M_SUN * dx / r**3
    ay_e = -G * M_SUN * dy / r**3

    return ax_s, ay_s, ax_e, ay_e
