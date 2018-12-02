#!/usr/bin/env python3
import argparse
import time
import sys
# import rclpy
# from rclpy.node import Node
#
# from diagnostic_msgs.msg import DiagnosticStatus
#
#
# class Participant(Node):
#
#     def __init__(self, time_to_live=0):
#         super().__init__('minimal_publisher')
#         self.publisher_ = self.create_publisher(String, 'topic')
#         timer_period = 0.5  # seconds
#         self.timer = self.create_timer(timer_period, self.timer_callback)
#         self.i = 0
#
#     def timer_callback(self):
#         msg = String()
#         msg.data = 'Hello World: %d' % self.i
#         self.publisher_.publish(msg)
#         self.get_logger().info('Publishing: "%s"' % msg.data)
#         self.i += 1
#
#
# def main(argv=sys.argv[1:]):
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--ttl', required=True, type=int)
#     args, argv = parser.parse_known_args(argv)
#     rclpy.init(args=argv)
#
#     participant = Participant(time_to_live=args.ttl)
#     rclpy.spin(participant)
#     participant.destroy_node()
#     rclpy.shutdown()


if __name__ == '__main__':
    print('sys.argv[1:]: ', sys.argv[1:])
    time.sleep(30)
    # main()
