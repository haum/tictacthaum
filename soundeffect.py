try:
    import pyglet
except ModuleNotFoundError:
    pyglet = False

class SoundEffect:
    def __init__(self, disable = False):
        if not pyglet or disable:
            self.sounds = {}
            print('Sound inactive:', 'disabled' if disable else 'pyglet not found')
            return
        else:
            print('Sound active')
        pyglet.resource.path = ['./']
        pyglet.resource.reindex()
        self.sounds = {
            'ping': pyglet.resource.media('ping.ogg', streaming=False),
            'ping2': pyglet.resource.media('ping2.ogg', streaming=False),
            'end': pyglet.resource.media('end.ogg', streaming=False),
        }

    def play(self, n):
        if n in self.sounds:
            self.sounds[n].play()
