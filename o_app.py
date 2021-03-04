from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from proctoring.phone_detection import phone_detection
from engineio.payload import Payload
import io
import base64
from PIL import Image
import cv2
import numpy as np
import imutils

app = Flask(__name__)
Payload.max_decode_packets = 10
# socketio = SocketIO(async_mode='gevent', ping_timeout=PING_TIMEOUT, ping_interval=PING_INTERVAL)
socketio = SocketIO(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@socketio.on('image')
def image(data_image):
    sbuf = io.StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    print('app: {}'.format(pimg.size))
    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    if phone_detection(frame) == True:
        print("inside true")
        # emit('error','You are using smartphone')

    # Process the image frame
    # frame = imutils.resize(frame, width=700)
    # frame = cv2.flip(frame, 1)
    # imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    # stringData = base64.b64encode(imgencode).decode('utf-8')
    # b64_src = 'data:image/jpg;base64,'
    # stringData = b64_src + stringData

    # emit the frame back
    # emit('response_back', stringData)

if __name__ == "__main__":
	socketio.run(app,debug = True)
