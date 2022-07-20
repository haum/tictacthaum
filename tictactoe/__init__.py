import itertools
from controllers import BlinkAnimator, StillAnimator
from utils import coord_3d_to_linear, coord_linear_to_3d

class Game:
    def __init__(self, ge):
        self.ge = ge

        self.winlines = []
        for i, j in itertools.product(range(4), repeat=2):
            self.winlines.append(tuple(coord_3d_to_linear(i,j,k) for k in range(4)))
            self.winlines.append(tuple(coord_3d_to_linear(i,k,j) for k in range(4)))
            self.winlines.append(tuple(coord_3d_to_linear(k,i,j) for k in range(4)))
        for i in range(4):
            self.winlines.append(tuple(coord_3d_to_linear(i,k,k) for k in range(4)))
            self.winlines.append(tuple(coord_3d_to_linear(k,i,k) for k in range(4)))
            self.winlines.append(tuple(coord_3d_to_linear(k,k,i) for k in range(4)))
            self.winlines.append(tuple(coord_3d_to_linear(i,k,3-k) for k in range(4)))
            self.winlines.append(tuple(coord_3d_to_linear(k,i,3-k) for k in range(4)))
            self.winlines.append(tuple(coord_3d_to_linear(k,3-k,i) for k in range(4)))
        self.winlines.append(tuple(coord_3d_to_linear(k,k,k) for k in range(4)))
        self.winlines.append(tuple(coord_3d_to_linear(3-k,k,k) for k in range(4)))
        self.winlines.append(tuple(coord_3d_to_linear(k,3-k,k) for k in range(4)))
        self.winlines.append(tuple(coord_3d_to_linear(k,k,3-k) for k in range(4)))

        self.reset_game()
        self.ge.change_state(self.process_playerN_plays)

    def change_player(self, v=None):
        if v == self.curplayer: return
        if v is None: v = 1 - self.curplayer
        self.curplayer = v
        b = self.curplayer == 0
        self.ge.r1.set_leds(b, b, b)
        b = not b
        self.ge.r2.set_leds(b, b, b)

    def reset_game(self):
        self.position = [0, 0]
        self.cubestate = [-1] * 64
        self.curplayer = -1
        self.change_player(0)

    def redraw_cube(self):
        for p in range(64):
            self.ge.cube.set_animator(p, StillAnimator(self.color_pos(p)))

    def color_pos(self, p):
        return self.color_player(self.cubestate[p])

    def color_player(self, p):
        if p == 0: return (255, 255, 0)
        elif p == 1: return (255, 0, 255)
        return (0, 0, 0)

    def position_change(self, pos, dx=0, dy=0, dz=0):
        pos3d = coord_linear_to_3d(pos)
        return coord_3d_to_linear(
            (pos3d[0] + dx) % 4,
            (pos3d[1] + dy) % 4,
            (pos3d[2] + dz) % 4
        )

    def process_playerN_plays(self, event):
        if event == 'state:enter':
            self.redraw_cube()
            if self.cubestate[self.position[self.curplayer]] == self.curplayer:
                self.ge.cube.set_animator(self.position[self.curplayer], BlinkAnimator((255, 255, 255), self.color_player(self.curplayer)))
            else:
                self.ge.cube.set_animator(self.position[self.curplayer], BlinkAnimator(self.color_pos(self.position[self.curplayer]), self.color_player(self.curplayer)))

        elif event.startswith(f'player{self.curplayer+1}:button:'):
            self.ge.cube.set_animator(self.position[self.curplayer], StillAnimator(self.color_pos(self.position[self.curplayer])))
            btn = event[15:]

            if btn in ('show', 'show_x', 'show_y', 'show_z'): return self.ge.change_state(self.process_show_xyz)
            elif btn == 'x+': self.position[self.curplayer] = self.position_change(self.position[self.curplayer], dx=1)
            elif btn == 'x-': self.position[self.curplayer] = self.position_change(self.position[self.curplayer], dx=-1)
            elif btn == 'y+': self.position[self.curplayer] = self.position_change(self.position[self.curplayer], dy=1)
            elif btn == 'y-': self.position[self.curplayer] = self.position_change(self.position[self.curplayer], dy=-1)
            elif btn == 'z+': self.position[self.curplayer] = self.position_change(self.position[self.curplayer], dz=1)
            elif btn == 'z-': self.position[self.curplayer] = self.position_change(self.position[self.curplayer], dz=-1)
            if self.cubestate[self.position[self.curplayer]] == self.curplayer:
                self.ge.cube.set_animator(self.position[self.curplayer], BlinkAnimator((255, 255, 255), self.color_player(self.curplayer)))
            else:
                self.ge.cube.set_animator(self.position[self.curplayer], BlinkAnimator(self.color_pos(self.position[self.curplayer]), self.color_player(self.curplayer)))

            if btn == 'valid' and self.cubestate[self.position[self.curplayer]] == -1:
                self.cubestate[self.position[self.curplayer]] = self.curplayer
                self.ge.cube.set_animator(self.position[self.curplayer], StillAnimator(self.color_pos(self.position[self.curplayer])))
                win = False
                for l in self.winlines:
                    v = self.cubestate[l[0]]
                    if v != -1 and v == self.cubestate[l[1]] and v == self.cubestate[l[2]] and v == self.cubestate[l[3]]:
                        win = True
                        for p in l:
                            self.ge.cube.set_animator(p, BlinkAnimator(self.color_player(v)))
                self.change_player()
                self.ge.change_state(self.process_end_game if win else self.process_playerN_plays)

    def process_show_xyz(self, event):
        def redraw(x_axis = False, y_axis = False, z_axis = False):
            for i in range(64):
                self.ge.cube.set_animator(i, StillAnimator((0,0,0)))
            x, y, z = coord_linear_to_3d(self.position[self.curplayer])
            for i in range(4):
                self.ge.cube.set_animator(coord_3d_to_linear(i, y, z), BlinkAnimator((255, 0, 0)) if x_axis else StillAnimator((255, 0, 0)))
                self.ge.cube.set_animator(coord_3d_to_linear(x, i, z), BlinkAnimator((0, 255, 0)) if y_axis else StillAnimator((0, 255, 0)))
                self.ge.cube.set_animator(coord_3d_to_linear(x, y, i), BlinkAnimator((0, 0, 255)) if z_axis else StillAnimator((0, 0, 255)))
            self.ge.cube.set_animator(coord_3d_to_linear(x, y, z), BlinkAnimator(self.color_player(self.curplayer)))

        if event == 'state:enter': redraw()
        elif event == f'player{self.curplayer+1}:button:off': self.ge.change_state(self.process_playerN_plays)
        elif event == f'player{self.curplayer+1}:button:show_x': redraw(x_axis=True)
        elif event == f'player{self.curplayer+1}:button:show_y': redraw(y_axis=True)
        elif event == f'player{self.curplayer+1}:button:show_z': redraw(z_axis=True)
        elif event == f'player{self.curplayer+1}:button:show': redraw()

    def process_end_game(self, event):
        if event == 'player1:button:valid' or event == 'player2:button:valid':
            self.reset_game()
            self.ge.change_state(self.process_playerN_plays)
