from core.halo import halo_initial_conditions
from core.propagator import propagate
from visualization.plot2d import plot_trajectory


def main():
    state0 = halo_initial_conditions(amplitude=0.002)
    solution = propagate(state0, t_final=102)
    plot_trajectory(solution)


if __name__ == "__main__":
    main()
