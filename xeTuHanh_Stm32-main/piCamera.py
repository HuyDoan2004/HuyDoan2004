from picamera2 import Picamera2
import cv2

# Khởi tạo Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)  # Kích thước khung hình
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")

# Bắt đầu camera
picam2.start()

print("Đang mở camera. Nhấn Ctrl+C để thoát.")

index=1

try:
    while True:
        frame = picam2.capture_array()  # Lấy khung hình từ camera
        cv2.imshow("Camera", frame)
        
        # Thoát khi nhấn 'q'
        # if cv2.waitKey(1000) & 0xFF == ord('q'):
        #     break
        # chụp ảnh màn hình khi nhấn 't'
        if cv2.waitKey(10) & 0xFF == ord('t'):
            # strPath="test"+str(index)+".jpg"
            # picam2.capture_file(strPath)
            # index=index+1
            print (frame[1], len(frame[1]))
except KeyboardInterrupt:
    print("Đang dừng camera...")

# # # Giải phóng tài nguyên
# # cv2.destroyAllWindows()
# # picam2.stop()
# import time
# import picamera

# from picamera2 import Picamera2
# from picamera2.encoders import H264Encoder

# picam2 = Picamera2()
# video_config = picam2.create_video_configuration()
# picam2.configure(video_config)

# encoder = H264Encoder(10000000)

# picam2.start_recording(encoder, 'test.h264')
# time.sleep(10)
# picam2.stop_recording()
# from picamera2 import Picamera2, Preview
# import time
# picam2 = Picamera2()
# camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
# picam2.configure(camera_config)
# picam2.start_preview(Preview.QTGL)
# picam2.start()
# time.sleep(2)
# picam2.capture_file("test.jpg")
# import time

# from picamera2 import Picamera2, Preview

# picam2 = Picamera2()

# preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
# picam2.configure(preview_config)

# picam2.start_preview(Preview.QTGL)

# picam2.start()
# time.sleep(2)

# picam2.capture_file("test.jpg")
# # print(metadata)

# picam2.close()
# # from picamera2 import Picamera2, Preview
# import time
# picam2 = Picamera2()
# camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
# picam2.configure(camera_config)
# picam2.start_preview(Preview.QTGL)
# picam2.start()
# time.sleep(2)
# picam2.capture_file("test.jpg")


