import rclpy
from rclpy.node import Node
import serial

class UARTControlNode(Node):
    def __init__(self):
        super().__init__('uart_control_node')
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            timeout=1
        )
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        try:
            cmd = 'F'
            self.ser.write(cmd.encode())
            self.get_logger().info(f"Sent command: {cmd}")
            response = self.ser.readline().decode('utf-8').strip()
            if response:
                self.get_logger().info(f"Received: {response}")
        except Exception as e:
            self.get_logger().error(f"UART error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = UARTControlNode()
    rclpy.spin(node)
    node.ser.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
