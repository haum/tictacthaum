#! /usr/bin/env python3
# -*- coding:utf8 -*-

import socket
import time

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

class Remote:
    def __init__(self, ip):
        self.ip = ip
        self.s = None
        self.last_connect_try = 0
        self.connect()

    def connect(self):
        if not self.ip: return
        if self.last_connect_try + 5 > time.time(): return
        self.last_connect_try = time.time()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.ip, 540))
            self.s.recv(1000)
        except ConnectionRefusedError:
            print('Remote connection error')
            self.s.close()
            self.s = None

    def tic(self):
        if self.ip and not self.s:
            self.connect()

    def fd(self):
        return self.s

    def get_events(self):
        if not self.s: return []
        v = self.s.recv(1000)
        if v == b'':
            print('Remote connection lost')
            self.s.close()
            self.s = None
        return v.strip().split()

    def set_leds(self, l1, l2, l3):
        if not self.s: return
        v = 0
        if l1: v += 1
        if l2: v += 2
        if l3: v += 4
        try:
            self.s.send((str(v)+'\n').encode())
        except BrokenPipeError:
            print('Remote connection lost')
            self.s.close()
            self.s = None


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
