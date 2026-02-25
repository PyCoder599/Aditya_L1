import numpy as np
import matplotlib
matplotlib.use("TKAgg")
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# -----------------------------
# Physical Constants (SI Units)
# -----------------------------

G = 6.67430e-11
M_sun = 1.989e30
AU = 1.496e11

# -----------------------------
# Initial Conditions
# -----------------------------

# Start Earth at (AU, 0)
x0 = AU
y0 = 0

# Circular orbit velocity
v0 = np.sqrt(G * M_sun / AU)

vx0 = 0
vy0 = v0

state0 = [x0, y0, vx0, vy0]


# -----------------------------
# Equations of Motion
# -----------------------------

def two_body(t, state):
    x, y, vx, vy = state

    r = np.sqrt(x ** 2 + y ** 2)

    ax = -G * M_sun * x / r ** 3
    ay = -G * M_sun * y / r ** 3

    return [vx, vy, ax, ay]


# -----------------------------
# Time span (1 year)
# -----------------------------

year = 365 * 24 * 3600
t_span = (0, year)
t_eval = np.linspace(0, year, 5000)

sol = solve_ivp(two_body, t_span, state0, t_eval=t_eval, rtol=1e-10, atol=1e-12)

# -----------------------------
# Plot
# -----------------------------

plt.figure(figsize=(6, 6))
plt.plot(sol.y[0], sol.y[1])
plt.scatter(0, 0, label="Sun")
plt.gca().set_aspect('equal')
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Earth Orbit Around Sun (SI Units)")
plt.legend()
plt.grid()
plt.show()

# Print orbital period check
print("Final position (m):", sol.y[0][-1], sol.y[1][-1])
print("Initial velocity (m/s):", v0)