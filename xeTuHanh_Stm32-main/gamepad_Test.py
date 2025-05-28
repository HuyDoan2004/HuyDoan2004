# import pygame
# import sys

# # Khởi tạo Pygame
# pygame.init()

# # Thiết lập màn hình
# screen = pygame.display.set_mode((640, 480))
# pygame.display.set_caption("Gamepad Example")

# # Màu sắc
# WHITE = (255, 255, 255)
# BLUE = (0, 0, 255)

# # Vị trí ban đầu của hình chữ nhật
# x, y = 320, 240
# speed = 5

# # Khởi tạo joystick
# pygame.joystick.init()
# if pygame.joystick.get_count() > 0:
#     joystick = pygame.joystick.Joystick(0)
#     joystick.init()
#     print("Tên bộ điều khiển:", joystick.get_name())
# else:
#     joystick = None
#     print("Không tìm thấy bộ điều khiển.")

# clock = pygame.time.Clock()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     # Xử lý đầu vào từ bộ điều khiển
#     if joystick:
#         axis_x = joystick.get_axis(0)  # Trục X
#         axis_y = joystick.get_axis(1)  # Trục Y

#         # Cập nhật vị trí dựa trên trục
#         x += int(axis_x * speed)
#         y += int(axis_y * speed)

#     # Giới hạn vị trí trong màn hình
#     x = max(0, min(x, 640))
#     y = max(0, min(y, 480))

#     # Vẽ lên màn hình
#     screen.fill(WHITE)
#     pygame.draw.rect(screen, BLUE, (x, y, 50, 50))
#     pygame.display.flip()

#     clock.tick(60)  # Giới hạn 60 FPS

# Example file showing a basic pygame "game loop"
# import pygame

# # pygame setup
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True

# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # fill the screen with a color to wipe away anything from last frame
#     screen.fill("purple")

#     # RENDER YOUR GAME HERE

#     # flip() the display to put your work on screen
#     pygame.display.flip()

#     clock.tick(60)  # limits FPS to 60

# pygame.quit()
# import pygame

# # Khởi tạo Pygame và gamepad
# pygame.init()
# pygame.joystick.init()

# # Màn hình
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Điều khiển bằng gamepad")

# # Màu sắc
# white = (255, 255, 255)
# blue = (0, 0, 255)

# # Tạo hình vuông
# square_pos = [400, 300]  # Vị trí ban đầu
# speed = 5

# # Kết nối gamepad
# joystick = None
# if pygame.joystick.get_count() > 0:
#     joystick = pygame.joystick.Joystick(0)
#     joystick.init()
#     print(f"Kết nối với: {joystick.get_name()}")

# # Vòng lặp chính
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.JOYBUTTONDOWN:
#             print(f"Nút {event.button} được nhấn")
#         elif event.type == pygame.JOYHATMOTION:
#             hat = joystick.get_hat(0)
#             print(f"D-Pad: {hat}")
    
#     # Di chuyển bằng joystick
#     if joystick:
#         x_axis = joystick.get_axis(0)  # Cần trái trục X
#         y_axis = joystick.get_axis(1)  # Cần trái trục Y
#         square_pos[0] += int(x_axis * speed)
#         square_pos[1] += int(y_axis * speed)
#         if x_axis or y_axis:
#             print ("vi tri truc x: ",round(x_axis,4))
#             print ("vi tri truc y: ", round(y_axis,4))

#     # Giới hạn hình vuông trong màn hình
#     square_pos[0] = max(0, min(800 - 50, square_pos[0]))
#     square_pos[1] = max(0, min(600 - 50, square_pos[1]))

#     # Vẽ
#     screen.fill(white)
#     pygame.draw.rect(screen, blue, (*square_pos, 50, 50))  # Hình vuông 50x50
#     pygame.display.flip()

# # Thoát
# pygame.quit()
import pygame
import time

# Khởi tạo Pygame
pygame.init()
pygame.joystick.init()

# Kiểm tra và kết nối gamepad
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("Không có gamepad nào được kết nối.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Đã kết nối với gamepad: {joystick.get_name()}")

# Vòng lặp đọc dữ liệu
try:
    while True:
        pygame.joystick.Joystick(0).init()

        # Đọc giá trị của các trục (axis)
        axis_count = joystick.get_numaxes()
        for i in range(axis_count):
            value = joystick.get_axis(i)
            print(f"Trục {i}: {value}")

        # Đọc trạng thái nút (button)
        button_count = joystick.get_numbuttons()
        for i in range(button_count):
            state = joystick.get_button(i)
            print(f"Nút {i}: {state}")

        # Đọc trạng thái D-Pad (hat)
        hat_count = joystick.get_numhats()
        for i in range(hat_count):
            position = joystick.get_hat(i)
            print(f"D-Pad {i}: {position}")

        time.sleep(0.1)  # Thêm độ trễ để dễ đọc hơn

except KeyboardInterrupt:
    print("\nKết thúc chương trình")

finally:
    pygame.joystick.quit()
    pygame.quit()
