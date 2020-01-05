# PiCamera Video Streaming
This is derived from [flask-video-streaming](https://github.com/miguelgrinberg/flask-video-streaming) by @miguelgrinberg.

I made some changes to support dynamic PiCamera configuration and provide API for stream receiving:
* run app.py on raspberry pi
* visit http://pi-address:5000 to view video stream, you can also specify width/height/framerate/horizontal_flip/vertical_flip in the url, eg. http://pi-address:5000/?w=640&h=480&fps=10&hf=1&vf=1
* to receive video stream from another computer, run receive.py or:
```python
from remote_pi_camera import RemotePiCamera
import cv2
for frame in RemotePiCamera(pi-address, resolution=(320,240), framerate=10):
    cv2.imshow('picam', cv2.flip(frame,-1))
    if cv2.waitKey(1) ==27: # if user hit esc
        break
cv2.destroyAllWindows()
```

## Ref
* https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/3
* https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited
* https://github.com/miguelgrinberg/flask-video-streaming
