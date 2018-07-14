from flask import Flask
from statistics import median
import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

app = Flask(__name__)

@app.route('/')
def index():
    return str(getAverageDistance())

def getAverageDistance():
    
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)

    #measure distance 8 times
    distances = []
    for i in range(0, 9):
        distances.append(getDistance())

    #take median distance
    averageDistance = median(distances)

    GPIO.cleanup()

    return averageDistance

def getDistance():

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

    return distance

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
