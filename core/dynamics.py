import numpy as np
from .constants import G, M_SUN, M_EARTH


def compute_acceleration(state):
    dx = state["xe"] - state["xs"]
    dy = state["ye"] - state["ys"]
    dz = state["ze"] - state["zs"]

    r = np.sqrt(dx**2 + dy**2 + dz**2)

    # Avoid division by zero
    if r == 0:
        return 0, 0, 0, 0, 0, 0

    ax_s = G * M_EARTH * dx / r**3
    ay_s = G * M_EARTH * dy / r**3
    az_s = G * M_EARTH * dz / r**3

    ax_e = -G * M_SUN * dx / r**3
    ay_e = -G * M_SUN * dy / r ** 3
    az_e = -G * M_SUN * dz / r ** 3

    return ax_s, ay_s, az_s, ax_e, ay_e, az_e
