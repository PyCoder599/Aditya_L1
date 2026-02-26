import numpy as np
import matplotlib
matplotlib.use("TKAgg")
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from core.constants import *

# -------------------------
# Initial Positions (Barycenter at origin)
# -------------------------

r_sun = (M_EARTH / (M_SUN + M_EARTH)) * AU
r_earth = (M_SUN / (M_SUN + M_EARTH)) * AU

# Sun at negative x
x_s0 = -r_sun
y_s0 = 0

# Earth at positive x
x_e0 = r_earth
y_e0 = 0

# Orbital angular velocity
omega = np.sqrt(G * (M_SUN + M_EARTH) / AU ** 3)

# Velocities perpendicular to radius
vx_s0 = 0
vy_s0 = -omega * r_sun

vx_e0 = 0
vy_e0 = omega * r_earth

state0 = [
    x_s0, y_s0, vx_s0, vy_s0,
    x_e0, y_e0, vx_e0, vy_e0
]


# -------------------------
# Equations
# -------------------------

def two_body_mutual(t, state):
    xs, ys, vxs, vys, xe, ye, vxe, vye = state

    dx = xe - xs
    dy = ye - ys
    r = np.sqrt(dx ** 2 + dy ** 2)

    ax_s = G * M_EARTH * dx / r ** 3
    ay_s = G * M_EARTH * dy / r ** 3

    ax_e = -G * M_SUN * dx / r ** 3
    ay_e = -G * M_SUN * dy / r ** 3

    return [
        vxs, vys, ax_s, ay_s,
        vxe, vye, ax_e, ay_e
    ]


# -------------------------
# Time span (1 year)
# -------------------------

t_span = (0, YEAR)
t_eval = np.linspace(0, YEAR, 1000)

sol = solve_ivp(
    two_body_mutual,
    t_span,
    state0,
    t_eval=t_eval,
    rtol=1e-10,
    atol=1e-12
)

# -------------------------
# Plot
# -------------------------

plt.figure(figsize=(6, 6))
plt.plot(sol.y[0], sol.y[1], label="Sun")
plt.plot(sol.y[4], sol.y[5], label="Earth")
plt.scatter(0, 0, label="Barycenter")
plt.gca().set_aspect('equal')
plt.legend()
plt.title("Sun–Earth Mutual Orbit (Barycentric Frame)")
plt.grid()
plt.show()

fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal')
ax.set_xlim(-1.1*AU, 1.1*AU)
ax.set_ylim(-1.1*AU, 1.1*AU)

sun_dot, = ax.plot([], [], 'yo', markersize=8)
earth_dot, = ax.plot([], [], 'bo', markersize=4)

sun_path, = ax.plot([], [], 'y-', linewidth=1)
earth_path, = ax.plot([], [], 'b-', linewidth=1)

def update(frame):
    sun_dot.set_data(sol.y[0][frame], sol.y[1][frame])
    earth_dot.set_data(sol.y[4][frame], sol.y[5][frame])

    sun_path.set_data(sol.y[0][:frame], sol.y[1][:frame])
    earth_path.set_data(sol.y[4][:frame], sol.y[5][:frame])

    return sun_dot, earth_dot, sun_path, earth_path


ani = animation.FuncAnimation(
    fig, update,
    frames=len(sol.t),
    interval=5
)

plt.show()

