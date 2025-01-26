import sys
import cv2
import time
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from ultralytics import YOLO


class YOLOCameraApp(QWidget):
    def __init__(self):
        super().__init__()

        # Cấu hình cửa sổ chính
        self.setWindowTitle("Phát hiện linh kiện điện tử")
        self.setGeometry(100, 100, 1200, 800)

        # Layout chính
        main_layout = QHBoxLayout()

        # Widget hiển thị camera
        self.camera_label = QLabel("Camera Feed")
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setStyleSheet("border: 1px solid black;")
        self.camera_label.setFixedSize(800, 600)
        main_layout.addWidget(self.camera_label)

        # Widget hiển thị dữ liệu phát hiện
        self.data_widget = QWidget()
        data_layout = QVBoxLayout()

        # Tên linh kiện và số lượng
        self.components_count = {
            "Điện trở": 0,
            "Tụ điện": 0,
            "LED": 0,
            "Nút bấm": 0
        }
        self.labels = {}
        for component in self.components_count:
            label = QLabel(f"{component}: 0")
            label.setStyleSheet("font-size: 14px; padding: 5px;")
            data_layout.addWidget(label)
            self.labels[component] = label

        self.data_widget.setLayout(data_layout)
        self.data_widget.setFixedWidth(300)
        main_layout.addWidget(self.data_widget)

        # Thiết lập layout cho cửa sổ
        self.setLayout(main_layout)

        # Load model YOLOv8
        self.model = YOLO("best.pt")

        # Biến camera và timer
        self.cap = cv2.VideoCapture(1)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.frames = 0
        self.start_time = time.time()

    def update_frame(self):
        """Cập nhật khung hình từ camera và chạy YOLO."""
        ret, frame = self.cap.read()
        if not ret:
            self.camera_label.setText("Không nhận được khung hình từ camera!")
            return

        # Chạy YOLO trên khung hình
        results = self.model(frame)

        # Annotate frame
        annotated_frame = results[0].plot()

        # Hiển thị khung hình lên giao diện
        rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(q_image))

        # Cập nhật dữ liệu phát hiện
        self.update_component_counts(results)

    def update_component_counts(self, results):
        """Cập nhật số lượng linh kiện phát hiện được."""
        # Đặt lại số lượng linh kiện
        for component in self.components_count:
            self.components_count[component] = 0

        # Trích xuất dữ liệu phát hiện
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]

                # So khớp tên với các linh kiện
                if class_name in self.components_count:
                    self.components_count[class_name] += 1

        # Hiển thị số lượng cập nhật lên giao diện
        for component, count in self.components_count.items():
            self.labels[component].setText(f"{component}: {count}")

    def closeEvent(self, event):
        """Xử lý khi đóng ứng dụng."""
        self.cap.release()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YOLOCameraApp()
    window.show()
    sys.exit(app.exec())
