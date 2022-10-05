sound_lib = True
try:
    from pydub import AudioSegment
except ModuleNotFoundError:
    sound_lib = False
try:
    from pydub.playback import play
except ModuleNotFoundError:
    sound_lib = False

class SoundEffect:
    def __init__(self, disable = False):
        if not sound_lib or disable:
            self.sounds = {}
            print('Sound inactive:', 'disabled' if disable else 'sound lib not found')
            return
        else:
            print('Sound active')
        self.sounds = {
            'ping': AudioSegment.from_ogg('ping.ogg'),
            'ping2': AudioSegment.from_ogg('ping2.ogg'),
            'end': AudioSegment.from_ogg('end.ogg'),
        }

    def play(self, n):
        if n in self.sounds:
            self.sounds[n].play()
