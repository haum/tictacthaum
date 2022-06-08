#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# controllers.py
#
# Copyright © 2021 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

import socket
import select
import time

import numpy as np
import sacn


class LedController:

    def __init__(self):
        self.fill()

        self.sender = sacn.sACNsender(source_name='On vous poutre tous')
        self.sender.start()
        self.sender.activate_output(1)
        self.sender.activate_output(2)
        self.sender[1].multicast = True
        self.sender[2].multicast = True

    def fill(self, val=[0]*3):
        self.chans = val*64*3

    def stop(self):
        self.fill()
        self.blit()
        self.sender.stop()

    def __setitem__(self, k, v):
        self.chans[k*3:(k+1)*3] = v

    def blit(self):
        self.sender[1].dmx_data = self.chans[:510]
        self.sender[2].dmx_data = self.chans[510:]


class TalController:

    def __init__(self):
        self.leds = LedController()

    def __setitem__(self, k, v):
        for l in range(3):
            self.leds[k*3+l] = v


class CubeController:

    def __init__(self):

        self.tals = TalController()
        self.m = np.array([1,35,38,40,15,25,33,32,18,23,28,31,20,21,22,30,55,45,43,41,5,2,36,39,13,16,26,34,12,19,24,29,58,53,48,42,63,56,46,44,8,6,3,37,11,14,17,27,60,52,51,50,61,59,54,49,62,64,57,47,10,9,7,4]).reshape(4,4,4)
        self.autoblit = True

    def __setitem__(self, k, v):
        self.tals[self.m[k]-1] = v
        if self.autoblit: self.blit()

    def fill(self, val=[0]*3):
        self.tals.leds.fill(val)
        if self.autoblit: self.blit()

    def blit(self):
        self.tals.leds.blit()

    def stop(self):
        self.tals.leds.stop()


class RemoteController:

    def __init__(self, nb):

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((f"192.168.88.24{nb}", 540))
        time.sleep(0.1)
        self.s.recv(1024)

    def send(self, v):
        self.s.send(bytes(str(v)+'\n\n', 'utf8'))

    def recv(self, timeout=0.01):
        readable, _, _ = select.select([self.s], [], [], timeout)
        if len(readable) > 0:
            return list(map(int, self.s.recv(1024).split()))
        else:
            return []

    def stop(self):
        self.s.close()


