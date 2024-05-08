import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattedancerealtime-b05cf-default-rtdb.firebaseio.com/"
})


ref = db.reference('Students')

data = {
    "393112":
        {
            "name":"Chandan",
            "major":"CSE",
            "starting_year":2020,
            "total_attendance":10,
            "standing":"G",
            "year":4,
            "last_attendance_time":"2024-05-04 11:10:11"
        },
    "852741":
        {
            "name":"Emily Blunt",
            "major":"ECE",
            "starting_year":2019,
            "total_attendance":6,
            "standing":"O",
            "year":3,
            "last_attendance_time":"2023-04-06 10:34:11"
        },
    "963852":
        {

            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "112233":
        {
            "name":"Avinash",
            "major":"DMLT",
            "starting_year":2022,
            "total_attendance":5,
            "standing":"G",
            "year":3,
            "last_attendance_time":"2023-02-16 19:10:11"
        }
}

for key, value in data.items():
    ref.child(key).set(value)