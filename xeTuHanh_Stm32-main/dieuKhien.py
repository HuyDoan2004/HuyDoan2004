# import RPi.GPIO as GPIO
import RPi.GPIO as GPIO
import time 
from adafruit_ssd1306 import SSD1306_I2C
import board
import busio
from PIL import Image, ImageDraw, ImageFont

# import threading

# tao lop do khoang cach
class hcSR_distance:
    
    def __init__(self, trigPin, echoPin): #haam khoi tao
        # self.trigPin=IntVar()
        # self.trigPin=int(trigPin)
        self.trigPin=trigPin
        self.echoPin=echoPin
        # self.name=name
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.trigPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)
        

    def measure_distance(self):
    # Đảm bảo chân Trig tắt
        GPIO.output(self.trigPin, False)
        time.sleep(0.5)
        
        # Kích hoạt Trig trong 10 microseconds
        GPIO.output(self.trigPin, True)
        time.sleep(0.00001)  # 10µs
        GPIO.output(self.trigPin, False)
        
        # Đo thời gian nhận tín hiệu Echo
        while GPIO.input(self.echoPin) == 0:
            pulse_start = time.time()
        
        while GPIO.input(self.echoPin) == 1:
            pulse_end = time.time()
        
        # Tính toán thời gian và khoảng cách
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Tốc độ âm thanh trong không khí (34300 cm/s / 2)
        distance = round(distance, 2)
        # print("khoảng cách",self.name,"là ", distance)
        return distance


try:
    sieuAm_1=hcSR_distance(23, 24)
    # sieuAm_2=hcSR_distance(22, 27, "siêu âm 2")
    while True:        
        dist_1=sieuAm_1.measure_distance()
        # thraedDist_1=threading.Thread(target= sieuAm_1.measure_distance())
        # thraedDist_2=threading.Thread(target= sieuAm_2.measure_distance())
        # thraedDist_1.start()
        # thraedDist_1.join()
        # thraedDist_2.start()
        # thraedDist_2.join()
        # dist_2=sieuAm_2.measure_distance()
        print("Khoảng cách đo được ở cảm biến siêu âm 1: ", dist_1, "cm")
        # print("Khoảng cách đo được ở cảm biến siêu âm 2: ", dist_2, "cm")
        time.sleep(1)
    
except KeyboardInterrupt:
    print("Dừng chương trình")
  
