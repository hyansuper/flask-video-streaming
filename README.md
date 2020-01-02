# Picamera Video Streaming
This is derived from [flask-video-streaming](https://github.com/miguelgrinberg/flask-video-streaming) by @miguelgrinberg.

I made some changes to support dynamic PiCamera configuration:
* run app.py on raspberry pi
* visit pi-address:5000 to view video stream, you can specify width/height/framerate/hflip/vflip in the url, eg. pi-address:5000/?w=640&h=480&fps=10&hf=1&vf=1
* run receive.py on another computer to read video stream with cv2

## Ref:
* https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/3
* https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited
* https://github.com/miguelgrinberg/flask-video-streaming
