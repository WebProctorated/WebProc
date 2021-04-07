from flask import Flask, render_template,Response
# from flask_socketio import SocketIO, emit
# from engineio.payload import Payload
import io
import base64
from PIL import Image
import cv2
import numpy as np
import imutils
from flask_cors import cross_origin  # flask-cors
from proctoring.ProctoringEngine import Proctor
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from threading import Thread

app = Flask(__name__)
# Payload.max_decode_packets = 6
# socketio = SocketIO(async_mode='gevent', ping_timeout=PING_TIMEOUT, ping_interval=PING_INTERVAL)
# socketio = SocketIO(app, cors_allowed_origins="*")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['LIP_DIST_MEASURE_DONE'] = False
app.config['USER_ORIENT_CALIBRATION_DONE'] = False
app.config['START_TEST'] = False # temporary solution as db not available for now
app.config['SCHEDULAR_STARTED'] = False
app.config['START_PROCTORING'] = False
app.config['TEST_DONE'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

proctor = Proctor()
scheduler = BackgroundScheduler()
scheduler.start()

# global variables
stop_thread = False             # controls thread execution
frame = None                      # stores the image retrieved by the camera


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    print('accessing')
    return render_template('index.html')

def stream(camera):
    global frame
    while True:
        #get camera frame
        # time.sleep(0.03) #30fps
        frame = camera.get_frame()
        ret, jpeg = cv2.imencode('.jpg', frame)
        stream_frame = jpeg.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + stream_frame + b'\r\n\r\n')

# @socketio.on('image')
@app.route('/video-stream')
@cross_origin()
def video_feed():
    global frame, stop_thread
     # start the capture thread: reads frames from the camera (non-stop) and stores the result in img
    t = Thread(target=gen, args=(proctor,), daemon=True) # a deamon thread is killed when the application exits
    t.start()
    return Response(stream(proctor),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
def gen(camera):
    global frame, stop_thread
    while True:
        if frame is None:
            #get camera frame
            frame = camera.get_frame()

        if proctor.STATE == 'CHECK_ROOM_INTENSITY':
            print('checking room intensity')
            # check is sitting in proper lighting or not
            if proctor.check_for_room_light_intensity(frame) == True:
                print('frame intensity good')
                # make a url instead which will listen to user button click on Proceed and start the test
                proctor.STATE = 'MEASURE_LIP_DIST'
                # also set some flag in database which will tell that user is already passed this check
                # emit('goodToGo', 'Perfect!!')
            else:
                print('frame intensity bad')
                # emit('error', 'Improve Room Light!!')

        # calibrate user lip distance
        if proctor.STATE == 'MEASURE_LIP_DIST':
            print('measuring lip distance')
            proctor.calibrate_user_lip_distance(frame)
            proctor.STATE = 'CALIBRATE_USER_ORIENT'

        # caliberating user orientaion
        if proctor.STATE == 'CALIBRATE_USER_ORIENT':
            scheduler.add_job(func=set_user_orient_calibration_done, trigger='date', run_date=datetime.now()+timedelta(seconds=10), args=[])
            app.config['SCHEDULAR_STARTED'] = True
            proctor.calibrating_user_orientation(frame)
            proctor.STATE = 'CALIBRATE_USER_ORIENT_INPROCESS'
        
        if proctor.STATE == 'CALIBRATE_USER_ORIENT_INPROCESS':
            proctor.calibrating_user_orientation(frame)

        if proctor.STATE == 'CALIBRATE_USER_ORIENT_DONE':
            if proctor.check_calibrated_user_orient() == True:
                proctor.STATE = 'START_TEST'
            else:
                proctor.STATE = 'CALIBRATE_USER_ORIENT'
                print('Calibration Can\'t be done properly, sit straight next time')

        if proctor.STATE == 'START_TEST':
            proctor.reset_plot_values()  # to clear the values accumulated while calibrations
            scheduler.add_job(func=set_start_test, trigger='date', run_date=datetime.now()+timedelta(minutes=1),args=[])
            proctor.predict(frame)
            proctor.STATE = 'TEST_INPROCESS'
        
        if proctor.STATE == 'TEST_INPROCESS':
            proctor.predict(frame)

        if proctor.STATE == 'TEST_DONE':
            proctor.draw_graph()
            proctor.STATE == 'TERMINATE'
            print('Test Done!!')
            return 
        # emit('goodToGo', 'Test Done!!')

def set_user_orient_calibration_done():
    print('inside thread1: ',datetime.now())
    proctor.STATE = 'CALIBRATE_USER_ORIENT_DONE'
    # scheduler.shutdown()


def set_start_test():
    print('inside thread2: ',datetime.now())
    proctor.STATE = 'TEST_DONE'
    # scheduler.shutdown()


if __name__ == "__main__":
    app.run(debug=True)
