def step(state, dt, speed, acceleration_function):

    ax_s, ay_s, ax_e, ay_e = acceleration_function(state)

    # Update velocities
    state["vxs"] += ax_s * dt * speed
    state["vys"] += ay_s * dt * speed
    state["vxe"] += ax_e * dt * speed
    state["vye"] += ay_e * dt * speed

    # Update positions
    state["xs"] += state["vxs"] * dt * speed
    state["ys"] += state["vys"] * dt * speed
    state["xe"] += state["vxe"] * dt * speed
    state["ye"] += state["vye"] * dt * speed

    return state
