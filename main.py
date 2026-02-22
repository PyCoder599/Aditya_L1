from core.propagator import propagate
from visualization.plot2d import plot_trajectory


def main():
    # Initial condition near L1
    state0 = [0.99, 0.01, 0.0, 0.0]

    solution = propagate(state0)

    plot_trajectory(solution)


if __name__ == "__main__":
    main()
