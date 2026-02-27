import random
import numpy as np
from vpython import sphere, vector, rate, color, canvas, local_light
from core.constants import AU, MOON_PERIOD, MOON_DISTANCE, MOON_INCLINATION
from core.dynamics import compute_acceleration
from core.integrator import step
from .ui_controls import create_ui, create_zoom_controls, add_restart, add_focus_controls


def run_simulation(state, initial_state_func):

    scene = canvas(title="Interactive Solar System",
                   width=1000, height=700,
                   background=color.black)

    scene.autoscale = False
    scene.range = 2  # zoom level

    visual_scale = 1/AU * 5

    sun = sphere(radius=0.05, color=color.orange, emissive=True)
    earth = sphere(radius=0.007, color=color.blue, make_trail=True, trail_radius=0.002, retain=500)
    earth.rotate_speed = 2 * np.pi / (24 * 3600)

    moon = sphere(radius=0.002, color=color.white, make_trail=True, trail_radius=0.001, retain=500)
    moon_angle = 0
    moon_angular_speed = 2 * np.pi / MOON_PERIOD

    local_light(pos=sun.pos, color=color.white)

    simulation = {
        "running": True,
        "speed": 1,
        "state": state,
        "init_func": initial_state_func,
        "earth": earth,
        "moon": moon,
        "scene": scene,
        "focus": "sun"
    }

    create_ui(simulation)
    create_zoom_controls(scene)
    add_restart(simulation)
    add_focus_controls(simulation)

    dt = 60 * 60 * 6

    for _ in range(200):
        sphere(
            pos=vector(random.uniform(-5, 5),
                       random.uniform(-5, 5),
                       random.uniform(-5, 5)),
            radius=0.005,
            color=color.white,
            emissive=True
        )

    while True:
        rate(200)

        if simulation["running"]:
            state = step(state, dt, simulation["speed"], compute_acceleration)
            moon_angle += moon_angular_speed * dt * simulation["speed"]

        if simulation["focus"] == "sun":
            scene.center = vector(0, 0, 0)

        elif simulation["focus"] == "earth":
            scene.center = earth.pos

        sun.pos = vector(state["xs"] * visual_scale, state["ys"] * visual_scale, state["zs"] * visual_scale)

        earth.pos = vector(state["xe"] * visual_scale, state["ye"] * visual_scale, state["ze"] * visual_scale)
        earth.rotate(angle=earth.rotate_speed * dt * simulation["speed"], axis=vector(0, 0, 1))

        # Local circular orbit
        x_orb = MOON_DISTANCE * np.cos(moon_angle)
        y_orb = MOON_DISTANCE * np.sin(moon_angle)
        z_orb = 0
        # Tilt orbit around X-axis
        y_tilt = y_orb * np.cos(MOON_INCLINATION)
        z_tilt = y_orb * np.sin(MOON_INCLINATION)

        moon_x = state["xe"] + x_orb
        moon_y = state["ye"] + y_tilt
        moon_z = state["ze"] + z_tilt
        moon.pos = vector(moon_x * visual_scale, moon_y * visual_scale, moon_z * visual_scale)

