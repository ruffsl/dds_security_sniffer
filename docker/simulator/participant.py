#!/usr/bin/env python3
import argparse
import datetime
import os
import time
import sys


from diagnostic_msgs.msg import DiagnosticStatus, KeyValue

import rclpy
from rclpy.node import Node


class Participant(Node):

    def __init__(self, time_to_live=0):
        self.count = 0
        self.time_to_live = time_to_live

        super().__init__('participant')
        self.name = os.path.join(self.get_namespace(), self.get_name())
        self.publisher_= self.create_publisher(
            DiagnosticStatus, '/topic')
        self.subscription = self.create_subscription(
            DiagnosticStatus, '/topic', self.listener_callback)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = DiagnosticStatus()
        msg.level = DiagnosticStatus.OK
        msg.name = self.name
        msg.message = '%d' % self.count
        msg.hardware_id = '%d' % self.time_to_live
        key_value = KeyValue(
            key=self.name,
            value=datetime.datetime.utcnow().isoformat())
        msg.values = [key_value]
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: %s' % msg.message)
        self.count += 1

    def listener_callback(self, msg):
        ttl = int(msg.hardware_id)
        keys = [key_value.key for key_value in msg.values]
        if self.name in keys:
            return
        else:
            if ttl >= 0:
                self.get_logger().info('Received: %s' % ' ,'.join(keys))
            if ttl > 0:
                msg.hardware_id = '%d' % (ttl - 1)
                key_value = KeyValue(
                    key=self.name,
                    value=datetime.datetime.utcnow().isoformat())
                msg.values.append(key_value)
                self.publisher_.publish(msg)


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
