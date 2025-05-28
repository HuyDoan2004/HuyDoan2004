import cv2

# Đường dẫn đến tệp Haar Cascade
cascade_path = "haarcascade_frontalface_default.xml"

# Kiểm tra camera
camera_index = 0  # Thường là 0 cho camera mặc định
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("Không thể mở camera!")
    exit()

# Tải Haar Cascade để nhận diện khuôn mặt
face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    print("Không thể tải tệp cascade!")
    exit()

print("Đang chạy nhận diện khuôn mặt. Nhấn 'q' để thoát.")

while True:
    # Đọc hình ảnh từ camera
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc hình ảnh từ camera!")
        break

    # Chuyển ảnh sang thang độ xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Vẽ hình chữ nhật quanh khuôn mặtpip3 install numpy
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Hiển thị khung hình
    cv2.imshow("Nhan Dien Khuon Mat", frame)

    # Nhấn phím 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
