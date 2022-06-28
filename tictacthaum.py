#! /usr/bin/env python3
# -*- coding:utf8 -*-

import time

from controllers import Cube, BlinkAnimator, StillAnimator
from legacy import TalController

timestep = 1/30

tc = TalController()
c = Cube(tc)

while True:
    time.sleep(timestep)
    c.animate(timestep)
