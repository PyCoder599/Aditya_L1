import numpy as np
from scipy.integrate import solve_ivp
from cr3bp import equations


def propagate(state0, t_final=10, steps=5000):
    t_span = (0, t_final)
    t_eval = np.linspace(0, t_final, steps)

    sol = solve_ivp(equations, t_span, state0, t_eval=t_eval)

    return sol
