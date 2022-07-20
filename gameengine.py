import importlib
import time

class GameEngine:
    def __init__(self, cube, r1, r2, game):
        self.cube = cube
        self.r1 = r1
        self.r2 = r2
        self._state = self.nullstate
        self._timers = []
        try:
            mod = importlib.import_module(game)
            self._game = mod.Game(self)
        except ModuleNotFoundError:
            print('Invalid game')

    def nullstate(self, event):
        pass

    def change_state(self, next_state):
        self._state('state:exit')
        self._state = next_state
        self._state('state:enter')

    def timer_add(self, n, t):
        self.timer_rm(n)
        self._timers.append((time.time()+t, n))

    def timer_rm(self, n):
        self._timers = [x for x in self._timers if x[1] != n]

    def process(self, rawevent):
        def button_name(data):
            if data == b'0': return 'off'
            elif data == b'1': return 'x+'
            elif data == b'2': return 'z+'
            elif data == b'4': return 'y+'
            elif data == b'8': return 'x-'
            elif data == b'16': return 'z-'
            elif data == b'32': return 'y-'
            elif data == b'64': return 'cancel'
            elif data == b'128': return 'show'
            elif data == b'256': return 'valid'
            elif data == b'129' or data == b'136': return 'show_x'
            elif data == b'130' or data == b'144': return 'show_z'
            elif data == b'132' or data == b'160': return 'show_y'
            return None

        if rawevent[0] == 'tic':
            now = time.time()
            removable = False
            for t, n in self._timers:
                if t <= now:
                    removable = True
                    self._state(f'timer:{n}')
            if removable:
                self._timers = [x for x in self._timers if x[0] > now]

        elif rawevent[0] == 'remote1':
            btn = button_name(rawevent[1])
            if btn:
                self._state('player1:'+btn)
        elif rawevent[0] == 'remote2':
            btn = button_name(rawevent[1])
            if btn:
                self._state('player2:'+btn)
        elif rawevent[0] == 'console':
            if rawevent[1]:
                self._state(rawevent[1])
