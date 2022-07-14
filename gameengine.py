from controllers import BlinkAnimator, StillAnimator
from utils import coord_3d_to_linear

colors = [
    [(255, 0, 0), (255, 255, 0)],
    [(0, 255, 0), (255, 0, 255)],
    [(0, 0, 255), (255, 255, 0)],
    [(255, 0, 0), (255, 0, 255)],
    [(255, 0, 255), (255, 0, 255)],
    [(255, 0, 0), (255, 0, 0)],
    [(255, 255, 0), (255, 255, 0)],
]

class GameEngine:
    def __init__(self, cube):
        self.cube = cube
        self.colornb = 0

    def process(self, event):
        if event[0] == 'remote1' and event[1] != b'0':
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        self.cube.set_animator(coord_3d_to_linear(i, j, k), StillAnimator(colors[self.colornb][k>1]))
            self.colornb += 1
            self.colornb %= len(colors)
