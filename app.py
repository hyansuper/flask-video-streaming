#!/usr/bin/env python
from flask import Flask, render_template, Response, request
from camera_pi import Camera
from subprocess import check_call

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    w = request.args.get('w',320,int)
    h = request.args.get('h',240,int)
    fps = request.args.get('fps',10,int)
    delay = request.args.get('delay',5,int)
    vf = -1 if request.args.get('vf',False,bool) else 1
    hf = -1 if request.args.get('hf',False,bool) else 1
    return render_template('index.html', w=w, h=h, fps=fps, delay=delay, hf=hf, vf=vf)


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    w = request.args.get('w',320,int)
    h = request.args.get('h',240,int)
    fps = request.args.get('fps',10,int)
    delay = request.args.get('delay',5,int)
    return Response(gen(Camera(w,h,fps,delay)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reboot')
def reboot():
    check_call(['sudo', 'reboot'])
    
@app.route('/poweroff')
def poweroff():
    check_call(['sudo', 'poweroff'])
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
