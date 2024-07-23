import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
import os

print("Webcam Connection established")

# Load images and class names
images = []
classNames = []
path = r"photos"
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    if curImg is not None:
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0].strip().lower())  # Use lowercase for consistency

# Load student details from CSV
student_details = {}
with open('input.csv', mode='r') as file:
    csvReader = csv.DictReader(file)
    for row in csvReader:
        student_details[row['Name'].strip().lower()] = row  # Use lowercase for consistency

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print("No face found in image, skipping:", img)
    return encodeList

def markAttendance(name, student_id):
    with open('Attendencebook.csv', 'r+', newline='') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%Y-%m-%d %H:%M:%S')
            f.writelines(f'\n{name},{student_id},{dtString}')

encodeListKnown = findEncodings(images)
print("Encoding of Images Completed!")

cap = cv2.VideoCapture(0)

try:
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            break
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].strip().lower()
                details = student_details.get(name)
                if details:
                    display_text = f"ID: {details['Student Id']}, Name: {details['Name']}, Branch: {details['Branch']}"
                    student_id = details['Student Id']
                else:
                    display_text = "Details not found"
                    student_id = 'Unknown'

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Display details at the top-left corner of the screen
                cv2.rectangle(img, (10, 10), (650, 60), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, display_text, (20, 40), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                markAttendance(name, student_id)
            else:
                name = 'Not Found'
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
