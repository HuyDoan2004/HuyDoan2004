import RPi.GPIO as GPIO
import time

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
        # return distance
    
    def cleanup(self):
        GPIO.cleanup()


# Sử dụng lớp HCSR04
if __name__ == "__main__":
    # Khởi tạo cảm biến HC-SR04 với Trig ở GPIO 23 và Echo ở GPIO 24
    sensor_sieAm_1 = HCSR04(trig_pin=27, echo_pin=22, name="cam bien sieu am 1")
    sensor_sieAm_2 = HCSR04(trig_pin=24, echo_pin=10, name="cam bien sieu am 2")
    sensor_sieAm_3 = HCSR04(trig_pin=9, echo_pin=23, name="cam bien sieu am 3")
    sensor_sieAm_4 = HCSR04(trig_pin=17, echo_pin=18, name="cam bien sieu am 4")
    
    try:
        while True:
            # Đo khoảng cách và in ra màn hình
            sensor_sieAm_1.print_distance()
            sensor_sieAm_2.print_distance()
            sensor_sieAm_3.print_distance()
            sensor_sieAm_4.print_distance()
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
