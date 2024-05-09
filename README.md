# FaceRecognition Attendance System

**This project is a real-time face attendance system using computer vision techniques and Firebase for data storage. The system recognizes faces in a live video stream, matches them with known students' faces, and updates their attendance records in a Firebase database.**

##Features##
- **Face Recognition**: Utilizes the face_recognition library to detect and recognize faces in real-time.
- **Firebase Integration**: Stores student information and attendance records in a Firebase real-time database.
- **Dynamic UI**: Displays student information and updates attendance status dynamically on the screen.
- **Mode Switching**: Supports switching between different display modes for better user interaction.

##Requirements##
Python 3.x
OpenCV
Numpy
Face Recognition Library (face_recognition)
Firebase Admin SDK
cvzone
Installation
Clone this repository:
bash
Copy code
git clone https://github.com/your_username/real-time-face-attendance-system.git
Install the required dependencies:
Copy code
pip install opencv-python numpy face-recognition firebase-admin cvzone
Obtain the Firebase service account key (serviceAccountKey.json) and place it in the root directory of the project.
Usage
Run the Python script:
Copy code
python face_attendance_system.py
Ensure that a webcam is connected to your system. The program will capture the video stream from the webcam and display the real-time face recognition system.
As faces are detected, the system will attempt to match them with known students' faces stored in the database. If a match is found, the student's information will be displayed, and their attendance status will be updated accordingly.
You can switch between different display modes by pressing certain keys or through user interaction.
Configuration
Update the EncodeFile.p file with the encodings of known faces.
Adjust the paths and filenames in the code according to your directory structure and file naming conventions.
Customize the Firebase database structure and storage paths as needed.
License
This project is licensed under the MIT License.


