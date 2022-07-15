#! /usr/bin/env python3
# -*- coding:utf8 -*-

import argparse
import select
import socket
import sys
import time

from utils import coord_3d_to_linear
from controllers import Cube, BlinkAnimator, StillAnimator
from gameengine import GameEngine
from legacy import TalController

parser = argparse.ArgumentParser(description='Tic Tac THaum')
parser.add_argument('--remote1', help='Number of first remote')
parser.add_argument('--remote2', help='Number of second remote')
args = parser.parse_args()

timestep = 1/30

tc = TalController()
c = Cube(tc)
ge = GameEngine(c)

r1 = None
if args.remote1 != None:
    r1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r1.connect((args.remote1, 540))
    r1.recv(1000)

r2 = None
if args.remote2 != None:
    r2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r2.connect((args.remote2, 540))
    r2.recv(1000)

while True:
    time.sleep(timestep)
    c.animate(timestep)

    toread = select.select([a for a in (sys.stdin, r1, r2) if a], [], [], 0)[0]
    if r1 in toread:
        lines = r1.recv(1000).strip().split()
        for l in lines:
            ge.process(('remote1', l))
    if r2 in toread:
        lines = r2.recv(1000).strip().split()
        for l in lines:
            ge.process(('remote2', l))
    if sys.stdin in toread:
        line = sys.stdin.readline().strip()
        ge.process(('console', line))
