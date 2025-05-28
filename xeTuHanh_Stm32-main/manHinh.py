#thu vien man hinh hien thi
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import  sh1106
from PIL import Image, ImageDraw, ImageFont
#thu vien giao tiep gpio thu khoang cach
import RPi.GPIO as GPIO
import time

class hcSR_distance:    #class do khoang cach sieu am
    
    def __init__(self, trigPin, echoPin,name): #haam khoi tao

        self.trigPin=trigPin
        self.echoPin=echoPin
        self.name=name
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
        # Distance= str("khoang cach"+self.name+" la " + distance)
        return distance
        # return Distance

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = sh1106(serial)
font=ImageFont.load_default()
while True:
    sieu_am_1=hcSR_distance(23,24,"sieu am 1")
    dist_1= sieu_am_1.measure_distance()
    dist_1="Khoang cach "+str(dist_1)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        # draw.textbbox((10,10),dist_1,stroke_width=1,font=font)
        draw.text((20, 30), dist_1, fill="white")
        draw.arc([(0,0),(128,64)], 0,360,fill="white",width=1)
        # draw.ellipse([(30,30),(100,60)],outline="red",width=2)