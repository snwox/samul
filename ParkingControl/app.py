from flask import Flask,app,render_template
from flask_socketio import SocketIO, emit
from module import dbModule
from datetime import datetime as dt

import os
import time
import json
import threading

trig_pin=4
echo_pin=14

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_pin,GPIO.OUT)
    GPIO.setup(echo_pin,GPIO.IN)

except:
    pass

if os.getenv("env") == "Dev":
    from config import Dev as CONF
else:
    from config import Production as CONF

app=Flask(__name__)
app.config.from_object(CONF)

socketio = SocketIO(app)

def go_out():
    try:
        for i in range(10):
            GPIO.output(trig_pin,True)
            time.sleep(0x00001)
            GPIO.output(trig_pin,False)

            while GPIO.input(echo_pin)==0:
                pass
            start=time.time()
            while GPIO.input(echo_pin)==1:
                pass
            stop=time.time()
            duration_time=stop-start
            distance=duration_time * 17160
            print('distance : %.1f',distance)
            if distance > 100:
                
    finally:
        GPIO.cleanup()
        print("clean up and exit")
    

@app.route("/")
def index():
    cars = [{'id': 1, 'number': '000테0001', 'enter_time': '2021년 귀월 찮일', 'enter_timeS': 12349900}]

    return render_template('index.html', cars=cars)

@socketio.on('eo')
def carEnterOut(data):
    car = db.executeOne('SELECT * FROM status WHERE number=?', (data.number))
    if not car:
        now = dt.now()
        now_stamp = int(json.dumps(time.mktime(now.timetuple())*1000).split(".")[0])
        enterTime = now.strftime('%Y년 %m월 %d일  %H:%M:%S')
        uid = db.executeOne('SELECT Auto_increment FROM information_schema.tables WHERE table_schema=`carmanager` AND table_name=`status`')
        db.execute('INSERT INTO status (number, enter_time, enter_timeS) VALUES (?,?,?)', (data.number, enterTime, now_stamp))
        emit('enter', {data: {
            "id": uid,
            "number": data.number,
            "enter_time": enterTime,
            "enter_timeS": now_stamp
        }})
    else:
        emit('out', {"id": car.id})

@socketio.on('out')
def carOut(data):
    try:
        db.execute('DELETE FROM status WHERE id=?', (data.id))
    except:
        emit('err', {"msg": '제거 에러'})

if __name__ == "__main__":
    t=threading.Thread(target=go_out)
    t.daemon=True
    t.start()
    socketio.run(app,host="0.0.0.0",debug=True)
