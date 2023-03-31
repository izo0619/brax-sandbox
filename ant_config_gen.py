# Colab setup and imports
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
import brax

# initialize brax configuration
ant = brax.Config()

torso = ant.bodies.add(name="$ Torso", mass=10)
cap = torso.colliders.add().capsule
cap.radius, cap.length, cap.end = 0.25, 0.5, 1
torso.inertia.x, torso.inertia.y, torso.inertia.z = 1, 1, 1

num_legs = 4
for leg in range(num_legs):
    angle = 360/num_legs * leg
    if angle > 180:
        # pos x rotation
        rot_x = 90
        # y rotation away from 90
        rot_y = angle - 90
    else:
        # neg x rotation
        rot_x = -90
        # y rotation away from -90
        rot_y = 270 - angle

    # upper limb
    uleg = ant.bodies.add(name=f"Upper {leg}", mass=1)
    cap = uleg.colliders.add().capsule
    rot = uleg.colliders.add().rotation
    cap.radius, cap.length = 0.08, 0.44
    rot.x, rot.y = rot_x, rot_y
    print(uleg)
    uleg.inertia.x, uleg.inertia.y, uleg.inertia.z = 1, 1, 1

    # bottom limb
    bleg = ant.bodies.add(name=f"Bottom {leg}", mass=1)
    print(bleg)
    cap = bleg.colliders.add().capsule
    cap.radius, cap.length = 0.08, 0.727
    rot = bleg.colliders.add().rotation
    rot.x, rot.y = rot_x, rot_y
    bleg.inertia.x, bleg.inertia.y, bleg.inertia.z = 1, 1, 1


print(ant)
