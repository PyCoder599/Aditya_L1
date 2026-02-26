from core.kepler_orbit import kepler_initial_conditions
from visualization.solar_system import run_simulation


def main():
    state = kepler_initial_conditions(e=0.0167)
    run_simulation(state, kepler_initial_conditions)


if __name__ == "__main__":
    main()
