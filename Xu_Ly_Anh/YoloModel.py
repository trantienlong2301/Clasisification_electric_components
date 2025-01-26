from ultralytics import YOLO
import cv2
import pandas as pd
import numpy as np

class YOLODetector:
    def __init__(self, model_path="best.pt", camera_index=1):
        """
        Khởi tạo YOLODetector với mô hình YOLOv8 và camera.
        """
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(camera_index)
        self.counts = {"resistor": 0, "capacitor": 0, "led": 0, "button": 0}
        self.previous_positions = {"resistor": 0, "capacitor": 0, "led": 0, "button": 0}
        self.current_positions = {"resistor": 0, "capacitor": 0, "led": 0, "button": 0}
        self.class_list = ['resistor', 'capacitor', 'led', 'button']
        self.dem = 0
        self.Object = None
    def process_frame(self):
        """
        Xử lý một khung hình từ camera và trả về kết quả:
        - frame: Khung hình đã được chú thích.
        - counts: Số lượng các đối tượng được phát hiện (dictionary).
        """
        ret, frame = self.cap.read()
        if not ret:
            return None, self.counts, self.Object

        # Làm mịn và tăng cường khung hình
        frame = cv2.medianBlur(frame, 5)
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        frame = cv2.addWeighted(frame, 1.5, blurred, -0.7, 0)

        # Dự đoán các đối tượng trong khung hình
        results = self.model.predict(frame)
        detections = results[0].boxes.data

        # Nếu không có đối tượng nào được phát hiện
        if len(detections) == 0:
            self.dem += 1
            if self.dem > 3:
                self.previous_positions = {key: 0 for key in self.previous_positions}
                self.current_positions = {key: 0 for key in self.current_positions}
                self.dem = 0
            return frame, self.counts, self.Object

        df = pd.DataFrame(detections).astype("float")

        # Duyệt qua từng đối tượng được phát hiện
        for _, row in df.iterrows():
            x1, y1, x2, y2, _, class_id = map(int, row)
            class_name = self.class_list[class_id]
            cv2.rectangle(frame,(x1,y1),((x2),(y2)),(255,0,255),2)
            if 're' in class_name:
                self.current_positions["resistor"] = (x1+x2)//2
                if abs(self.current_positions["resistor"]- self.previous_positions["resistor"])>100:
                    self.counts["resistor"] +=1
                self.Object = 0
            elif'cap' in class_name:
                self.current_positions["capacitor"] = (x1+x2)//2
                if abs(self.current_positions["capacitor"]- self.previous_positions["capacitor"])>100:
                    self.counts["capacitor"] +=1
                self.Object = 1
            elif 'le' in class_name:
                self.current_positions["led"] = (x1+x2)//2
                if abs(self.current_positions["led"]- self.previous_positions["led"])>100:
                    self.counts["led"] +=1
                self.Object = 2
            elif 'bu' in class_name:
                self.current_positions["button"] = (x1+x2)//2
                if abs(self.current_positions["button"]- self.previous_positions["button"])>100:
                    self.counts["button"] +=1
                self.Object = 3
            self.previous_positions = self.current_positions
            

            # Vẽ khung chữ nhật và nhãn lên khung hình
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        return frame, self.counts, self.Object

    def release_resources(self):
        """
        Giải phóng tài nguyên camera.
        """
        self.cap.release()
        cv2.destroyAllWindows()
