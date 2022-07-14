from controllers import BlinkAnimator, StillAnimator
from utils import coord_3d_to_linear

def position_change(pos, dp):
    return (
        (pos[0] + dp[0]) % 4,
        (pos[1] + dp[1]) % 4,
        (pos[2] + dp[2]) % 4
    )

class GameEngine:
    def __init__(self, cube):
        self.cube = cube
        self.position1 = (0, 0, 0)
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    self.cube.set_animator(coord_3d_to_linear(i, j, k), StillAnimator((0, 0, 0)))

    def process(self, event):
        if event[0] == 'remote1' and event[1] != b'0':
            self.cube.set_animator(coord_3d_to_linear(*self.position1), StillAnimator((0, 0, 0)))
            if event[1] == b'1':
                self.position1 = position_change(self.position1, (1, 0, 0))
            elif event[1] == b'8':
                self.position1 = position_change(self.position1, (-1, 0, 0))
            if event[1] == b'2':
                self.position1 = position_change(self.position1, (0, 1, 0))
            elif event[1] == b'16':
                self.position1 = position_change(self.position1, (0, -1, 0))
            if event[1] == b'4':
                self.position1 = position_change(self.position1, (0, 0, 1))
            elif event[1] == b'32':
                self.position1 = position_change(self.position1, (0, 0, -1))
            self.cube.set_animator(coord_3d_to_linear(*self.position1), StillAnimator((255, 0, 255)))
