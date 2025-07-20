import cv2
import dlib
import numpy as np
import time
import socket

def eye_aspect_ratio(eye):
    # Eye Aspect Ratio (EAR)
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def detect_eye_closure():
    # Load face detector and landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('/home/nico-to/Coding/qnx-testing/shape_predictor_68_face_landmarks.dat')

    # Start webcam
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    closure_time_threshold = 1 # Eye closure duration in seconds

    # Thresholds and variables
    EAR_THRESHOLD = 0.15
    eyes_closed_start_time = None  # Track the time when eyes are first closed
    wake_up_printed = False 

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if len(faces) > 0:
            face = faces[0]
            landmarks = predictor(gray, face)
            landmarks = np.array([(p.x, p.y) for p in landmarks.parts()])

            left_eye = landmarks[36:42]
            right_eye = landmarks[42:48]
            ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

            if ear < EAR_THRESHOLD:
                # Eyes are closed
                if eyes_closed_start_time is None:
                    eyes_closed_start_time = time.time()  # Record the time when eyes first closed
                    print(eyes_closed_start_time)
                elapsed_time = time.time() - eyes_closed_start_time

                if elapsed_time >= closure_time_threshold and not wake_up_printed:
                    print("WAKE UP")
                    # s.sendall(b'WAKE UP!')
                    wake_up_printed = True  # Ensure "WAKE UP" is printed only once
                # print("Eyes closed")
            else:
                if eyes_closed_start_time != None and float(eyes_closed_start_time) - time.time() >= 0.1:
                    eyes_closed_start_time = None  # Reset the closed time when eyes open
                wake_up_printed = False  # Reset the flag to allow for future "WAKE UP" detection
                # print(eyes_closed_start_time)
                # s.sendall(b'normal')
                # print("Eyes opened")

            cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (255, 0, 0), 2)

        cv2.imshow('Eye Closure Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
HOST = 'qnxpi.local'  # Replace with Raspberry Pi's IP
PORT = 5001
if __name__ == "__main__":
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT))
    detect_eye_closure()