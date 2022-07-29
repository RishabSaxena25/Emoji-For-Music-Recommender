import mediapipe as mp
import numpy as np
import cv2

from cv2 import VideoCapture
from cv2 import waitKey
from cv2 import destroyAllWindows

#capture from the camera
cap = cv2.VideoCapture(0)

name = input("Enter the name of the data: ")

#Holistic for storing all the frames and store all the facial and hands keypoint
holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils

#To store set of rows
x = []
data_size=0

#capture from the camera
while True:
    #To store rows lst is used
    lst = []

    _, frm = cap.read()

    #To avoid mirror effect
    frm = cv2.flip(frm, 1)

    res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

#if someone is in the frame
    if res.face_landmarks:
        for i in res.face_landmarks.landmark:
            lst.append(i.x - res.face_landmarks.landmark[1].x)
            lst.append(i.y - res.face_landmarks.landmark[1].y)



        if res.left_hand_landmarks:
            for i in res.left_hand_landmarks.landmark:
                lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
        else:
            for i in range(42):
                lst.append(0.0)



        if res.right_hand_landmarks:
            for i in res.right_hand_landmarks.landmark:
                lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
                lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
        else:
            for i in range(42):
                lst.append(0.0)


        x.append(lst)
        data_size=data_size+1


    #For drawing the frames on our face and hands
    drawing.draw_landmarks(frm, res.face_landmarks, holistic.FACEMESH_CONTOURS)
    drawing.draw_landmarks(frm, res.left_hand_landmarks, hands.HAND_CONNECTIONS)
    drawing.draw_landmarks(frm, res.right_hand_landmarks, hands.HAND_CONNECTIONS)


    cv2.putText(frm, str(data_size), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)

    cv2.imshow("window", frm)

    if cv2.waitKey(1)==27 or data_size > 99:
        cv2.destroyAllWindows()
        cap.release()
        break

#To save data
np.save(f"{name}.npy", np.array(x))
print(np.array(x).shape)