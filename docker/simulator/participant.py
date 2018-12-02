#!/usr/bin/env python3
import argparse
import os
import time
import sys


from diagnostic_msgs.msg import DiagnosticStatus

import rclpy
from rclpy.node import Node


class Participant(Node):

    def __init__(self, time_to_live=0):
        self.count = 0
        self.time_to_live = time_to_live

        super().__init__('participant')
        self.name = self.get_namespace() + '/' + self.get_name()
        self.publisher_ = self.create_publisher(DiagnosticStatus, '/topic')
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = DiagnosticStatus()
        msg.level = DiagnosticStatus.OK
        msg.name = os.path.join(self.get_namespace(), self.get_name())
        msg.message = '%d' % self.count
        msg.hardware_id = '%d' % self.time_to_live
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.message)
        self.count += 1


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--ttl', required=True, type=int)
    args, argv = parser.parse_known_args(argv)
    rclpy.init(args=argv)

    participant = Participant(time_to_live=args.ttl)
    rclpy.spin(participant)
    participant.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    # print('sys.argv[1:]: ', sys.argv[1:])
    # time.sleep(30)
    main()
