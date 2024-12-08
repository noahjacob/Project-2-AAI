# Description: Class file for the facial recognition part of the app.
import cv2
import os
import face_recognition

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

    def train_model():
        known_face_encodings = []
        known_face_labels = []
        dataset_dir = "dataset"
        for filename in os.listdir(dataset_dir):
            if filename.endswith(".jpg"):
                img_path = os.path.join(dataset_dir, filename)

                image = cv2.imread(img_path)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                face_encodings_in_image = face_recognition.face_encodings(rgb_image)
                
                # Assuming only one face in image.
                if face_encodings_in_image:
                    face_encoding = face_encodings_in_image[0]
                    label = filename.split('_')[0]
                    known_face_encodings.append(face_encoding)
                    known_face_labels.append(label)
                else:
                    print("No Face Encodings")