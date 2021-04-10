from flask import Flask, render_template,Response,request,session
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
import sqlite3

app = Flask(__name__)
# Payload.max_decode_packets = 6
# socketio = SocketIO(async_mode='gevent', ping_timeout=PING_TIMEOUT, ping_interval=PING_INTERVAL)
# socketio = SocketIO(app, cors_allowed_origins="*")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

proctor = Proctor()
scheduler = BackgroundScheduler()
scheduler.start()

@app.route('/login',methods=['POST'])
@cross_origin()
def login():
    enrollment = request.json['enrollment']
    testId = request.json['testId']
    with sqlite3.connect("student.db") as con:
        cur = con.cursor()
        statement = f"SELECT enrollment_number from Student WHERE enrollment_number='{enrollment}' AND Password = '{testId}';"
        cur.execute(statement)
        if not cur.fetchone():  # An empty result evaluates to False.
            print("Login failed")
            return jsonify({'error':'Wrong Credentials'}), 401  #unauthorize
        else:
            session['enrollment'] = enrollment
            return Response(), 201 #success
    return Response(), 400 # server error

@app.route('/calibration',methods=['POST'])
@cross_origin()
def calibration():
    global frame, stop_thread, msg
     # start the capture thread: reads frames from the camera (non-stop) and stores the result in img
    t = Thread(target=checks, args=(proctor,), daemon=True) # a deamon thread is killed when the application exits
    t.start()
    if len(msg) == 0:
        return Response(stream(proctor),status=201,
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        error = msg
        msg = []
        return Response(statusText=error[0],status=404)

def checks(camera):
    global frame, stop_thread, msg, proctor
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
                msg.append('Increase Room Light')
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
                msg.append('Calibration Can\'t be done properly, sit straight next time')
                print('Calibration Can\'t be done properly, sit straight next time')

def stream(camera):
    global frame, proctor
    while True:
        #get camera frame
        # time.sleep(0.03) #30fps
        if proctor.STATE == 'START_TEST':
            return
        else:
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
    con = sqlite3.connect("student.db")  
    print("Database opened successfully")  
    con.execute("DROP TABLE Student")
    con.execute("DROP TABLE Questions")
    con.execute("DROP TABLE Result")
    con.execute("create table Student (enrollment_number VARCHAR[12] PRIMARY KEY , first_name TEXT NOT NULL, last_name TEXT NOT NULL, password VARCHAR[30] NOT NULL)")  
    con.execute("create table Questions (question_id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, a TEXT NOT NULL, b TEXT NOT NULL, c TEXT NOT NULL, d TEXT NOT NULL, answer TEXT NOT NULL)") 
    con.execute("create table Result (enrollment_number VARCHAR[12] PRIMARY KEY , marks INTEGER NOT NULL) ")
    print("Table created successfully")  

    cur = con.cursor()  
    cur.execute("INSERT OR IGNORE into Student (enrollment_number,first_name, last_name, password) values (?,?,?,?)",('student_123','first_name','last_name','test_123'))  
    con.commit()
    msg = "Employee successfully Added" 
    
    con.close()  
    app.run(debug=True)
