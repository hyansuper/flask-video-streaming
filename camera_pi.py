import io
import time
import picamera
from base_camera import BaseCamera


class Camera(BaseCamera):
    def __init__(self, w=320, h=240, fps=10, close_delay=5):
        new_config = {'w':w, 'h':h, 'fps':fps, 'close_delay':close_delay}
        if not new_config == Camera.config:
            Camera.config = new_config
            if Camera.thread:
                Camera.stop = True
                Camera.thread.join()
            
        BaseCamera.__init__(self)
        
    @classmethod
    def frames(cls):
        with picamera.PiCamera(resolution=(cls.config['w'], cls.config['h']), framerate=cls.config['fps']) as camera:
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
