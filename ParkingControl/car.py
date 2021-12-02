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

try:   
    display = drivers.Lcd()             #gpio 를 세팅한다.
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(trig_pin,GPIO.OUT)
    GPIO.setup(echo_pin,GPIO.IN)
    GPIO.setup(led_pin,GPIO.OUT)
    cap=cv2.VideoCapture('/dev/video0')

    if not cap.isOpened():
        print("camera error")
        exit()
    time.sleep(1)
    while True:
        GPIO.output(trig_pin,True)              # 초음파 모듈로 거리 측정
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
        print('distance : %.1f'%distance)
        ret,frame=cap.read()
        if not ret:
            break
        cv2.imshow("frame",frame)
        if cv2.waitKey(10)==27:
            cv2.imwrite('output.jpg',frame)
            break
        if distance<=35:                    # 35센치 이내로 들어올 때
                                            # licensePlate 모듈의 detect 함수를 카메라에 찍힌 번호판사진을 인자로 호출
            GPIO.output(led_pin,1)
            try:
                car_num=licensePlate.detect(frame)
                if car_num[0]!=0:                           #차량번호가 정상적일 때 (숫자로 시작하고 숫자로 끝남) lcd 에 출력한다.
                    display.lcd_display_string(car_num[1],1)
                    print(f"----------------------\n{car_num[1]}\n--------------------")
                    time.sleep(3)
                else:
                    print(f"!!!!! nop : {car_num[1]} !!!!!")
                
            except:
                pass
            GPIO.output(led_pin,1)
        else:
            GPIO.output(led_pin,0)
        time.sleep(0.1)
finally:                        # 사용한 자원을 반환한다.
    GPIO.output(led_pin,0)
    cv2.destroyAllWindows()
    GPIO.cleanup()
    display.lcd_clear()
    print("clean up and exit")
