from flask import Flask,app,render_template
import os
from module import dbModule
from flask_socketio import SocketIO

if os.getenv("env") == "Dev":
    from config import Dev as CONF
else:
    from config import Production as CONF

app=Flask(__name__)
app.config.from_object(CONF)

socketio = SocketIO(app)


@app.route("/")
def index():
    cars = [{'id': 1, 'idx': 1, 'number': '000테0001', 'enter_time': '2021년 귀월 찮일', 'enter_timeS': 12349900},{'id': 1, 'idx': 1, 'number': '000테0001', 'enter_time': '2021년 귀월 찮일', 'enter_timeS': 12349900},{'id': 1, 'idx': 1, 'number': '000테0001', 'enter_time': '2021년 귀월 찮일', 'enter_timeS': 12349900}]

    return render_template('index.html', cars=cars)

@socketio.on("my event")
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == "__main__":
    db=dbModule.Database()
    print(db)
    socketio.run(app,host="0.0.0.0",debug=True,port=5000)
