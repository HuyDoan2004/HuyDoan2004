import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import RPi.GPIO as GPIO
import time
import math

class UltrasonicSensorNode(Node):
    def __init__(self):
        super().__init__('ultrasonic_sensor_node')

        self.trig_pin = 27
        self.echo_pin = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        self.publisher = self.create_publisher(LaserScan, 'scan', 10)
        self.timer = self.create_timer(0.5, self.publish_scan)

        self.angle_min = -math.pi / 4  # -45 degrees
        self.angle_max = math.pi / 4   # +45 degrees
        self.angle_increment = math.pi / 18  # 10 degrees step
        self.range_max = 3.5  # max 3.5m ultrasonic sensor range
        self.range_min = 0.02

    def get_distance(self):
        GPIO.output(self.trig_pin, False)
        time.sleep(0.05)

        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        pulse_start = None
        pulse_end = None
        timeout = time.time() + 0.04

        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return None
        if pulse_start is None:
            return None

        timeout = time.time() + 0.04
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return None
        if pulse_end is None:
            return None

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150 / 100  # convert to meters
        return distance

    def publish_scan(self):
        scan = LaserScan()
        scan.header.stamp = self.get_clock().now().to_msg()
        scan.header.frame_id = 'laser_frame'

        scan.angle_min = self.angle_min
        scan.angle_max = self.angle_max
        scan.angle_increment = self.angle_increment
        scan.time_increment = 0.0
        scan.scan_time = 0.5
        scan.range_min = self.range_min
        scan.range_max = self.range_max

        ranges = []
        steps = int((self.angle_max - self.angle_min) / self.angle_increment) + 1
        for _ in range(steps):
            d = self.get_distance()
            if d is None or d < self.range_min or d > self.range_max:
                ranges.append(float('inf'))
            else:
                ranges.append(d)
        scan.ranges = ranges

        self.publisher.publish(scan)
        self.get_logger().info(f"Published scan ranges: {ranges}")

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicSensorNode()
    rclpy.spin(node)
    node.destroy_node()
    GPIO.cleanup()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
