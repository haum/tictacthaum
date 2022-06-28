#! /usr/bin/env python3
# -*- coding:utf8 -*-

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
