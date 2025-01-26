from ultralytics import YOLO
import cv2
import time
import sys
import numpy as np
import pandas as pd

print("Python Executable:", sys.executable)
print("Python Path:", sys.path)

# Load model YOLOv8
model = YOLO("best.pt")  
count =0
dem = 0
count0 = 0
count1 = 0
count2 = 0
count3 = 0
list_0=0
list_1=0
list_2=0
list_3=0
list0=0
list1=0
list2=0
list3=0
class_list = ['resistor', 'capacitor',  'led', 'button']
cap = cv2.VideoCapture(1)  
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
   
    frame = cv2.medianBlur(frame,5)
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    frame = cv2.addWeighted(frame, 1.5, blurred, -0.7, 0)
    
    results = model.predict(frame)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
    if len(a) == 0:
        dem +=1
        if dem > 3:
            list_0=0
            list_1=0
            list_2=0
            list_3=0
            list0=0
            list1=0
            list2=0
            list3=0
            dem = 0
    for index,row in px.iterrows():

 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        cv2.rectangle(frame,(x1,y1),((x2),(y2)),(255,0,255),2)
        if 're' in c:
           list0 = (x1+x2)//2
          
        elif'cap' in c:
            list1 = (x1+x2)//2
          
        elif 'le' in c:
            list2 = (x1+x2)//2
        elif 'bu' in c:
            list3 = (x1+x2)//2
    if abs(list0-list_0)>100:
        count0 +=1
    list_0 = list0
    if abs(list1-list_1)>100:
        count1 +=1
    list_1 = list1
    if abs(list2-list_2)>100:
        count2 +=1
    list_2 = list2
    if abs(list3-list_3)>100:
        count3 +=1
    list_3 = list3
    cv2.putText(frame, f'Resistors: {count0}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f'Capacitors: {count1}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f'LEDs: {count2}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f'Buttons: {count3}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2) 
    cv2.putText(frame, f'list0: {list0}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2) 
    cv2.putText(frame, f'list_0: {list_0}', (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2) 
    cv2.imshow("HEHE", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
