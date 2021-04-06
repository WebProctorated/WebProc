from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from engineio.payload import Payload
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

app = Flask(__name__)
Payload.max_decode_packets = 6
# socketio = SocketIO(async_mode='gevent', ping_timeout=PING_TIMEOUT, ping_interval=PING_INTERVAL)
socketio = SocketIO(app, cors_allowed_origins="*")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['LIP_DIST_MEASURE_DONE'] = False
app.config['USER_ORIENT_CALIBRATION_DONE'] = False
app.config['START_TEST'] = False
# temporary solution as db not available for now
app.config['SCHEDULAR_STARTED'] = False
app.config['START_PROCTORING'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

proctor = Proctor()
scheduler = BackgroundScheduler()


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    print('accessing')
    return render_template('index.html')


@socketio.on('image')
def image(data_image):
    sbuf = io.StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    print('app: {}'.format(pimg.size))
    # converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    if app.config['START_PROCTORING'] == False:
        print('inside proctoring false')
        # check is sitting in proper lighting or not
        if proctor.check_for_room_light_intensity(frame) == True:
            print('frame intensity good')
            # make a url instead which will listen to user button click on Proceed and start the test
            app.config['START_PROCTORING'] = True
            # also set some flag in database which will tell that user is already passed this check
            emit('goodToGo', 'Perfect!!')
        else:
            print('frame intensity bad')
            emit('error', 'Improve Room Light!!')
    else:
        print('inside proctoring false')
        # calibrate user lip distance
        if app.config['LIP_DIST_MEASURE_DONE'] == False:
            print('lip distance measure false')
            proctor.calibrate_user_lip_distance(frame)
            app.config['LIP_DIST_MEASURE_DONE'] = True

        if app.config['LIP_DIST_MEASURE_DONE'] == True:
            print('lip distance measure true')
            # caliberating user orientaion
            if app.config['USER_ORIENT_CALIBRATION_DONE'] == False:
                if app.config['SCHEDULAR_STARTED'] == False:
                    scheduler.add_job(func=set_user_orient_calibration_done(
                        True), trigger="interval", seconds=15)
                    scheduler.start()
                    app.config['SCHEDULAR_STARTED'] = True

                proctor.calibrating_user_orientation(frame)
            else:
                if proctor.check_calibrated_user_orient() == True:
                    app.config['START_TEST'] = True
                    emit('goodToGo', 'Perfect!!')
                else:
                    # on user button click re calibration should start
                    emit(
                        'error', 'Calibration Can\'t be done properly, sit straight next time')

            if app.config['START_TEST'] == True:
                if app.config['SCHEDULAR_STARTED'] == False:
                    proctor.reset_plot_values()  # to clear the values accumulated while calibrations
                    scheduler.add_job(func=set_start_test(
                        False), trigger='interval', seconds=15*60)
                    scheduler.start()
                    app.config['SCHEDULAR_STARTED'] = True
                proctor.predict(frame)
            else:
                proctor.draw_graph()
                app.config['LIP_DIST_MEASURE_DONE'] = False
                app.config['START_PROCTORING'] = False
                print('Test Done!!')
                emit('goodToGo', 'Test Done!!')

    # if phone_detection(frame) == True:
    #     print("inside true")
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


def set_user_orient_calibration_done(value):
    app.config['USER_ORIENT_CALIBRATION_DONE'] = value
    app.config['SCHEDULAR_STARTED'] = False
    scheduler.shutdown()


def set_start_test(value):
    app.config['START_TEST'] = value
    app.config['SCHEDULAR_STARTED'] = False
    scheduler.shutdown()


if __name__ == "__main__":
    socketio.run(app, debug=True)
