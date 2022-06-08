#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# tictacthaum.py
#
# Copyright © 2022 HAUM <contact@haum.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#


import time

from controllers import Cube, BlinkAnimator, StillAnimator

timestep = 1/30

c = Cube()

while True:
    time.sleep(timestep)
    c.animate(timestep)
