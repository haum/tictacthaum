import importlib
import time
from controllers import StillAnimator
from utils import coord_3d_to_linear

class GameEngine:
    def __init__(self, cube, r1, r2, game):
        self.cube = cube
        self.r1 = r1
        self.r2 = r2
        self.game = game
        self.player_colors = [
            ((255, 0, 0), (127, 0, 0)),
            ((0, 255, 0), (0, 127, 0)),
            ((0, 0, 255), (0, 0, 127)),
            ((0, 255, 255), (0, 127, 127)),
            ((255, 0, 255), (127, 0, 127)),
            ((255, 255, 0), (127, 127, 0)),
        ]
        self.player_colors_sel = [3, 5]
        self._state = self.nullstate
        self.change_state(self.process_config)
        self._timers = []

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

    def player_color(self, p, mod=False):
        if not p in (0, 1): return (0, 0, 0)
        c = self.player_colors_sel[p]
        return self.player_colors[c][mod]

    def process_config(self, event):
        def load_game():
            try:
                mod = importlib.import_module(self.game)
                self._game = mod.Game(self)
            except ModuleNotFoundError:
                print('Invalid game')

        def draw0():
            for p in (coord_3d_to_linear(0, 0, 0), coord_3d_to_linear(1, 0, 0), coord_3d_to_linear(0, 1, 0), coord_3d_to_linear(0, 0, 1)):
                self.cube.set_animator(p, StillAnimator(self.player_color(0)))

        def draw1():
            for p in (coord_3d_to_linear(3, 3, 3), coord_3d_to_linear(2, 3, 3), coord_3d_to_linear(3, 2, 3), coord_3d_to_linear(3, 3, 2)):
                self.cube.set_animator(p, StillAnimator(self.player_color(1)))

        if event == 'state:enter':
            draw0()
            draw1()

        elif event == 'player1:valid' or event == 'player2:valid':
            load_game()

        elif event in ('player1:x+', 'player1:x-', 'player1:y+', 'player1:y-', 'player1:z+', 'player1:z-'):
            self.player_colors_sel[0] += 1
            self.player_colors_sel[0] %= len(self.player_colors)
            if self.player_colors_sel[0] == self.player_colors_sel[1]:
                self.player_colors_sel[0] += 1
                self.player_colors_sel[0] %= len(self.player_colors)
            draw0()

        elif event in ('player2:x+', 'player2:x-', 'player2:y+', 'player2:y-', 'player2:z+', 'player2:z-'):
            self.player_colors_sel[1] += 1
            self.player_colors_sel[1] %= len(self.player_colors)
            if self.player_colors_sel[1] == self.player_colors_sel[0]:
                self.player_colors_sel[1] += 1
                self.player_colors_sel[1] %= len(self.player_colors)
            draw1()

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
