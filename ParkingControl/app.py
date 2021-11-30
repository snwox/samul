from flask import Flask,app,render_template
from flask_socketio import SocketIO
from module import dbModule, licensePlate
from datetime import datetime as dt

import os
import time
import json
import threading

trig_pin=4
echo_pin=14
led_pin=21

# 번호판 구하기  = licensePlate.detect(cv2로 찍은 이미지 파일)   : 리턴값 = 번호판

try:
    import RPi.GPIO as GPIO
    from lcd import drivers

    display = drivers.Lcd()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_pin,GPIO.OUT)
    GPIO.setup(echo_pin,GPIO.IN)
    GPIO.setup(led_pin,GPIO.OUT)

except:
    pass

if os.getenv("env") == "Dev":
    from config import Dev as CONF
else:
    from config import Production as CONF

db=dbModule.Database()

app=Flask(__name__)
app.config.from_object(CONF)

socketio = SocketIO(app, cors_allowed_origins='*')

def go_out():
    try:
        for i in range(10):
            GPIO.output(trig_pin,True)
            time.sleep(0.00001)
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
                #picture and capture car
                car_num=''

                #database 조회 후 소켓 보내기
                GPIO.output(led_pin,1)
                display.lcd_display(car_num,1)
                pass
    # finally:
        GPIO.cleanup()
        display.lcd_clear()
        print("clean up and exit")
    except:
        pass
    

@app.route("/")
def index():
    cars = db.executeAll('SELECT * FROM status')

    return render_template('index.html', cars=cars)

@socketio.on('eo')
def carEnterOut(data):
    print(data)
    car = db.executeOne('SELECT * FROM status WHERE number=%s', (data))
    if not car:
        now = dt.now()
        now_stamp = int(json.dumps(time.mktime(now.timetuple())*1000).split(".")[0])
        enterTime = now.strftime('%Y년 %m월 %d일  %H:%M:%S')
        uid = db.executeOne('SELECT Auto_increment FROM information_schema.tables WHERE table_schema="carmanager" AND table_name="status"')
        db.execute('INSERT INTO status (number, enter_time, enter_timeS) VALUES (%s,%s,%s)', (data, enterTime, now_stamp))
        db.commit()
        socketio.emit('enter', {'data': {
            "id": uid['Auto_increment'],
            "number": data,
            "enter_time": enterTime,
            "enter_timeS": now_stamp
        }})
    else:
        socketio.emit('out', {"id": car['id']})

@socketio.on('out')
def carOut(data):
    try:
        db.execute('DELETE FROM status WHERE id=%s', (data['id']))
        db.commit()
    except:
        socketio.emit('err', {"msg": '제거 에러'})

if __name__ == "__main__":
    t=threading.Thread(target=go_out)
    t.daemon=True
    t.start()
    socketio.run(app,host="0.0.0.0",debug=True)
