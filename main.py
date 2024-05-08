
import cv2
import os
import pickle
import cvzone
import numpy as np
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattedancerealtime-b05cf-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattedancerealtime-b05cf.appspot.com"
})
bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 638)
cap.set(4, 479)

imageBackground = cv2.imread('resources/background.png')

folderModePath = 'resources/modes'
modePathList = os.listdir(folderModePath)
# Filter out irrelevant files and sort the list
modePathList = [file for file in modePathList if not file.startswith('.')]
modePathList.sort()

print(modePathList)

imgModeList = []

# Load images into imgModeList
for path in modePathList:
    img = cv2.imread(os.path.join(folderModePath,path))
    if img is not None:  # Ensure the image is loaded successfully
        imgModeList.append(img)

file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()

encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    resizedImg = cv2.resize(img,(640, 480))

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imageBackground[162:162 + 480, 55:55 + 640] = resizedImg

    # Check if imgModeList is not empty before accessing elements
    if imgModeList:
        imageBackground[44:44 + 633, 808:808 + 414] = imgModeList[min(modeType, len(imgModeList)-1)]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imageBackground = cvzone.cornerRect(imageBackground, bbox, rt=0)

                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imageBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imageBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                blob = bucket.get_blob(f'images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    if imgModeList:
                        imageBackground[44:44 + 633, 808:808 + 414] = imgModeList[min(modeType, len(imgModeList)-1)]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                if imgModeList:
                    imageBackground[44:44 + 633, 808:808 + 414] = imgModeList[min(modeType, len(imgModeList)-1)]

                if counter <= 10:
                    if imgModeList:
                        cv2.putText(  imageBackground, str(studentInfo['total_attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(  imageBackground, str(studentInfo['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(  imageBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imageBackground, str(studentInfo['standing']), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imageBackground, str(studentInfo['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(  imageBackground, str(studentInfo['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imageBackground, str(studentInfo['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                        imageBackground[175:175 + 216, 909:909 + 216] = imgStudent

                    counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    if imgModeList:
                        imageBackground[44:44 + 633, 808:808 + 414] = imgModeList[min(modeType, len(imgModeList)-1)]
    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Attendance", imageBackground)
    cv2.waitKey(1)
