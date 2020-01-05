import urllib.request
import cv2
import numpy as np

class RemotePiCamera:
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
    def read(self):
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
        self.stream.close()
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
