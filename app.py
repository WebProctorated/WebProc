from flask import Flask, render_template,Response,request,session, Response
from flask_socketio import SocketIO, emit, disconnect
from engineio.payload import Payload
from io import StringIO
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
import sys

app = Flask(__name__)

Payload.max_decode_packets = 500
socketio = SocketIO(app, cors_allowed_origins="*")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

proctor = Proctor()
scheduler = BackgroundScheduler()
scheduler.start()

@app.route('/cheat',methods=['POST'])
@cross_origin()
def cheat():
    if proctor.STATE == TEST_INPROCESS:
        proctor.CHEAT = True
        proctor.TAB_CHANGE = True
    return Response(status=201)

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

flag = False
frame_q = []
msg_q = []

def proctor_task():
    global flag, frame_q, msg_q, proctor

    while flag == True:
        if len(frame_q) == 0:
            continue
        print(proctor.STATE)
        frame = frame_q.pop(0)
        try:
            if proctor.STATE == 'START_TEST':
                proctor.STATE = 'TEST_INPROCESS'
                proctor.reset_plot_values()  # to clear the values accumulated while calibrations
                scheduler.add_job(func=set_start_test, trigger='date', run_date=datetime.now()+timedelta(minutes=1),args=[])
                proctor.predict(frame)
            
            if proctor.STATE == 'TEST_INPROCESS':
                proctor.predict(frame)
        except Exception as e:
            emit('msg',{'error':True,'msg':'Cheating Detected'})

        if proctor.STATE == 'TEST_DONE':
            proctor.save_graph()
            proctor.STATE == 'TERMINATE'
            print('Test Done!!')
            return 

def calibration_task():
    global flag, frame_q, msg_q, proctor
    while flag == True:
        # time.sleep(0.2)
        if len(frame_q) == 0:
            continue
        frame = frame_q.pop(0)
        print(proctor.STATE)
        if proctor.STATE == 'CHECK_ROOM_INTENSITY':
            print('checking room intensity')
            # check is sitting in proper lighting or not
            if proctor.check_for_room_light_intensity(frame) == True:
                print('frame intensity good')
                proctor.STATE = 'MEASURE_LIP_DIST'
                msg_q.append({'error':False,'msg':'Room Light Fine!!'})

            else:
                print('frame intensity bad')
                msg_q.append({'error':True,'msg':'Improve Room Light!!'})
                flag = False

        # calibrate user lip distance
        if proctor.STATE == 'MEASURE_LIP_DIST':
            print('measuring lip distance')
            proctor.calibrate_user_lip_distance(frame)
            proctor.STATE = 'CALIBRATE_USER_ORIENT'
        try:
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
                    msg_q.append({'error':True,'msg':'All Is Fine!! Good to Go!'})
                    return
                    # emit('msg', {'error':False,'msg':'All Is Fine!! Good to Go!'})
                else:
                    proctor.STATE = 'CALIBRATE_USER_ORIENT'
                    msg_q.append({'error':True,'msg':'Calibration Can\'t be done properly, sit straight next time'})
                    flag = False
                    # emit('msg', {'error':True,'msg':'Calibration Can\'t be done properly, sit straight next time'})
                    print('Calibration Can\'t be done properly, sit straight next time')
                    return
                    # disconnect() # ends socket con
        except Exception as e:
            proctor.STATE = 'CALIBRATE_USER_ORIENT'
            msg_q.append({'error':True,'msg':'Calibration Can\'t be done properly, sit straight next time'})
            return

    return 


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")

start_calibration = False
start_proctoring = False

@socketio.on('calibrate', namespace='/test')
def calibration(data_image):
    global frame_q,msg_q,start_calibration,flag

    if start_calibration == False:
        start_calibration = True
        flag = True
        t = Thread(target=calibration_task, daemon=True) # a deamon thread is killed when the application exits
        t.start()

    data_image = data_image.split(",")[1]
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    frame_q.append(frame)

    if len(msg_q) != 0:
        m = msg_q.pop(0)
        emit('msg',m)
        if m['error'] == True:
            start_calibration = False
            disconnect()


    emit('out-image-event','heartbeat msg')

@socketio.on('proctor', namespace='/test')
def calibration(data_image):
    global frame_q,msg_q,start_proctoring,flag

    if start_proctoring == False:
        start_proctoring = True
        flag = True
        t = Thread(target=proctor_task, daemon=True) # a deamon thread is killed when the application exits
        t.start()

    data_image = data_image.split(",")[1]
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    frame_q.append(frame)

    if proctor.CHEAT == True:
        proctor.CHEAT = False
        emit('msg',{'error':True,'msg':'Cheating Detected'})

    emit('out-image-event','heartbeat msg')

def set_user_orient_calibration_done():
    print('inside thread1: ',datetime.now())
    proctor.STATE = 'CALIBRATE_USER_ORIENT_DONE'
    # scheduler.shutdown()


def set_start_test():
    print('inside thread2: ',datetime.now())
    proctor.STATE = 'TEST_DONE'
    # scheduler.shutdown()


if __name__ == "__main__":
    # con = sqlite3.connect("student.db")  
    # print("Database opened successfully")  
    # # con.execute("DROP TABLE Student")
    # # con.execute("DROP TABLE Questions")
    # # con.execute("DROP TABLE Result")
    # con.execute("create table Student (enrollment_number VARCHAR[12] PRIMARY KEY , first_name TEXT NOT NULL, last_name TEXT NOT NULL, password VARCHAR[30] NOT NULL)")  
    # con.execute("create table Questions (question_id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, a TEXT NOT NULL, b TEXT NOT NULL, c TEXT NOT NULL, d TEXT NOT NULL, answer TEXT NOT NULL)") 
    # con.execute("create table Result (enrollment_number VARCHAR[12] PRIMARY KEY , marks INTEGER NOT NULL) ")
    # print("Table created successfully")  

    # cur = con.cursor()  
    # cur.execute("INSERT OR IGNORE into Student (enrollment_number,first_name, last_name, password) values (?,?,?,?)",('student_123','first_name','last_name','test_123'))  
    # con.commit()
    # msg = "Employee successfully Added" 
    
    # con.close()  
    socketio.run(app,debug = True)
