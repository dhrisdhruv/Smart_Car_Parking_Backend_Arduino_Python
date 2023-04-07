from Arduino import Arduino

import time

trigPin = 9
echoPin = 10

duration = 0
distance = 0

board = Arduino()


def setup():
    board.pinMode(trigPin, 'OUTPUT')
    board.pinMode(echoPin, 'INPUT')


setup()

while True:
    board.digitalWrite(trigPin, 'LOW')
    time.sleep(2 / 1000000.0)
    board.digitalWrite(trigPin, 'HIGH')
    time.sleep(10 / 1000000.0)
    board.digitalWrite(trigPin, 'LOW')
    duration = board.pulseIn(echoPin, 'HIGH')
    distance = duration * 0.034 / 2
    print(distance)
    time.sleep(1)
