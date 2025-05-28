import cv2
from picamera2 import Picamera2
# Đường dẫn tới tệp cascade nhận diện khuôn mặt
cascade_path = "/home/meanlab/Trung/haarcascade_frontalface_default.xml"

# Khởi tạo bộ nhận diện khuôn mặt
face_cascade = cv2.CascadeClassifier(cascade_path)

# Kiểm tra xem tệp cascade có tải thành công không
if face_cascade.empty():
    print("Không thể tải tệp cascade!")
    exit()

# Khởi tạo camera
# Khởi tạo Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)  # Kích thước khung hình
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")

# Bắt đầu camera
picam2.start()

# camera_index = 0  # 0 cho camera mặc định
# cap = cv2.VideoCapture(camera_index)

# if not cap.isOpened():
#     print("Không thể mở camera!")
#     exit()
print("Đang chạy nhận diện khuôn mặt. Nhấn 'q' để thoát.")
index=1
while True:
    # Đọc từng khung hình từ camera
    frame = picam2.capture_array()
    # if not ret:
    #     print("Không thể nhận khung hình từ camera!")
    #     break

    # Chuyển đổi khung hình sang thang độ xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Nhận diện khuôn mặt
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Vẽ hình chữ nhật quanh các khuôn mặt được nhận diện
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Hiển thị khung hình
    cv2.imshow("Nhan Dien Khuon Mat", frame)

    # Nhấn phím 'q' để thoát
    inputKeyboard= cv2.waitKey(1) & 0xFF
    if inputKeyboard==ord('t'):
        strPath="test"+str(index)+".jpg"
        picam2.capture_file(strPath)
        index=index+1
    if inputKeyboard == ord('q'):
        break

# Giải phóng tài nguyên
# cap.release()
cv2.destroyAllWindows()