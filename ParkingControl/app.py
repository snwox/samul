from flask import Flask,app,render_template
from flask_socketio import SocketIO, emit
from module import dbModule

from datetime import datetime as dt

import os
import time
import json

if os.getenv("env") == "Dev":
    from config import Dev as CONF
else:
    from config import Production as CONF

app=Flask(__name__)
app.config.from_object(CONF)

socketio = SocketIO(app)


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
<<<<<<< HEAD
    db=dbModule.Database()
    print(db)
    socketio.run(app,host="0.0.0.0",debug=True,port=5000)
=======
    app.run(host="0.0.0.0", debug=True)
    socketio.run(host="0.0.0.0",debug=True)
>>>>>>> d64cea45d584af3aea0c1f71e2042995f3ceb6c6
