import itertools
import random
from controllers import BlinkAnimator, StillAnimator
from utils import coord_3d_to_linear, coord_linear_to_3d

class Game:
    def __init__(self, ge):
        self.ge = ge
        self.anim = 0
        self.anims = [m for m in dir(self) if m.startswith('anim_')]
        random.shuffle(self.anims)
        self.colorbase = 0
        self.period = 8
        self.ge.change_state(self.process_play)

    def color(self):
        pos = self.colorbase
        c = (0, 0, 0)
        m = 6 * 255
        if pos < 1/6:
            c = (255, pos * m, 0)
        elif pos < 2/6:
            pos -= 1/6
            c = (pos * m, 255, 0)
        elif pos < 3/6:
            pos -= 2/6
            c = (0, 255, pos * m)
        elif pos < 4/6:
            pos -= 3/6
            c = (0, pos * m, 255)
        elif pos < 5/6:
            pos -= 4/6
            c = (pos * m, 0, 255)
        else:
            pos -= 5/6
            c = (255, 0, pos * m)
        return tuple(map(int, c))

    def animation_send_event(self, ev):
        getattr(self, self.anims[self.anim])(ev)

    def process_play(self, event):
        asev = self.animation_send_event

        if event == 'state:enter':
            asev('anim:start')

        elif event == 'player1:x+' or event == 'player2:x+':
            self.colorbase = (self.colorbase + 1/12) % 1
            asev('anim:redraw')

        elif event == 'player1:x-' or event == 'player2:x-':
            self.colorbase = (self.colorbase - 1/12) % 1
            asev('anim:redraw')

        elif event == 'player1:y+' or event == 'player2:y+':
            asev('anim:stop')
            self.anim = (self.anim + 1) % len(self.anims)
            asev('anim:start')

        elif event == 'player1:y-' or event == 'player2:y-':
            asev('anim:stop')
            self.anim = self.anim - 1 if self.anim > 0 else len(self.anims) - 1
            asev('anim:start')

        elif event == 'player1:z+' or event == 'player2:z+':
            self.period /= 2
            if self.period < 0.5: self.period = 0.5
            asev('anim:redraw')

        elif event == 'player1:z-' or event == 'player2:z-':
            self.period *= 2
            if self.period > 16: self.period = 16
            asev('anim:redraw')

        elif event.startswith('timer:'):
            asev(event)

    def anim_fill(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        for i in range(64):
            self.ge.cube.set_animator(i, StillAnimator(self.color()))

    def anim_wipe(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        for i in range(64):
            self.ge.cube.set_animator(i, BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 0.5,
                phase_percent = 1-i/128
            ))

    def anim_chaser(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        for i in range(64):
            self.ge.cube.set_animator(i, BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 1/64,
                phase_percent = 1-i/64
            ))

    def anim_flicker(self, ev):
        if ev not in ('anim:start', 'anim:redraw', 'timer:anim_flicker'): return
        l = list(range(64))
        s = random.sample(l, 14)
        s1, s2 = s[:7], s[7:]
        p = self.period / 4
        for i in range(64):
            if i in s1:
                self.ge.cube.set_animator(i, BlinkAnimator(
                    self.color(),
                    period = p,
                    duty_cycle = 1/2,
                    phase_percent = 0
                ))
            elif i in s2:
                self.ge.cube.set_animator(i, BlinkAnimator(
                    self.color(),
                    period = p,
                    duty_cycle = 1/2,
                    phase_percent = 1/3
                ))
            else:
                self.ge.cube.set_animator(i, StillAnimator((0, 0, 0)))
        self.ge.timer_add('anim_flicker', p) # Just to be recalled periodically, do not check event value

    def helper_anim_chaserface(self, v):
        for i, j, k in itertools.product(range(4), repeat=3):
            c = coord_3d_to_linear(i, j, k)
            self.ge.cube.set_animator(c, BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 0.25,
                phase_percent = (4-(i, j, k)[v])/4
            ))

    def anim_chaserface_x(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        self.helper_anim_chaserface(0)
    def anim_chaserface_y(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        self.helper_anim_chaserface(1)
    def anim_chaserface_z(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        self.helper_anim_chaserface(2)
    def anim_chaserface_xyz(self, ev):
        if ev not in ('anim:start', 'anim:redraw', 'timer:anim_chaserface_xyz'): return
        if ev == 'anim:start': self.anim_chaserface_xyz_pos = -1
        self.anim_chaserface_xyz_pos = (self.anim_chaserface_xyz_pos + 1) % 3
        self.helper_anim_chaserface(self.anim_chaserface_xyz_pos)
        self.ge.timer_add('anim_chaserface_xyz', self.period) # Just to be recalled periodically, do not check event value

    def anim_chaser_vertical(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        for i, j, k in itertools.product(range(4), repeat=3):
            c = coord_3d_to_linear(i, j, k)
            self.ge.cube.set_animator(c, BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 1/10,
                phase_percent = 1-(i+j+k)/10
            ))

    def anim_chaser_inout(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        def o(x, y, z, phase):
            self.ge.cube.set_animator(coord_3d_to_linear(x, y, z), BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 1/5,
                phase_percent = phase/5
            ))
        for i in range(4):
            o(i, i, i, 5)
        for i in range(3):
            o(1+i, i, i, 4)
            o(i, 1+i, i, 4)
            o(i, i, 1+i, 4)
            o(i, 1+i, 1+i, 4)
            o(1+i, i, 1+i, 4)
            o(1+i, 1+i, i, 4)
        for i in range(2):
            o(i, 2+i, 1+i, 3)
            o(i, 1+i, 2+i, 3)
            o(2+i, i, 1+i, 3)
            o(1+i, i, 2+i, 3)
            o(2+i, 1+i, i, 3)
            o(1+i, 2+i, i, 3)
        for i in range(2):
            o(2+i, i, i, 2)
            o(i, 2+i, i, 2)
            o(i, i, 2+i, 2)
            o(i, 2+i, 2+i, 2)
            o(2+i, i, 2+i, 2)
            o(2+i, 2+i, i, 2)
        for i in range(4):
            o(3,i,0, 1)
            o(3,0,i, 1)
            o(i,3,0, 1)
            o(0,3,i, 1)
            o(i,0,3, 1)
            o(0,i,3, 1)

    def anim_chaser_outin(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        def o(x, y, z, phase):
            self.ge.cube.set_animator(coord_3d_to_linear(x, y, z), BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 1/5,
                phase_percent = phase/5
            ))
        for i in range(4):
            o(i, i, i, 1)
        for i in range(3):
            o(1+i, i, i, 2)
            o(i, 1+i, i, 2)
            o(i, i, 1+i, 2)
            o(i, 1+i, 1+i, 2)
            o(1+i, i, 1+i, 2)
            o(1+i, 1+i, i, 2)
        for i in range(2):
            o(i, 2+i, 1+i, 3)
            o(i, 1+i, 2+i, 3)
            o(2+i, i, 1+i, 3)
            o(1+i, i, 2+i, 3)
            o(2+i, 1+i, i, 3)
            o(1+i, 2+i, i, 3)
        for i in range(2):
            o(2+i, i, i, 4)
            o(i, 2+i, i, 4)
            o(i, i, 2+i, 4)
            o(i, 2+i, 2+i, 4)
            o(2+i, i, 2+i, 4)
            o(2+i, 2+i, i, 4)
        for i in range(4):
            o(3,i,0, 0)
            o(3,0,i, 0)
            o(i,3,0, 0)
            o(0,3,i, 0)
            o(i,0,3, 0)
            o(0,i,3, 0)

    def anim_chaseredges(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        def o(x, y, z, phase):
            self.ge.cube.set_animator(coord_3d_to_linear(x, y, z), BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 1/10,
                phase_percent = phase/10
            ))
        for i in range(64):
            self.ge.cube.set_animator(i, StillAnimator((0, 0, 0)))
        for i in range(4):
            o(i,0,0, 10-i)
            o(0,i,0, 10-i)
            o(0,0,i, 10-i)
        for i in range(2):
            o(3,i+1,0, 6-i)
            o(3,0,i+1, 6-i)
            o(i+1,3,0, 6-i)
            o(0,3,i+1, 6-i)
            o(i+1,0,3, 6-i)
            o(0,i+1,3, 6-i)
        for i in range(4):
            o(i,3,3, 4-i)
            o(3,i,3, 4-i)
            o(3,3,i, 4-i)


    def helper_anim_wipeface(self, v):
        for i, j, k in itertools.product(range(4), repeat=3):
            c = coord_3d_to_linear(i, j, k)
            self.ge.cube.set_animator(c, BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 0.5,
                phase_percent = (8-(i, j, k)[v])/8
            ))

    def anim_wipeface_x(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        self.helper_anim_wipeface(0)
    def anim_wipeface_y(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        self.helper_anim_wipeface(1)
    def anim_wipeface_z(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        self.helper_anim_wipeface(2)

    def anim_wipeface_xyz(self, ev):
        if ev not in ('anim:start', 'anim:redraw', 'timer:anim_wipeface_xyz'): return
        if ev == 'anim:start': self.anim_wipeface_xyz_pos = -1
        self.anim_wipeface_xyz_pos = (self.anim_wipeface_xyz_pos + 1) % 3
        self.helper_anim_wipeface(self.anim_wipeface_xyz_pos)
        self.ge.timer_add('anim_wipeface_xyz', self.period) # Just to be recalled periodically, do not check event value

    def anim_wipe_vertical(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        for i, j, k in itertools.product(range(4), repeat=3):
            c = coord_3d_to_linear(i, j, k)
            self.ge.cube.set_animator(c, BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 1/2,
                phase_percent = 1-(i+j+k)/20
            ))

    def anim_wipe_inout(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        def o(x, y, z, phase):
            self.ge.cube.set_animator(coord_3d_to_linear(x, y, z), BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 1/2,
                phase_percent = phase/10 + 0.5
            ))
        for i in range(4):
            o(i, i, i, 5)
        for i in range(3):
            o(1+i, i, i, 4)
            o(i, 1+i, i, 4)
            o(i, i, 1+i, 4)
            o(i, 1+i, 1+i, 4)
            o(1+i, i, 1+i, 4)
            o(1+i, 1+i, i, 4)
        for i in range(2):
            o(i, 2+i, 1+i, 3)
            o(i, 1+i, 2+i, 3)
            o(2+i, i, 1+i, 3)
            o(1+i, i, 2+i, 3)
            o(2+i, 1+i, i, 3)
            o(1+i, 2+i, i, 3)
        for i in range(2):
            o(2+i, i, i, 2)
            o(i, 2+i, i, 2)
            o(i, i, 2+i, 2)
            o(i, 2+i, 2+i, 2)
            o(2+i, i, 2+i, 2)
            o(2+i, 2+i, i, 2)
        for i in range(4):
            o(3,i,0, 1)
            o(3,0,i, 1)
            o(i,3,0, 1)
            o(0,3,i, 1)
            o(i,0,3, 1)
            o(0,i,3, 1)

    def anim_wipe_outin(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        def o(x, y, z, phase):
            self.ge.cube.set_animator(coord_3d_to_linear(x, y, z), BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 1/2,
                phase_percent = phase/10 + 0.5
            ))
        for i in range(4):
            o(i, i, i, 1)
        for i in range(3):
            o(1+i, i, i, 2)
            o(i, 1+i, i, 2)
            o(i, i, 1+i, 2)
            o(i, 1+i, 1+i, 2)
            o(1+i, i, 1+i, 2)
            o(1+i, 1+i, i, 2)
        for i in range(2):
            o(i, 2+i, 1+i, 3)
            o(i, 1+i, 2+i, 3)
            o(2+i, i, 1+i, 3)
            o(1+i, i, 2+i, 3)
            o(2+i, 1+i, i, 3)
            o(1+i, 2+i, i, 3)
        for i in range(2):
            o(2+i, i, i, 4)
            o(i, 2+i, i, 4)
            o(i, i, 2+i, 4)
            o(i, 2+i, 2+i, 4)
            o(2+i, i, 2+i, 4)
            o(2+i, 2+i, i, 4)
        for i in range(4):
            o(3,i,0, 5)
            o(3,0,i, 5)
            o(i,3,0, 5)
            o(0,3,i, 5)
            o(i,0,3, 5)
            o(0,i,3, 5)

    def anim_wipeedges(self, ev):
        if ev not in ('anim:start', 'anim:redraw'): return
        def o(x, y, z, phase):
            self.ge.cube.set_animator(coord_3d_to_linear(x, y, z), BlinkAnimator(
                self.color(),
                period = self.period,
                duty_cycle = 1/2,
                phase_percent = phase/20 + 0.5
            ))
        for i in range(64):
            self.ge.cube.set_animator(i, StillAnimator((0, 0, 0)))
        for i in range(4):
            o(i,0,0, 10-i)
            o(0,i,0, 10-i)
            o(0,0,i, 10-i)
        for i in range(2):
            o(3,i+1,0, 6-i)
            o(3,0,i+1, 6-i)
            o(i+1,3,0, 6-i)
            o(0,3,i+1, 6-i)
            o(i+1,0,3, 6-i)
            o(0,i+1,3, 6-i)
        for i in range(4):
            o(i,3,3, 4-i)
            o(3,i,3, 4-i)
            o(3,3,i, 4-i)
