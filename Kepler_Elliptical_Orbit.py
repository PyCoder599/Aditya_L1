import numpy as np
import matplotlib
matplotlib.use("TKAgg")
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -------------------------
# Constants
# -------------------------

G = 6.67430e-11
M_sun = 1.989e30
M_earth = 5.972e24
AU = 1.496e11

# -------------------------
# Kepler Parameters
# -------------------------

a = AU
e = 0.0167

rp = a * (1 - e)

# Perihelion velocity (vis-viva equation)
vp = np.sqrt(G * (M_sun + M_earth) * (1 + e) / (a * (1 - e)))

# -------------------------
# Initial Conditions
# -------------------------

# Earth at perihelion on x-axis
x_e0 = rp
y_e0 = 0

vx_e0 = 0
vy_e0 = vp

# Sun initial position from barycenter condition
r_sun = (M_earth / (M_sun + M_earth)) * rp
x_s0 = -r_sun
y_s0 = 0

vx_s0 = 0
vy_s0 = - (M_earth / M_sun) * vp

state0 = [
    x_s0, y_s0, vx_s0, vy_s0,
    x_e0, y_e0, vx_e0, vy_e0
]


# -------------------------
# Equations of Motion
# -------------------------

def two_body_mutual(t, state):
    xs, ys, vxs, vys, xe, ye, vxe, vye = state

    dx = xe - xs
    dy = ye - ys
    r = np.sqrt(dx ** 2 + dy ** 2)

    ax_s = G * M_earth * dx / r ** 3
    ay_s = G * M_earth * dy / r ** 3

    ax_e = -G * M_sun * dx / r ** 3
    ay_e = -G * M_sun * dy / r ** 3

    return [
        vxs, vys, ax_s, ay_s,
        vxe, vye, ax_e, ay_e
    ]


# -------------------------
# Integrate for 1 year
# -------------------------

year = 365.25 * 24 * 3600
t_span = (0, year)
t_eval = np.linspace(0, year, 4000)

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
# Sun trajectory
plt.plot(sol.y[0], sol.y[1], label="Sun", color="orange")

# Earth trajectory
plt.plot(sol.y[4] - sol.y[0], sol.y[5] - sol.y[1])

# Barycenter
plt.scatter(0, 0, color="black", label="Barycenter")

plt.gca().set_aspect('equal')
plt.legend()
plt.title("Sun–Earth Mutual Elliptical Orbit")
plt.grid()
plt.show()

print("Perihelion velocity (m/s):", vp)

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
