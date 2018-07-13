from flask import Flask
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

@app.route('/')
def index():
    return str(getDistance())

def getDistance():
    
    GPIO.setmode(GPIO.BCM)
    
    TRIG = 23
    ECHO = 24

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)

    #time delay to settle sensor
    time.sleep(0.5)

    #send trigger pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    #store last low timestamp
    while GPIO.input(ECHO) == 0:
        pulseStart = time.time()

    #store last high timestamp
    while GPIO.input(ECHO) == 1:
        pulseEnd = time.time()

    #calculate duration of high signal
    pulseDuration = pulseEnd - pulseStart

    #calculate distance using the speed of sound at 343m/s
    distance = pulseDuration * 17150
    distance = round(distance, 2)

    GPIO.cleanup()

    return distance

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
