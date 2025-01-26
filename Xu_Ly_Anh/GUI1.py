import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer
import cv2
from YoloModel import YOLODetector

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Thiết lập cửa sổ GUI
        self.setWindowTitle("YOLO Object Detection")
        self.setGeometry(100, 100, 800, 600)

        # Khởi tạo các thành phần
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(800, 450)  # Kích thước khung hình

        self.info_label = QLabel(self)
        self.info_label.setText("Initializing...")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.info_label)
        self.setLayout(layout)

        # Khởi tạo YOLODetector
        self.detector = YOLODetector()

        # Timer để cập nhật khung hình
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Cập nhật mỗi 30ms

    def update_frame(self):
        # Lấy khung hình và số lượng đối tượng
        frame, counts = self.detector.process_frame()

        if frame is None:
            self.info_label.setText("Camera not available")
            return

        # Hiển thị khung hình trên QLabel
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        qimg = QImage(rgb_image.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qimg))

        # Cập nhật thông tin số lượng đối tượng
        info_text = (f"Resistors: {counts['resistor']}\n"
                     f"Capacitors: {counts['capacitor']}\n"
                     f"LEDs: {counts['led']}\n"
                     f"Buttons: {counts['button']}")
        self.info_label.setText(info_text)

    def closeEvent(self, event):
        # Dừng camera và giải phóng tài nguyên khi đóng ứng dụng
        self.detector.release_resources()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
