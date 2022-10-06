import threading
import queue

sound_lib = True
try:
    from pydub import AudioSegment
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
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self._thread_loop)
        self.thread.start()

    def play(self, n):
        if n in self.sounds and self.thread.is_alive():
            self.q.put(n)

    def stop(self):
        self.q.put(None)

    def _thread_loop(self):
        print('Sound thread: begin')
        while True:
            s = self.q.get()
            if s in self.sounds:
                play(self.sounds[s])
            self.q.task_done()
            if s is None: break
        print('Sound thread: end')
