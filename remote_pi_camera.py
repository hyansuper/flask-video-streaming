import urllib.request
import cv2
import numpy as np

class RemotePiCamera:
    def __init__(self, url):
        self.stream = urllib.request.urlopen(url)
        self.total_bytes = b''
    def read(self):
        while True:         
            self.total_bytes += self.stream.read(1024)
            end = self.total_bytes.find(b'\xff\xd9') # JPEG end
            if not end == -1:
                start = self.total_bytes.find(b'\xff\xd8') # JPEG start
                jpg = self.total_bytes[start: end+2]
                self.total_bytes = self.total_bytes[end+2:]
                return cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR) 
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
