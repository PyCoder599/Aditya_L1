from .lagrange import compute_L1


def halo_initial_conditions(amplitude=1e-3):
    x_L1 = compute_L1()

    x0 = x_L1 - 0.001
    y0 = 0
    z0 = 0.001

    vx0 = 0
    vy0 = 0.01
    vz0 = 0

    return [x0, y0, vx0, vy0]
