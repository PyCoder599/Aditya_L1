import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
from core.constants import MU


def plot_trajectory(solution):
    x = solution.y[0]
    y = solution.y[1]

    plt.figure()
    plt.plot(x, y, label="Spacecraft")
    plt.scatter(-MU, 0, label="Sun")
    plt.scatter(1-MU, 0, label="Earth")

    plt.xlabel("x (normalized)")
    plt.ylabel("y (normalized)")
    plt.legend()
    plt.title("Aditya-L1 CR3BP Simulation")
    plt.grid()
    plt.show()
