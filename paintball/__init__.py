from controllers import BlinkAnimator, StillAnimator
from utils import coord_3d_to_linear, coord_linear_to_3d, position_change

class Game:
    def __init__(self, ge):
        self.ge = ge

        self.reset_game()
        self.ge.change_state(self.process_play)

    def reset_game(self):
        self.position = [coord_3d_to_linear(0, 0, 0), coord_3d_to_linear(3, 3, 3)]
        self.cubestate = [-1] * 64
        self.cubestate[self.position[0]] = 0
        self.cubestate[self.position[1]] = 1

    def move(self, n, event):
        if event.startswith(f'player{n+1}:'):
            btn = event[8:]
            if btn == 'x+': self.position[n] = position_change(self.position[n], dx=1)
            elif btn == 'x-': self.position[n] = position_change(self.position[n], dx=-1)
            elif btn == 'y+': self.position[n] = position_change(self.position[n], dy=1)
            elif btn == 'y-': self.position[n] = position_change(self.position[n], dy=-1)
            elif btn == 'z+': self.position[n] = position_change(self.position[n], dz=1)
            elif btn == 'z-': self.position[n] = position_change(self.position[n], dz=-1)
            return True
        else:
            return False

    def process_play(self, event):
        if event == 'state:enter':
            self.ge.timer_add(0, 20)
            for i in range(64):
                self.ge.cube.set_animator(i, StillAnimator(self.ge.player_color(self.cubestate[i])))

        elif event == 'timer:0':
            c0 = self.cubestate.count(0)
            c1 = self.cubestate.count(1)
            if c0 >= c1:
                for i in range(64):
                    if self.cubestate[i] == 0:
                        self.ge.cube.set_animator(i, BlinkAnimator(self.ge.player_color(0)))
            if c0 <= c1:
                for i in range(64):
                    if self.cubestate[i] == 1:
                        self.ge.cube.set_animator(i, BlinkAnimator(self.ge.player_color(1)))
            self.ge.change_state(self.process_end_game)

        elif self.move(0, event):
            self.ge.cube.set_animator(self.position[0], StillAnimator(self.ge.player_color(0)))
            self.cubestate[self.position[0]] = 0

        elif self.move(1, event):
            self.ge.cube.set_animator(self.position[1], StillAnimator(self.ge.player_color(1)))
            self.cubestate[self.position[1]] = 1

    def process_end_game(self, event):
        if event == 'state:enter':
            self.ge.sound.play('end')

        elif event == 'player1:valid' or event == 'player2:valid':
            self.reset_game()
            self.ge.change_state(self.process_play)
