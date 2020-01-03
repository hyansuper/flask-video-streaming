import cv2
import numpy as np
import urllib.request

stream = urllib.request.urlopen('http://pi-address:5000/video_feed?fps=5')
total_bytes = b''
while True:
    total_bytes += stream.read(1024)
    b = total_bytes.find(b'\xff\xd9') # JPEG end
    if not b == -1:
        a = total_bytes.find(b'\xff\xd8') # JPEG start
        jpg = total_bytes[a:b+2] # actual image
        total_bytes= total_bytes[b+2:] # other informations
        
        # decode to colored image ( another option is cv2.IMREAD_GRAYSCALE )
        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR) 
        cv2.imshow('Window name',cv2.flip(img, -1)) # display image while receiving data
        if cv2.waitKey(1) ==27: # if user hit esc            
            break
cv2.destroyWindow('Window name')
