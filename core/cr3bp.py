import numpy as np
from .constants import MU


def equations(t, state):
    x, y, vx, vy = state

    r1 = np.sqrt((x + MU)**2 + y**2)
    r2 = np.sqrt((x - 1 + MU)**2 + y**2)

    ax = 2*vy + x - (1-MU)*(x+MU)/r1**3 - MU*(x-1+MU)/r2**3

    ay = -2*vx + y - (1-MU)*y/r1**3 - MU*y/r2**3

    return [vx, vy, ax, ay]
