import numpy as np
from scipy.optimize import root_scalar
from .constants import MU


def collinear_equation(x):
    r1 = abs(x + MU)
    r2 = abs(x - 1 + MU)
    return x - (1 - MU)*(x + MU)/r1**3 - MU*(x - 1 + MU)/r2**3


def compute_L1():
    xs = np.linspace(0.9, 1 - MU - 1e-4, 1000)

    for i in range(len(xs) - 1):
        if collinear_equation(xs[i]) * collinear_equation(xs[i + 1]) < 0:
            sol = root_scalar(
                collinear_equation,
                bracket=[xs[i], xs[i + 1]],
                method='brentq'
            )
            return sol.root

    raise RuntimeError("L1 root not found")

print("L1:", compute_L1())