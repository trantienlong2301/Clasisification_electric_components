import sys
from PyQt6.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt
import cv2
from YoloModel import YOLODetector  # Đảm bảo tệp YOLODetector hoạt động chính xác
import serial
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Thiết lập cửa sổ GUI
        self.setWindowTitle("YOLO Object Detection")
        self.setGeometry(100, 100, 800, 600)

        # Khởi tạo số lượng linh kiện
        self.counts = {"resistor": 0, "capacitor": 0, "led": 0, "button": 0}

        # Khởi tạo các thành phần giao diện
        self.title_label = QLabel("HỆ THỐNG PHÂN LOẠI LINH KIỆN ĐIỆN TỬ")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 20px; background-color: #2c3e50; border-radius: 10px;")

        self.image_label = QLabel("Camera Feed")
        self.image_label.setFixedSize(800, 500)  # Kích thước khung hình
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: black; border-radius: 10px;")

        self.info_label = QLabel("Bảng Linh Kiện")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("font-size: 18px; color: white; while: 10px; background-color: #333333; border-radius: 10px;")

        # Khởi tạo các nút
        self.start_button = QPushButton("Bật Camera")
        self.start_button.setStyleSheet(
            "background-color: green; color: white; font-size: 18px; border-radius: 10px; min-width: 150px; min-height: 50px;"
        )
        self.start_button.clicked.connect(self.start_camera)

        self.stop_button = QPushButton("Tắt Camera")
        self.stop_button.setStyleSheet(
            "background-color: red; color: white; font-size: 18px; border-radius: 10px; min-width: 150px; min-height: 50px;"
        )
        self.stop_button.clicked.connect(self.stop_camera)
        self.stop_button.setEnabled(False)

        # Thêm nút điều khiển động cơ
        self.motor_button = QPushButton("ĐỘNG CƠ")
        self.motor_button.setStyleSheet(
            "background-color: #f39c12; color: white; font-size: 18px; border-radius: 10px; min-width: 150px; min-height: 50px;"
        )
        self.motor_button.clicked.connect(self.toggle_motor)
        
        try:
            self.arduino = serial.Serial(port="COM9", baudrate=9600, timeout=1)  # Thay "COM3" bằng cổng Arduino trên máy bạn
        except serial.SerialException as e:
            self.arduino = None
            print(f"Lỗi kết nối Arduino: {e}")

        # Gọi hàm khởi tạo giao diện
        self.init_ui()

        # Khởi tạo YOLODetector
        self.detector = YOLODetector()

        # Timer để cập nhật khung hình
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

    def init_ui(self):
        # Layout chính
        main_layout = QVBoxLayout()

        # Thêm title vào layout
        main_layout.addWidget(self.title_label)

        # Layout cho camera và thông tin
        camera_info_layout = QHBoxLayout()

        # Layout bên phải (Thông tin và nút bấm)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.info_label)
        right_layout.addWidget(self.start_button)
        right_layout.addWidget(self.stop_button)
        right_layout.addWidget(self.motor_button)  # Thêm nút điều khiển động cơ
        right_layout.setSpacing(20)  # Thêm khoảng cách giữa các nút

        # Thêm các thành phần vào layout chính
        camera_info_layout.addWidget(self.image_label)  # Camera bên trái
        camera_info_layout.addLayout(right_layout)  # Thông tin và nút bên phải

        # Thêm layout camera và thông tin vào layout chính
        main_layout.addLayout(camera_info_layout)

        # Đặt layout chính
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #ecf0f1;")  # Màu nền sáng cho ứng dụng

    def start_camera(self):
        """Bật camera."""
        # self.cap = cv2.VideoCapture(0)  # Mở camera
        # if not self.cap.isOpened():
        #     self.image_label.setText("Không thể mở camera!")
        #     return
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.timer.start(30)  # Bắt đầu cập nhật khung hình

    def stop_camera(self):
        """Tắt camera."""
        self.timer.stop()
        # if self.cap:
        #     self.cap.release()
        self.image_label.setText("Camera đã tắt")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_frame(self):
        """Cập nhật khung hình từ camera và thông tin số lượng."""


        # Sử dụng YOLO để xử lý khung hình
        frame, counts, component = self.detector.process_frame()

        # Kiểm tra frame có hợp lệ không
        if frame is None or frame.size == 0:
            self.image_label.setText("Không có khung hình hợp lệ!")
            return
 
        if component ==0:
            self.send_command_to_arduino("0")
            print('0')
        if component ==1:
            self.send_command_to_arduino("1")
            print('1')
        if component ==2:
            self.send_command_to_arduino("2")
            print('2')
        if component ==3:
            self.send_command_to_arduino("3")
            print('3')
        # Hiển thị khung hình trên QLabel
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        qimg = QImage(rgb_image.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qimg))

        # Cập nhật thông tin số lượng
        info_text = (
            f"<p style='font-size:18px; font-weight:bold; color:#3498db;'>RESISTORs: "
            f"<span style='color:white;'>{counts['resistor']}</span></p>"
            f"<p style='font-size:18px; font-weight:bold; color:#9b59b6;'>CAPACITORs: "
            f"<span style='color:white;'>{counts['capacitor']}</span></p>"
            f"<p style='font-size:18px; font-weight:bold; color:#f39c12;'>LEDs: "
            f"<span style='color:white;'>{counts['led']}</span></p>"
            f"<p style='font-size:18px; font-weight:bold; color:#e74c3c;'>BUTTONs: "
            f"<span style='color:white;'>{counts['button']}</span></p>"
        )

        # Cập nhật văn bản cho QLabel
        self.info_label.setText(info_text)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def toggle_motor(self):
        """Chức năng điều khiển động cơ."""
        current_text = self.motor_button.text()

        if current_text == "BẬT ĐỘNG CƠ":
            # Giả sử bạn gửi lệnh bật động cơ
            self.motor_button.setText("TẮT ĐỘNG CƠ")
            self.send_command_to_arduino("ON")
            # Thêm mã lệnh điều khiển động cơ ở đây (ví dụ: GPIO.output(motor_pin, GPIO.HIGH))
            print("ĐỘNG CƠ ĐÃ BẬT")
        else:
            # Giả sử bạn gửi lệnh tắt động cơ
            self.motor_button.setText("BẬT ĐỘNG CƠ")
            # Thêm mã lệnh điều khiển động cơ ở đây (ví dụ: GPIO.output(motor_pin, GPIO.LOW))
            self.send_command_to_arduino("OFF")
            print("ĐỘNG CƠ ĐÃ TẮT")

    def send_command_to_arduino(self, command):
        """Gửi lệnh điều khiển đến Arduino."""
        try:
            self.arduino.write(f"{command}\n".encode())
        except serial.SerialException as e:
            print(f"Lỗi khi gửi lệnh: {e}")

    def closeEvent(self, event):
        """Dừng camera và giải phóng tài nguyên khi đóng ứng dụng."""
        self.timer.stop()
        self.detector.release_resources()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
