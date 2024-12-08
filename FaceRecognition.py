# Description: Class file for the facial recognition part of the app.
import cv2
import os

class FaceRecognition:
    def generate_dataset(name):
        if not os.path.exists("dataset"):
            os.makedirs("dataset")

    
        video_capture = cv2.VideoCapture(0)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        img_count = 0
        

        while True:
            ret, frame = video_capture.read()

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            
            for (x, y, w, h) in faces:
                # Draw boxes
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Save the face image to the dataset directory
                face_image = frame[y:y+h, x:x+w]
                img_count += 1
                cv2.imwrite(f"dataset/{name}_{img_count}.jpg", face_image)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q') or img_count >= 50:
                break