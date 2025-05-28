import pygame
import serial
import time

# Hàm nhận và gửi tín hiệu xuồng stm32
def send_and_receive_data_from_Stm32(serialConnection,characterSend):
    serialConnection.write(characterSend.encode())
    print(f"da gui chu {characterSend}")
    serialConnection.flush()
    data_receive=serialConnection.read(1)
    print("chuoi",data_receive)
# hàm thực thi lệnh từ nút ấn
def thuc_hien_Button(serialConncection,numberButton):
    if numberButton== 3: # nút "X" :quay trái
        send_and_receive_data_from_Stm32(serialConncection,"G")
    elif numberButton==1: #nut "B" : quay phải
        send_and_receive_data_from_Stm32(serialConncection,"F")
    elif numberButton==4: # nut Y: quay con lăn thuận chiều kim đồng hồ
        send_and_receive_data_from_Stm32(serialConncection,"M") 
    elif numberButton==0:# nút "A": quay con lăn nghịch
        send_and_receive_data_from_Stm32(serialConncection,"N")
    elif numberButton==10: # nút "select": bắn bóng
        send_and_receive_data_from_Stm32(serialConncection,"X")
# hàm thực hiện lệnh từ D_pad trên gamepad
def thuc_hien_D_Pad(serialConncection,toaDo_Tuple):
    if toaDo_Tuple==(1,0): #sang phải
        send_and_receive_data_from_Stm32(serialConncection,"D")
    elif toaDo_Tuple==(-1,0): #sang trái
        send_and_receive_data_from_Stm32(serialConncection,"A")
    elif toaDo_Tuple==(0,1): # tiến
        send_and_receive_data_from_Stm32(serialConncection,"W")
    elif toaDo_Tuple==(0,-1): #lùi
        send_and_receive_data_from_Stm32(serialConncection,"S")
# Hàm thực hiện lệnh từ axes
def thuc_hien_Axes(serialConncection,x_axis,y_axis):
    if x_axis==1 and y_axis==0: #sang phải
        send_and_receive_data_from_Stm32(serialConncection,"D")
    elif x_axis==-1 and y_axis==0:#sang trái
        send_and_receive_data_from_Stm32(serialConncection,"A")
    elif x_axis==0 and y_axis==1:#đi thẳng
        send_and_receive_data_from_Stm32(serialConncection,"W")
    elif x_axis==0 and y_axis==-1:#đi lùi
        send_and_receive_data_from_Stm32(serialConncection,"S")
    elif (x_axis>0.0 and x_axis<=1.0 and y_axis>0.0 and y_axis<=1.0): #đi chéo phải tiến
        send_and_receive_data_from_Stm32(serialConncection,"E")
    elif x_axis>0.01 and x_axis<=1.0 and y_axis>=-1.0 and y_axis<0.0:#Đi chéo trái lùi
        send_and_receive_data_from_Stm32(serialConncection,"C")
    elif x_axis>=-1.0 and x_axis<0.0 and y_axis>0.0 and y_axis<=1.0:# đi chéo trái tiến
        send_and_receive_data_from_Stm32(serialConncection,"Q")
    elif x_axis>=-1.0 and x_axis<0.0 and y_axis>=-1.0 and y_axis<0.0:# đi chéo phải lùi
        send_and_receive_data_from_Stm32(serialConncection,"Z")


#khởi tạo kết nối
ser = serial.Serial(
        port='/dev/ttyS0',  # Hoặc /dev/ttyS0 nếu sử dụng UART mini
        baudrate=9600,        # Tốc độ baud, phải khớp với STM32
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1             # Thời gian chờ nhận dữ liệu (giây)
    )
    
    # Kiểm tra kết nối
if ser.isOpen():
    print("UART kết nối thành công!")

# Khởi tạo Pygame và gamepad
pygame.init()
pygame.joystick.init()

# Kết nối gamepad
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Kết nối với: {joystick.get_name()}")

# Vòng lặp chính
while (1):
    #thoát pygame
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            pass
    #kiểm tra nút ấn 
    for _indexBut in range (joystick.get_numbuttons()):
        if joystick.get_button(_indexBut)==1:
            thuc_hien_Button(ser,_indexBut)
            print(f"Nút {_indexBut} được nhấn")
            pygame.time.wait(100)
    #Kiểm tra D_Pad
    for _indexHat in range(joystick.get_numhats()):
        if joystick.get_hat(_indexHat) !=(0,0):
            thuc_hien_D_Pad(serialConncection=ser,toaDo_Tuple=joystick.get_hat(_indexHat))
            print(f"Nút {joystick.get_hat(_indexHat)} được nhấn")
            pygame.time.wait(100)
    # # Di chuyển bằng joystick
    if joystick:
        x_axis = round(joystick.get_axis(0),4)  # Cần trái trục X
        y_axis = -round(joystick.get_axis(1),4)  # Cần trái trục Y
        if x_axis or y_axis:
            thuc_hien_Axes(ser,x_axis=x_axis,y_axis=y_axis)
            print ("vi tri truc x,y: ",x_axis,-y_axis)
            pygame.time.wait(100)
        
# Thoát
pygame.quit()
