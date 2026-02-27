import numpy as np
from .constants import M_EARTH, M_SUN


def compute_Lagrange_points(state):
    """
    Returns dictionary with L1-L5 positions in SI units
    """

    xs, ys, zs = state["xs"], state["ys"], state["zs"]
    xe, ye, ze = state["xe"], state["ye"], state["ze"]

    # Vector Earth relative to Sun
    rx = xe - xs
    ry = ye - ys
    rz = ze - zs

    R = np.sqrt(rx ** 2 + ry ** 2 + rz ** 2)

    # Unit vector from Sun to Earth
    ux = rx / R
    uy = ry / R
    uz = rz / R

    # Approximate L1 and L2 distance from Earth
    r_L = R * (M_EARTH / (3 * M_SUN)) ** (1 / 3)

    # L1 (between Sun and Earth)
    L1 = (
        xe - r_L * ux,
        ye - r_L * uy,
        ze - r_L * uz
    )

    # L2 (beyond Earth)
    L2 = (
        xe + r_L * ux,
        ye + r_L * uy,
        ze + r_L * uz
    )

    # L3 (opposite side of Sun)
    L3 = (
        xs - R * ux,
        ys - R * uy,
        zs - R * uz
    )

    # Perpendicular vector for L4/L5
    # Cross product with z-axis for 3D perpendicular
    perp_x = -uy
    perp_y = ux
    perp_z = 0

    # Normalize perpendicular
    norm = np.sqrt(perp_x ** 2 + perp_y ** 2 + perp_z ** 2)
    perp_x /= norm
    perp_y /= norm
    perp_z /= norm

    # L4 (60° ahead)
    L4 = (
        xs + R * (0.5 * ux + np.sqrt(3) / 2 * perp_x),
        ys + R * (0.5 * uy + np.sqrt(3) / 2 * perp_y),
        zs + R * (0.5 * uz + np.sqrt(3) / 2 * perp_z)
    )

    # L5 (60° behind)
    L5 = (
        xs + R * (0.5 * ux - np.sqrt(3) / 2 * perp_x),
        ys + R * (0.5 * uy - np.sqrt(3) / 2 * perp_y),
        zs + R * (0.5 * uz - np.sqrt(3) / 2 * perp_z)
    )

    return {
        "L1": L1,
        "L2": L2,
        "L3": L3,
        "L4": L4,
        "L5": L5
    }

