import cv2
import os
import time
import json
from datetime import datetime


class CheckpointCapture:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.checkpoint_path = "checkpoint_captures"
        self.log_file = "logs/checkpoint_log.json"

        # Create directories
        if not os.path.exists(self.checkpoint_path):
            os.makedirs(self.checkpoint_path)
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def log_checkpoint_event(self, user_id, status, image_path):
        """Log checkpoint events to JSON file"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'status': status,
            'image_path': image_path
        }

        logs = []
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []

        logs.append(log_entry)

        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)

    def capture_single_checkpoint(self, checkpoint_name="main_gate"):
        """Capture single image at checkpoint when face is detected"""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open camera")
            return None

        print(f"Checkpoint '{checkpoint_name}' activated...")
        print("Looking for faces...")

        face_detected = False
        captured_image_path = None

        start_time = time.time()
        timeout = 30  # 30 seconds timeout

        while not face_detected and (time.time() - start_time) < timeout:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Face detected
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'Face Detected', (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # Save the captured image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"checkpoint_{checkpoint_name}_{timestamp}.jpg"
                captured_image_path = os.path.join(
                    self.checkpoint_path, filename)
                cv2.imwrite(captured_image_path, frame)

                face_detected = True
                print(f"Face detected and captured: {captured_image_path}")

                # Log the event
                self.log_checkpoint_event(
                    "unknown", "face_detected", captured_image_path)
                break

            # Display frame with instructions
            cv2.putText(frame, f'Checkpoint: {checkpoint_name}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, 'Looking for face...', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f'Timeout in: {int(timeout - (time.time() - start_time))}s',
                        (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow(f'Checkpoint: {checkpoint_name}', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if not face_detected:
            print("No face detected within timeout period")

        return captured_image_path

    def continuous_checkpoint_monitoring(self, checkpoint_name="main_gate"):
        """Continuous monitoring at checkpoint"""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        print(f"Continuous monitoring started at '{checkpoint_name}'")
        print("Press 'c' to manually capture, 'q' to quit")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            face_detected = len(faces) > 0

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'Face Detected', (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Display status
            status = "Face Detected" if face_detected else "No Face"
            color = (0, 255, 0) if face_detected else (0, 0, 255)
            cv2.putText(frame, f'Status: {status}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, "Press 'c' to capture, 'q' to quit", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow(f'Checkpoint Monitor: {checkpoint_name}', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                # Manual capture
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"manual_{checkpoint_name}_{timestamp}.jpg"
                captured_image_path = os.path.join(
                    self.checkpoint_path, filename)
                cv2.imwrite(captured_image_path, frame)
                print(f"Manual capture: {captured_image_path}")
                self.log_checkpoint_event(
                    "manual", "manual_capture", captured_image_path)

            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    checkpoint = CheckpointCapture()

    print("Choose mode:")
    print("1. Single capture (waits for face)")
    print("2. Continuous monitoring")

    choice = input("Enter choice (1 or 2): ")

    checkpoint_name = input(
        "Enter checkpoint name (default: main_gate): ") or "main_gate"

    if choice == "1":
        checkpoint.capture_single_checkpoint(checkpoint_name)
    elif choice == "2":
        checkpoint.continuous_checkpoint_monitoring(checkpoint_name)
    else:
        print("Invalid choice")
