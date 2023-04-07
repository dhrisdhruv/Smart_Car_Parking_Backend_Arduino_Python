import time
import firebase_admin
from firebase_admin import db
from pymata4 import pymata4
import numpy as np
import pandas as pd
import datetime

from sklearn.linear_model import LinearRegression
from sklearn import metrics

data = pd.read_csv('duration.csv')

x = data['day'].to_numpy().reshape((-1, 1))

y = data['duration']

model = LinearRegression()

model.fit(x, y)

ypred = model.predict(x)

d = datetime.datetime.now()

wait_time = ypred[int(d.strftime("%d"))]

cred_obj = firebase_admin.credentials.Certificate('car-parking-dhruv-firebase-adminsdk-czdtf-f89a1d6825.json')

default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': "https://car-parking-dhruv-default-rtdb.firebaseio.com/"})

ref = db.reference("/slots/")
slots = ref.get();
slotState = slots["slot2"]["state"]

trigPin = 9
echoPin = 10
greenLed = 7
redLed = 6

board = pymata4.Pymata4()

oldState = False

board.set_pin_mode_digital_output(greenLed)
board.set_pin_mode_digital_output(redLed)


def the_callback(data):
    distance = data[2]
    global oldState
    global slotState
    #print(distance)
    if distance < 20:
        slotState = False
    else:
        slotState = True

    if slotState != oldState:
        if slotState == True:
            board.digital_write(greenLed, 1)
            board.digital_write(redLed, 0)
            ref.child('slot2').update({"state": slotState, "BookingDevice": ""})
        else:
            board.digital_write(greenLed, 0)
            board.digital_write(redLed, 1)
            ref.child('slot2').update({"state": slotState, "BookingDevice": "arduino"})
        print(distance)
        print(slotState)
    oldState = slotState


board.set_pin_mode_sonar(trigPin, echoPin, the_callback)

while True:
    while True:
        try:
            bookingDevice = ref.get()["slot2"]["BookingDevice"]
            st = ref.get()["slot2"]["state"]
            #print("Database reading done")
            if str(bookingDevice) == "app":
                board.digital_write(greenLed, 0)
                board.digital_write(redLed, 1)
                print("Slot booked via app")
                break
            else:
                board.sonar_read(trigPin)
                #board.digital_write(greenLed, 1)
                #board.digital_write(redLed, 0)
                #print("Slot is free")
            time.sleep(0.1)
            ref.child('slot2').update({"wt": wait_time})
        except Exception:
            board.shutdown()
            print("Board shutting down")