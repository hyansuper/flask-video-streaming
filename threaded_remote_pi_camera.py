import urllib.request
import cv2
import numpy as np
import time
import threading

class ThreadedRemotePiCamera:
    def __init__(self, pi_address, resolution=(320,240), framerate=10, hflip=False, vflip=False):
        if hflip and vflip:
            self.flip = -1
        elif hflip:
            self.flip = 0
        elif vflip:
            self.flip = 1
        else:
            self.flip = None
        self.stream = urllib.request.urlopen('http://%s:5000/video_feed?w=%d&h=%d&fps=%d' % ((pi_address,)+resolution+(framerate,)))
        self.total_bytes = b''
        
        self.th = threading.Thread(target=self.run, daemon=True)
        self.running = True        
        self.frame = None
        self.th.start()
    def run(self):
        while self.running:
            self.frame = self.get_frame()
        self.stream.close()
    def read(self):
        while self.frame is None:
            time.sleep(.1)
        f = self.frame
        self.frame = None
        return f
    def get_frame(self):
        while True:         
            self.total_bytes += self.stream.read(1024)
            end = self.total_bytes.find(b'\xff\xd9') # JPEG end
            if not end == -1:
                start = self.total_bytes.find(b'\xff\xd8') # JPEG start
                jpg = cv2.imdecode(np.fromstring(self.total_bytes[start: end+2], dtype=np.uint8), cv2.IMREAD_COLOR)
                if self.flip is not None:
                    jpg = cv2.flip(jpg, self.flip)
                self.total_bytes = self.total_bytes[end+2:]
                return jpg
    def release(self):
        self.running = False
        self.th.join()
    def frames(self):
        while True:
            yield self.read()
    def __iter__(self):
        return self.frames()
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.release()
    def __del__(self):
        self.release()
