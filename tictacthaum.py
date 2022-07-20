#! /usr/bin/env python3
# -*- coding:utf8 -*-

import argparse
import select
import sys
import time

from utils import coord_3d_to_linear
from controllers import Cube, Remote, BlinkAnimator, StillAnimator
from gameengine import GameEngine
from legacy import TalController

parser = argparse.ArgumentParser(description='Tic Tac THaum')
parser.add_argument('-r1', '--remote1', help='Number of first remote')
parser.add_argument('-r2', '--remote2', help='Number of second remote')
parser.add_argument('-g', '--game', default='tictactoe', help='Game name')
args = parser.parse_args()

timestep = 1/30

tc = TalController()
c = Cube(tc)
r1 = Remote(args.remote1)
r2 = Remote(args.remote2)
ge = GameEngine(c, r1, r2, args.game)

while True:
    time.sleep(timestep)
    c.animate(timestep)
    ge.process(('tic', ))

    toread = select.select([a for a in (sys.stdin, r1.fd(), r2.fd()) if a], [], [], 0)[0]
    if r1.fd() in toread:
        for e in r1.get_events():
            ge.process(('remote1', e))
    if r2.fd() in toread:
        for e in r2.get_events():
            ge.process(('remote2', e))
    if sys.stdin in toread:
        line = sys.stdin.readline().strip()
        ge.process(('console', line))
