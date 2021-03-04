import time
from absl import app, logging
import cv2
import numpy as np
import tensorflow as tf
from proctoring.yolov3 import (
    YoloV3
)

from flask import Flask, request, Response, jsonify, send_from_directory, abort, render_template
from flask_socketio import SocketIO, emit
from engineio.payload import Payload

# customize your API through the following parameters
classes_path = './data/labels/coco.names'
weights_path = './weights/yolov3.tf'


yolo = YoloV3(classes=num_classes)

# Initialize Flask application
app = Flask(__name__)
Payload.max_decode_packets = 10
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

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    boxes, scores, classes, nums = yolo(frame)

    print(boxes,scores,classes,nums)

if __name__ == "__main__":
	socketio.run(app,debug = True)