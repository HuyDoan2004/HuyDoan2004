import rclpy
from rclpy.node import Node
import serial
import serial.serialutil

class UARTControlNode(Node):
    def __init__(self):
        super().__init__('uart_control_node')
        try:
            self.ser = serial.Serial(
                port='/dev/ttyS0',
                baudrate=9600,
                timeout=0.1
            )
            self.get_logger().info("UART connected successfully.")
        except serial.serialutil.SerialException as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            self.ser = None

        if self.ser and self.ser.is_open:
            # Tạo timer gửi lệnh F mỗi 1ms = 0.001s => 1000Hz
            self.timer = self.create_timer(0.001, self.timer_callback)
        else:
            self.get_logger().error("Serial port not open, timer not started.")

    def timer_callback(self):
        if not self.ser or not self.ser.is_open:
            self.get_logger().error("Serial port is not open.")
            return
        try:
            cmd = 'F\n'
            self.ser.write(cmd.encode())
            # Bạn có thể comment dòng dưới để giảm log, vì quá nhiều log gây lag
            # self.get_logger().info(f"Sent command: {cmd.strip()}")
            
            # Nếu thiết bị trả về phản hồi, đọc phản hồi:
            # response = self.ser.readline().decode('utf-8').strip()
            # if response:
            #     self.get_logger().info(f"Received: {response}")
        except Exception as e:
            self.get_logger().error(f"UART error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = UARTControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.ser and node.ser.is_open:
            node.ser.close()
            node.get_logger().info("Serial port closed.")
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
