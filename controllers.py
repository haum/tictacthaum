#! /usr/bin/env python3
# -*- coding:utf8 -*-

class Cube:
    def __init__(self, tals_controller):
        self.animators = [StillAnimator((0,0,0)) for _ in range(64)]
        self.tals = tals_controller

    def set_animator(self, i, anim):
        assert(i >= 0 and i <= 63)
        self.animators[i] = anim

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
