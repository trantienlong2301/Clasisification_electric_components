import cv2
import time
import numpy as np

# Mở camera (0 là camera mặc định, có thể thay đổi nếu bạn có nhiều camera)
cap = cv2.VideoCapture(1)

# Kiểm tra nếu camera mở thành công
if not cap.isOpened():
    print("Không thể mở camera.")
    exit()

# Đặt số lần chụp ảnh và tên file ảnh
counter = 721

# Kích thước mục tiêu
target_size = (640, 640)

# Vòng lặp liên tục để chụp ảnh mỗi giây
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Không thể lấy khung hình từ camera.")
        break

    # Lấy kích thước ảnh ban đầu
    h, w = frame.shape[:2]
    frame = cv2.medianBlur(frame,5)
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    frame = cv2.addWeighted(frame, 1.5, blurred, -0.7, 0)
    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Tính toán tỷ lệ resize
    if w > h:
        new_w = target_size[0]
        new_h = int(h * (new_w / w))
    else:
        new_h = target_size[1]
        new_w = int(w * (new_h / h))
    
    # Resize ảnh
    resized_frame = cv2.resize(frame, (new_w, new_h))
    
    # Tạo padding nếu cần
    top = (target_size[1] - new_h) // 2
    bottom = target_size[1] - new_h - top
    left = (target_size[0] - new_w) // 2
    right = target_size[0] - new_w - left
    
    # Thêm padding vào ảnh
    padded_frame = cv2.copyMakeBorder(resized_frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    
    resized2_frame = cv2.resize(frame2, (new_w, new_h))
    
    # Tạo padding nếu cần
    top = (target_size[1] - new_h) // 2
    bottom = target_size[1] - new_h - top
    left = (target_size[0] - new_w) // 2
    right = target_size[0] - new_w - left
    
    # Thêm padding vào ảnh
    padded2_frame = cv2.copyMakeBorder(resized2_frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    # Lưu ảnh vào file mỗi giây
    cv2.imshow('Camera', padded_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('a'): 
        counter += 1
        filename = f'{counter}.jpg'
        filename2 = f'A{counter}.jpg'
        cv2.imwrite(filename, padded_frame)
        cv2.imwrite(filename2, padded2_frame)
        print(f"Ảnh đã được lưu thành công: {filename}")
    elif  key == ord('q'):
        break

# Giải phóng camera và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
