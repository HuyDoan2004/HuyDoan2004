#sh1106 libary i2c
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import  sh1106
from PIL import Image, ImageDraw, ImageFont
#Gpio
import RPi.GPIO as GPIO
import time
# get IP 
import socket
import fcntl
import struct

# Định nghĩa lớp HCSR04
class HCSR04:
    def __init__(self, trig_pin, echo_pin,name):
        # Khởi tạo các chân GPIO
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.name=name
        # Thiết lập chế độ GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Thiết lập chân Trig là Output và chân Echo là Input
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    def print_distance(self):
        # Đảm bảo chân Trig tắt
        GPIO.output(self.trig_pin, False)
        time.sleep(0.5)
        
        # Kích hoạt Trig trong 10 microseconds
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)  # 10µs
        GPIO.output(self.trig_pin, False)
        
        # Đo thời gian nhận tín hiệu Echo
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
        
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()
        
        # Tính toán thời gian và khoảng cách
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Tốc độ âm thanh trong không khí (34300 cm/s / 2)
        distance = round(distance, 2)
        print("khoang cach do duoc cua ", self.name," la:", distance, "(cm)")
        return distance
    
    def cleanup(self):
        GPIO.cleanup()
##
## get IP 
def get_wifi_ip(interface="wlan0"):
    try:
        # Tạo socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Lấy địa chỉ IP của giao diện mạng (wlan0)
        ip_address = socket.inet_ntoa(
            fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR: Lấy địa chỉ IP
                struct.pack('256s', interface[:15].encode('utf-8'))
            )[20:24]
        )
        return ip_address
    except Exception as e:
        return f"Không thể lấy địa chỉ IP của {interface}: {e}"

# Sử dụng lớp HCSR04
if __name__ == "__main__":
    # Khởi tạo cảm biến HC-SR04 với Trig ở GPIO 23 và Echo ở GPIO 24
    sensor_sieAm_1 = HCSR04(trig_pin=27, echo_pin=22, name="cam bien sieu am 1")
    sensor_sieAm_2 = HCSR04(trig_pin=24, echo_pin=10, name="cam bien sieu am 2")
    sensor_sieAm_3 = HCSR04(trig_pin=9, echo_pin=23, name="cam bien sieu am 3")
    sensor_sieAm_4 = HCSR04(trig_pin=17, echo_pin=18, name="cam bien sieu am 4")
    # rev.1 users set port=0
    # substitute spi(device=0, port=0) below if using that interface
    # substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
    serial = i2c(port=1, address=0x3C)
    # substitute ssd1331(...) or sh1106(...) below if using that device
    device = sh1106(serial)
    font=ImageFont.load_default()

    ## get Ip
    interface = "wlan0"  # Giao diện WiFi mặc định
    ip = get_wifi_ip(interface)
    print(f"Địa chỉ IP WiFi ({interface}): {ip}")
    try:
        while True:
            # Đo khoảng cách và in ra màn hình
            distance_Sensor_1=sensor_sieAm_1.print_distance()
            distance_Sensor_2=sensor_sieAm_2.print_distance()
            distance_Sensor_3=sensor_sieAm_3.print_distance()
            distance_Sensor_4=sensor_sieAm_4.print_distance()
            
            # sieu_am_1=hcSR_distance(23,24,"sieu am 1")
            # dist_1= sieu_am_1.measure_distance()
            # dist_1="Khoang cach "+str(dist_1)
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                # draw.textbbox((10,10),dist_1,stroke_width=1,font=font)
                # draw.text((20, 30), str(distance_Sensor_1), fill="white")
                draw.text((20, 30), str(ip), fill="white")
                draw.arc([(0,0),(128,64)], 0,360,fill="white",width=1)
                # draw.ellipse([(30,30),(100,60)],outline="red",width=2)
                # print("Khoảng cách đo được: ", distance, "cm")
                time.sleep(1)
    except KeyboardInterrupt:
        print("Dừng chương trình")
    finally:
        # Dọn dẹp GPIO sau khi kết thúc
        sensor_sieAm_1.cleanup()
        sensor_sieAm_2.cleanup()
        sensor_sieAm_3.cleanup()
        sensor_sieAm_4.cleanup()
