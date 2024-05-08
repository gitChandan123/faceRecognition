import os
import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattedancerealtime-b05cf-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattedancerealtime-b05cf.appspot.com"
})


# importing student images
folderPath = 'images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []

# print(pathList)

# print(pathList)

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


studentIds = studentIds[1:]
# print(studentIds)
# studentIds = studentIds[1:]
imgList = imgList[1:]
# imgList = imgList[::-1]
# print(len(imgList))

def findEncoding(imageList):
    encodeList = []
    for img in imageList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


print("encoding started.......")
encodeListKnown = findEncoding(imgList)
encodeListKnownWithIds = [encodeListKnown,studentIds]
# print(encodeListKnown)
print("encoding completed......")

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close

# print("FILE SAVED")


