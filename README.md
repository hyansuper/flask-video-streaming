# PiCamera Video Streaming
This is derived from [flask-video-streaming](https://github.com/miguelgrinberg/flask-video-streaming) by @miguelgrinberg.

I made some changes to support dynamic PiCamera configuration and simple API for stream receiving:
1. run app.py on raspberry pi
2. visit http://pi-address:5000 to view video stream, you can also specify resolution/framerate/hflip/vflip in the url, eg. http://pi-address:5000/?w=640&h=480&fps=10&hf=1&vf=1
3. to receive video stream from another computer, run receive.py or use:
* `RemotePiCamera(pi_address, resolution=(320,240), framerate=10, hflip=False, vflip=False)`
* `ThreadedRemotePiCamera(pi_address, resolution=(320,240), framerate=10, hflip=False, vflip=False)`
```python
from remote_pi_camera import RemotePiCamera
import cv2
for frame in RemotePiCamera(pi_address):
    cv2.imshow('picam', frame)
    if cv2.waitKey(1) ==27: # if user hit esc
        break
cv2.destroyAllWindows()
```
The threaded version has a background thread to receive video stream, which behaves more similar to `cv2.VideoCapture`, but is not thread-safe.

## Ref
* https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/3
* https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited
* https://github.com/miguelgrinberg/flask-video-streaming
