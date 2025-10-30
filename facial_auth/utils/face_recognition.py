import cv2
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity


class FaceRecognition:
    def __init__(self):
        # Initialize face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def capture_face_encoding(self):
        """Capture face from webcam and return encoding"""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise Exception("Could not open webcam")

        print("Looking for face... Press SPACE to capture, ESC to cancel")

        face_encoding = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            # Draw rectangle around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # Add instruction text
                cv2.putText(frame, 'Face Detected! Press SPACE to capture',
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow(
                'Face Capture - Press SPACE to capture, ESC to cancel', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # SPACE key
                if len(faces) > 0:
                    # Use the first detected face
                    face_encoding = self.simulate_face_encoding(gray, faces[0])
                    break
                else:
                    print("No face detected!")
            elif key == 27:  # ESC key
                break

        cap.release()
        cv2.destroyAllWindows()
        return face_encoding.tolist() if face_encoding is not None else None

    def simulate_face_encoding(self, gray_face, face_coords):
        """Simulate face encoding generation"""
        x, y, w, h = face_coords
        face_roi = gray_face[y:y+h, x:x+w]

        # Resize to standard size
        face_roi = cv2.resize(face_roi, (100, 100))

        # Flatten and normalize to simulate encoding
        encoding = face_roi.flatten().astype(np.float32) / 255.0

        # Add some random variation to make encodings unique
        encoding += np.random.normal(0, 0.01, encoding.shape)

        return encoding

    def verify_face(self, stored_encoding, current_encoding, threshold=0.8):
        """Verify if two face encodings match"""
        stored = np.array(stored_encoding).reshape(1, -1)
        current = np.array(current_encoding).reshape(1, -1)

        # Calculate cosine similarity
        similarity = cosine_similarity(stored, current)[0][0]

        return similarity >= threshold, similarity


# Create global instance
face_recognition = FaceRecognition()
