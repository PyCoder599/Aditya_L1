import random
import numpy as np
from vpython import sphere, vector, rate, color, canvas, local_light, label
from core.constants import *
from core.dynamics import compute_acceleration
from core.integrator import step
from core.lagrange import compute_Lagrange_points
from .ui_controls import *


def run_simulation(state, initial_state_func):
    SIZE_SCALE = 20
    scene = canvas(title="Interactive Solar System",
                   width=1300, height=650,
                   background=color.black)

    scene.autoscale = False
    scene.range = 2  # zoom level

    visual_scale = 1/AU * 5

    sun = sphere(
        radius=R_SUN * visual_scale * SIZE_SCALE,
        color=color.orange, emissive=True)
    earth = sphere(
        radius=R_EARTH * visual_scale * SIZE_SCALE,
        color=color.blue, make_trail=True, trail_radius=0.002, retain=500)
    earth.rotate_speed = 2 * np.pi / (24 * 3600)

    moon = sphere(
        radius=R_MOON * visual_scale * SIZE_SCALE,
        color=color.white, make_trail=True, trail_radius=0.001, retain=500)
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
        "focus": "sun",
        "Lagrange": False,
        "launch_aditya": False
    }

    create_ui(simulation)
    create_zoom_controls(scene)
    add_restart(simulation)
    add_focus_controls(simulation)
    add_lagrange(simulation)

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

    lagrange_spheres = {}
    lagrange_labels = {}
    for name in ["L1", "L2", "L3", "L4", "L5"]:
        lagrange_spheres[name] = sphere(
            radius=0.003,
            color=color.yellow,
            emissive=True
        )
        lagrange_labels[name] = label(
            text=name,
            xoffset=10,
            yoffset=10,
            space=0,
            height=10,
            border=4,
            font='sans',
            visible=False
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

        elif simulation["focus"] == "L1":
            scene.center = scene.center = scene.center + 0.1*(lagrange_spheres["L1"].pos - scene.center)

        if simulation["Lagrange"]:
            L_points = compute_Lagrange_points(state)
            for name, pos in L_points.items():
                x, y, z = pos
                scaled_pos = vector(
                    x * visual_scale,
                    y * visual_scale,
                    z * visual_scale
                )

                lagrange_spheres[name].pos = scaled_pos
                lagrange_spheres[name].visible = True

                lagrange_labels[name].pos = scaled_pos + vector(0, 0.001, 0)
                lagrange_labels[name].visible = True
        else:
            for name in lagrange_spheres:
                lagrange_spheres[name].visible = False
                lagrange_labels[name].visible = False

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

