import numpy as np


def step(state, dt, speed, acceleration_function):

    ax_s, ay_s, az_s, ax_e, ay_e, az_e = acceleration_function(state)
    # Update velocities
    state["vxs"] += ax_s * dt * speed
    state["vys"] += ay_s * dt * speed
    state["vzs"] += az_s * dt * speed

    state["vxe"] += ax_e * dt * speed
    state["vye"] += ay_e * dt * speed
    state["vze"] += az_e * dt * speed

    # Update positions
    state["xs"] += state["vxs"] * dt * speed
    state["ys"] += state["vys"] * dt * speed
    state["zs"] += state["vzs"] * dt * speed

    state["xe"] += state["vxe"] * dt * speed
    state["ye"] += state["vye"] * dt * speed
    state["ze"] += state["vze"] * dt * speed


    return state
