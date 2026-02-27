import numpy as np

# Physical Constants (SI)
G = 6.67430e-11

M_SUN = 1.989e30
M_EARTH = 5.972e24

AU = 1.496e11
YEAR = 365.25 * 24 * 3600

e_earth = 0.0167

M_MOON = 7.347e22
MOON_DISTANCE = 384400000  # meters
MOON_PERIOD = 27.3 * 24 * 3600
MOON_INCLINATION = np.radians(5.145)

# CR3BP normalized parameter
MU = M_EARTH / (M_SUN + M_EARTH)
