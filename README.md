Attendance System Using Face Recognition



This project is an attendance system that leverages face recognition technology to automatically mark attendance. The system captures real-time images from a webcam, recognizes faces, and logs attendance details into a CSV file.

Prerequisites
Before running the project, ensure you have Python 3.x, OpenCV, the face_recognition library, and NumPy installed. These libraries are essential for processing images and recognizing faces.

Project Structure
The project consists of several components. The photos/ directory contains images of the students, while the input.csv file holds student details, including Name, Student Id, and Branch. The Attendencebook.csv file is used to store attendance records. The main script, attendance_system.py, runs the attendance system.

Setup
To set up the project, first, prepare the images by placing them in the photos/ directory. Ensure that each image file name corresponds to the student's name (e.g., john_doe.jpg). Next, create an input.csv file with columns for Name, Student Id, and Branch. Make sure the names in the Name column match the image file names.

Usage
To use the system, run the main script to start the attendance system. This will open a webcam feed. As the system recognizes faces, it will display the student's details and log their attendance in Attendencebook.csv. You can press 'q' to quit the webcam feed.

How It Works
The script begins by loading images from the photos/ directory and computing their face encodings. It then processes the webcam feed frame by frame, resizing and converting each frame to RGB. Faces in the frame are located and encoded. The script compares these face encodings with the known encodings, and if a match is found, it displays the student's details and marks their attendance.

Marking Attendance
Attendance is logged in Attendencebook.csv, including the student's name, ID, and a timestamp. This ensures that the attendance records are updated in real-time as students are recognized.

Notes
Ensure that the images in the photos/ directory are clear and prominently display the student's face. The script assumes that the Name column in input.csv matches the image file names. If the system fails to capture images from the webcam, make sure the webcam is properly connected and accessible. If a face is not recognized, check the quality and clarity of the images in the photos/ directory, and ensure that the input.csv file is correctly formatted and matches the image file names.

