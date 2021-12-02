from flask import Flask,app,render_template
from flask_socketio import SocketIO
from module import dbModule, licensePlate
from datetime import datetime as dt
from lcd import drivers

import RPi.GPIO as GPIO
import cv2
import os
import time
import json
import threading

trig_pin=4
echo_pin=14
led_pin=21

# 번호판 구하기  = licensePlate.detect(cv2로 찍은 이미지 파일)   : 리턴값 = 번호판



if os.getenv("env") == "Dev":
    from config import Dev as CONF
else:
    from config import Production as CONF

db=dbModule.Database()    

app=Flask(__name__)
app.config.from_object(CONF)

socketio = SocketIO(app, cors_allowed_origins='*')

@app.route("/")
def index():                # database 에 차량목록 가져와서 메인페이지에 추력
    cars = db.executeAll('SELECT * FROM status')

    return render_template('index.html', cars=cars)

@socketio.on('eo')          # licensePlate 모듈에서 차량번호를 소켓으로 보낼 때 
                            # 신규차량이면 차의 id, 차번호, 입장시간, 현재시간을 내보내고, 이미 있는 차량이면, out 을 내보낸다.
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

@socketio.on('out')     # 소켓으로 out 을 내보냈을 때 database 에서 삭제한다.
def carOut(data):
    try:
        db.execute('DELETE FROM status WHERE id=%s', (data['id']))
        db.commit()
    except:
        socketio.emit('err', {"msg": '제거 에러'})

if __name__ == "__main__":
    print("hello")
    socketio.run(app,host="0.0.0.0",debug=True)
