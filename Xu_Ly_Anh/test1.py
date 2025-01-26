import cv2
import numpy as np

cap = cv2.VideoCapture(1)

# Kiểm tra nếu camera mở thành công
if not cap.isOpened():
    print("Không thể mở camera.")
    exit()

# Đặt số lần chụp ảnh và tên file ảnh


# Kích thước mục tiêu


# Vòng lặp liên tục để chụp ảnh mỗi giây
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Không thể lấy khung hình từ camera.")
        break
    frame = cv2.medianBlur(frame,5)
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    kernel = np.array([[0, -1,  0],
                    [-1,  5, -1],
                    [0, -1,  0]])

    # Áp dụng bộ lọc
    sharpened = cv2.filter2D(blurred, -1, kernel)

    

    # Tạo ảnh sắc nét bằng cách cộng chênh lệch giữa ảnh gốc và ảnh làm mờ
    unsharpened = cv2.addWeighted(frame, 1.5, blurred, -0.7, 0)
# Hiển thị kết quả
    cv2.imshow('Original Image', frame)
    cv2.imshow('sharp', sharpened)
    cv2.imshow('unsharp', unsharpened)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()