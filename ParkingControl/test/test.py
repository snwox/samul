import RPi.GPIO as GPIO
import time

trig=4
echo=14
GPIO.setmode(GPIO.BCM)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
try:
    while True:
        GPIO.output(trig,1)
        time.sleep(0.00001)
        GPIO.output(trig,0)
        while GPIO.input(echo)==0:
            pass
        start=time.time()
        while GPIO.input(echo)==1:
            pass
        stop=time.time()
        dur=stop-start
        dis=dur*17160
        print('%.1f'%dis)
        time.sleep(0.1)
finally:
    GPIO.cleanup()
    print("exit")
