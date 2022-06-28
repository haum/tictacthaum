#! /usr/bin/env python3
# -*- coding:utf8 -*-

import time

from controllers import Cube, BlinkAnimator, StillAnimator

timestep = 1/30

c = Cube()

while True:
    time.sleep(timestep)
    c.animate(timestep)
