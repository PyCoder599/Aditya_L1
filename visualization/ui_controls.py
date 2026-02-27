from vpython import button, slider, wtext, vector


def create_ui(simulation):
    def toggle_run(b):
        simulation["running"] = not simulation["running"]
        b.text = "Pause" if simulation["running"] else "Start"

    def change_speed(s):
        simulation["speed"] = s.value

    button(text="Pause", bind=toggle_run)
    wtext(text="   Speed:")
    slider(min=0.1, max=10, value=1, length=200, bind=change_speed)


def create_zoom_controls(scene):

    def zoom_in(b):
        scene.range *= 0.8

    def zoom_out(b):
        scene.range *= 1.2

    button(text="Zoom In", bind=zoom_in)
    button(text="Zoom Out", bind=zoom_out)


def add_restart(simulation):

    def restart(b):
        simulation["state"].clear()
        simulation["state"].update(simulation["init_func"]())

        # Clear trails
        simulation["earth"].clear_trail()
        simulation["moon"].clear_trail()

    button(text="Restart", bind=restart)


def add_focus_controls(simulation):

    def focus_sun(b):
        simulation["focus"] = "sun"

    def focus_earth(b):
        simulation["focus"] = "earth"

    def focus_L1(b):
        simulation["focus"] = "L1"

    button(text="Focus Sun", bind=focus_sun)
    button(text="Focus Earth", bind=focus_earth)
    button(text="Focus L1", bind=focus_L1)


def add_lagrange(simulation):
    def toggle_lagrange(b):
        simulation["Lagrange"] = not simulation["Lagrange"]
        b.text = "Hide Lagrange Points" if simulation["Lagrange"] else "Show Lagrange Points"

    button(text="Show Lagrange Points", bind=toggle_lagrange)


def aditya_L1(simulation):
    def Launch_aditya(b):
        simulation["launch_aditya"] = True

    button(text="Launch Aditya-L1", bind=Launch_aditya)
