#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# controllers.py
#
# Copyright © 2022 HAUM <contact@haum.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

from legacy import TalController


class Cube:
    def __init__(self):
        self.animators = [StillAnimator((255,0,0))] + [BlinkAnimator((255, 255, 255), (0, 0, 255)) for i in range(63)]
        self.tals = TalController()

    def animate(self, dt):
        for i, a in enumerate(self.animators):
            self.tals[i] = a.animate(dt)
        self.tals.leds.blit()



class BlinkAnimator:
    def __init__(self, color, color2=(0,0,0), period=1):
        self.color = color
        self.color2 = color2
        self.t = 0
        self.period = period

    def animate(self, dt):
        self.t += dt
        if self.t > self.period:
            self.t = 0

        if self.t > self.period/2:
            c = self.color
        else:
            c = self.color2
        return c


class StillAnimator:
    def __init__(self, color):
        self.color = color

    def animate(self, dt):
        return self.color
