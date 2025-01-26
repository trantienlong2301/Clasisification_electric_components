from ultralytics import YOLO
import cv2
import time
import sys
import pandas as pd
import cvzone
import numpy as np
from tracker import *
print("Python Executable:", sys.executable)
print("Python Path:", sys.path)

# Load model YOLOv8
model = YOLO("best.pt")  

count = 0
class_list = ['resistor', 'capacitor',  'led', 'button']
tracker0 = Tracker()
tracker1=Tracker()
tracker2=Tracker()
tracker3=Tracker()
list0=[]
list1=[]
list2=[]
list3=[]
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

    
    
    for index,row in px.iterrows():

 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if 're' in c:
           list0.append([x1,y1,x2,y2])
          
        elif'cap' in c:
            list1.append([x1,y1,x2,y2])
          
        elif 'le' in c:
            list2.append([x1,y1,x2,y2])
        elif 'bu' in c:
            list3.append([x1,y1,x2,y2])
   
    bbox0_idx=tracker0.update(list0)
    for bbox0 in bbox0_idx:
        x30,y30,x40,y40,id10=bbox0
        cx30=int(x30+x40)//2
        cy30=int(y30+y40)//2
       
        cv2.circle(frame,(cx30,cy30),4,(255,0,0),-1)
        cv2.rectangle(frame,(x30,y30),(x40,y40),(255,0,255),2)
        cvzone.putTextRect(frame,f'{id10}',(x30,y30),1,1)
    bbox1_idx=tracker1.update(list1)
    for bbox1 in bbox1_idx:
        x31,y31,x41,y41,id11=bbox1
        cx31=int(x31+x41)//2
        cy31=int(y31+y41)//2
       
        cv2.circle(frame,(cx31,cy31),4,(255,0,0),-1)
        cv2.rectangle(frame,(x31,y31),(x41,y41),(255,0,255),2)
        cvzone.putTextRect(frame,f'{id11}',(x31,y31),1,1)
    bbox2_idx=tracker2.update(list2)
    for bbox2 in bbox2_idx:
        x32,y32,x42,y42,id12=bbox2
        cx32=int(x32+x42)//2
        cy32=int(y32+y42)//2
       
        cv2.circle(frame,(cx32,cy32),4,(255,0,0),-1)
        cv2.rectangle(frame,(x32,y32),(x42,y42),(255,0,255),2)
        cvzone.putTextRect(frame,f'{id12}',(x32,y32),1,1)
    bbox3_idx=tracker3.update(list3)
    for bbox3 in bbox3_idx:
        x33,y33,x43,y43,id13=bbox3
        cx33=int(x33+x43)//2
        cy33=int(y33+y43)//2
       
        cv2.circle(frame,(cx33,cy33),4,(255,0,0),-1)
        cv2.rectangle(frame,(x33,y33),(x43,y43),(255,0,255),2)
        cvzone.putTextRect(frame,f'{id13}',(x33,y33),1,1)
    cv2.putText(frame, f'Resistors: {tracker0.id_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f'Capacitors: {tracker1.id_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f'LEDs: {tracker2.id_count}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f'Buttons: {tracker3.id_count}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)  
    if a is not None:
       list0=[]
       list1=[]
       list2=[]
       list3=[]
    cv2.imshow("HEHE", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
