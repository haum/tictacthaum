#! /usr/bin/env python3
# -*- coding:utf8 -*-

import time

from utils import coord_3d_to_linear
from controllers import Cube, BlinkAnimator, StillAnimator
from legacy import TalController

timestep = 1/30

tc = TalController()
c = Cube(tc)

c.set_animator(coord_3d_to_linear(3, 0, 0), StillAnimator((255, 0, 0)))
c.set_animator(coord_3d_to_linear(0, 3, 0), StillAnimator((0, 255, 0)))
c.set_animator(coord_3d_to_linear(0, 0, 3), StillAnimator((0, 0, 255)))

while True:
    time.sleep(timestep)
    c.animate(timestep)
