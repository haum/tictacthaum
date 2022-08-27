import pyglet

class SoundEffect:
    def __init__(self):
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
