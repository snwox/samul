from flask import Flask
import RPi.GPIO as GPIO
app=Flask(__name__)
leds={"red":22,"blue":23}
ops={"on":1,"off":0}
@app.route("/")
def index():    
    return """
    <h1>Hello, Flask</h1>
    <a href="/led/red/on">RED LED ON</a>
    <a href="/led/red/off">RED LED OFF</a>
    <a href="/led/blue/on">BLUE LED ON</a>
    <a href="/led/blue/off">BLUE LED OFF</a>
    """

@app.route("/led/<color>/<op>")
def onoff(color,op):
    print(color)
    print(op)
    global leds
    global ops
    GPIO.output(leds[color],ops[op])
    return f"<p>{color.upper()} LED {op.upper()}</p><a href="/">Go Home</a>"
    
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0")
    finally:
        GPIO.cleanup()