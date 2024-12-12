# Description: Class file for the facial recognition part of the app.
import cv2
import os
import face_recognition
import face_recognition
import pickle
import glob

class FaceRecognition:
    def __init__(self):
        self.__dataset_dir = "dataset"
        self.__model_file = "known_faces.pkl"
        self.__face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    def get_face_cascade(self):
        return self.__face_cascade

    def get_model_file(self):
        return self.__model_file
    
    def get_dataset_dir(self):
        return self.__dataset_dir
    
    def generate_dataset(self, name):
        # Generating dataset and storing the images inside the dataset_dir.
        dataset_dir = self.get_dataset_dir()
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)

        video_capture = cv2.VideoCapture(0)
        img_count = 0

        while True:
            ret, frame = video_capture.read()

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.get_face_cascade().detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Draw boxes
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Save the face image to the dataset directory
                face_image = frame[y:y+h, x:x+w]
                img_count += 1
                cv2.imwrite(f"{dataset_dir}/{name}_{img_count}.jpg", face_image)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q') or img_count >= 50:
                break

    def train_model(self, known_face_encodings = [], known_face_labels = []):
        # Train the face recognition model and save it to a file.
        dataset_dir = self.get_dataset_dir()
        for filename in os.listdir(dataset_dir):
            if filename.endswith(".jpg"):
                img_path = os.path.join(dataset_dir, filename)

                image = cv2.imread(img_path)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                face_encodings_in_image = face_recognition.face_encodings(rgb_image)

                if face_encodings_in_image:
                    face_encoding = face_encodings_in_image[0]
                    label = filename.split('_')[0]
                    known_face_encodings.append(face_encoding)
                    known_face_labels.append(label)
                else:
                    print("No face encodings found in the image.")
        
        with open(self.get_model_file(), "wb") as model:
            pickle.dump((known_face_encodings, known_face_labels), model)
    
    def load_model(self):
        """Load the saved face recognition model."""
        if os.path.exists(self.get_model_file()):
            with open(self.get_model_file(), "rb") as f:
                known_face_encodings, known_face_labels = pickle.load(f)
            return known_face_encodings, known_face_labels
        else:
            raise FileNotFoundError("No saved model found. Please train the model first.")
        

    def recognize_faces(self, known_face_encodings, known_face_labels):
        """Recognize faces using the trained model."""
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings_in_image = face_recognition.face_encodings(rgb_image, face_locations)

            if face_encodings_in_image:
                top, right, bottom, left = face_locations[0]
                face_encoding = face_encodings_in_image[0]

                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    match_index = matches.index(True)
                    name = known_face_labels[match_index]

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                cv2.imshow('Face Recognition', frame)

                # Break the loop if the 'q' key is pressed or a face is recognized
                if cv2.waitKey(1) & 0xFF == ord('q') or name != "Unknown":
                    break

        return name
    
    def update_model_and_train(self):
        '''Updates and trains the model.'''
        try:
            known_faces, known_labels = self.load_model()
            self.train_model(known_faces, known_labels)
        except FileNotFoundError as err:
            print(err)
            self.train_model()
            known_faces, known_labels = self.load_model()

    def pipeline(self):
        """Run the face recognition pipeline."""
        known_faces, known_labels = self.load_model()
        name = self.recognize_faces(known_faces, known_labels)
        return name
    
    def check_if_registered(self, name):
        """Check if the person's face is already registered."""
        dataset_dir = self.get_dataset_dir()
        pattern = os.path.join(dataset_dir, f"{name}_*.jpg")
        matches = glob.glob(pattern)
        return len(matches) > 0