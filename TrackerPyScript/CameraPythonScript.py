
import numpy as np
import cv2
import serial
import time
PORT = 'COM3'
BAUD_RATE=9600

try:
    seri = serial.Serial(PORT , BAUD_RATE , timeout=1)
    time.sleep(2)
except serial.SerialException as e :
    exit()

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_POS_FRAMES, 100)
cap.set(cv2.CAP_PROP_GAIN,60)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
while True:
    
    _ , frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(grey , scaleFactor= 1.1, minNeighbors=1 ,minSize= (50, 50))
    largest_face=None
    max_area=0
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            area = w * h
            if area > max_area:
                max_area = area
                largest_face = (x, y, w, h)
            
        if largest_face is not None:
            x_largest, y_largest, w_largest, h_largest = largest_face
            
            # draw rec
            cv2.rectangle(frame, (x_largest, y_largest), (x_largest + w_largest, y_largest + h_largest), (255, 0, 0), 2)
            face_centre = x_largest + w_largest //2
            print(f"Sending X: {x_largest} 'Sending W:' {w_largest}")

            # Serial Data is sent over
            data= f"{face_centre}\n"
            try:
                seri.write(data.encode("utf-8"))
                print(f"Sending Face Center: {face_centre}")
            except serial.SerialException as e:
                break

    cv2.imshow("Face Detection" , frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Video Resolution: {width}x{height}")
cap.release()
cv2.destroyAllWindows()
print("Finished")
