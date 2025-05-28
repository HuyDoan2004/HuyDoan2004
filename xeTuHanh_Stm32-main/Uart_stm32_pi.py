import serial
import time

# ser = serial.Serial(
#         port='/dev/ttyAMA0',  # Hoặc /dev/ttyS0 nếu sử dụng UART mini
#         baudrate=9600,        # Tốc độ baud, phải khớp với STM32
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
# #         timeout=1             # Thời gian chờ nhận dữ liệu (giây)
#     )
    
#     # Kiểm tra kết nối
# if ser.isOpen():
#     print("UART kết nối thành công!")

    # if ser.in_waiting:
    
# ser.write(0x44)
# time.sleep(0.1)
# t=0
while True:
    c=input("nhap vao ky tu gui di: ")
    if c:
        # ser.write(c.encode())
        print("da gui chu ",c[0])
        # time.sleep(1)
        # x=ser.read(1)
        # print("chuoi",x)

        # t=t+1


# while True:
# 	ser.write('D')
# 	print("da gui chu D")
# 	time.sleep(1)
#     # sc=chuoi.decode()
#     # print ("chuoi sau decode:", sc)
# import time
# import serial
 
# ser = serial.Serial(
# 	port = '/dev/ttyAMA0',
# 	baudrate = 9600,
# 	parity = serial.PARITY_NONE,
# 	stopbits = serial.STOPBITS_ONE,
# 	bytesize = serial.EIGHTBITS,
# 	timeout = 1
# )
 
# print("Raspberry's receiving : ")
 
# try:
#     while True:
#         s = ser.read(1)
#         data = s.decode()			# decode s
#         # data = data.rstrip()			# cut "\r\n" at last of string
#         print(data)				# print string
 
# except KeyboardInterrupt:
# 	ser.close()
#!/usr/bin/python3
 
# import time
# import serial
 
# ser = serial.Serial(
# 	port = '/dev/ttyAMA0',
# 	baudrate = 9600,
# 	parity = serial.PARITY_NONE,
# 	stopbits = serial.STOPBITS_ONE,
# 	bytesize = serial.EIGHTBITS,
# 	timeout = 1
# )
 
# print("Raspberry's sending : ")
 
# try:
#     while True:
#     	ser.write(b'hehe')
#     	ser.flush()
#     	print("hehe")
#     	time.sleep(1)
# except KeyboardInterrupt:
# 	ser.close()