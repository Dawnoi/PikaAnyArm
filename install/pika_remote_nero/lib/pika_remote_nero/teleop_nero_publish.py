#!/usr/bin/env python3
"""
Nero Teleoperation Publish Node
订阅主设备位姿，发布到 IK 控制器进行遥操作
"""

import math
import numpy as np
from transformations import quaternion_from_euler, euler_from_quaternion, quaternion_from_matrix
import os
import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header
import argparse
from nav_msgs.msg import Odometry
import threading
from std_srvs.srv import Trigger
import time
from sensor_msgs.msg import JointState


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

os.environ['MKL_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'


def matrix_to_xyzrpy(matrix):
    x = matrix[0, 3]
    y = matrix[1, 3]
    z = matrix[2, 3]
    roll = math.atan2(matrix[2, 1], matrix[2, 2])
    pitch = math.asin(-matrix[2, 0])
    yaw = math.atan2(matrix[1, 0], matrix[0, 0])
    return [x, y, z, roll, pitch, yaw]


def create_transformation_matrix(x, y, z, roll, pitch, yaw):
    transformation_matrix = np.eye(4)
    A = np.cos(yaw)
    B = np.sin(yaw)
    C = np.cos(pitch)
    D = np.sin(pitch)
    E = np.cos(roll)
    F = np.sin(roll)
    DE = D * E
    DF = D * F
    transformation_matrix[0, 0] = A * C
    transformation_matrix[0, 1] = A * DF - B * E
    transformation_matrix[0, 2] = B * F + A * DE
    transformation_matrix[0, 3] = x
    transformation_matrix[1, 0] = B * C
    transformation_matrix[1, 1] = A * E + B * DF
    transformation_matrix[1, 2] = B * DE - A * F
    transformation_matrix[1, 3] = y
    transformation_matrix[2, 0] = -D
    transformation_matrix[2, 1] = C * F
    transformation_matrix[2, 2] = C * E
    transformation_matrix[2, 3] = z
    transformation_matrix[3, 0] = 0
    transformation_matrix[3, 1] = 0
    transformation_matrix[3, 2] = 0
    transformation_matrix[3, 3] = 1
    return transformation_matrix


class RosOperator(Node):
    def __init__(self, args):
        super().__init__('teleop_nero_publisher')
        self.args = args
        self.localization_pose_subscriber = None
        self.arm_end_pose_subscriber = None
        self.arm_end_pose_ctrl_publisher = None
        self.localization_pose_matrix = None
        self.arm_end_pose_matrix = None
        self.refresh_localization_pose = True
        self.refresh_arm_end_pose = True
        self.thread = None
        self.stop_thread = False
        self.status_srv = None
        self.status = False
        
        # 存储当前关节位置
        self.current_joint_positions = [0.0] * 7  # Nero 有 7 个关节
        self.joint_positions_received = False
        
        self.init_ros()

    def localization_pose_callback(self, msg):
        roll, pitch, yaw = euler_from_quaternion((msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w))
        matrix = create_transformation_matrix(msg.pose.position.x, msg.pose.position.y, msg.pose.position.z, roll, pitch, yaw)
        if self.refresh_localization_pose:
            self.refresh_localization_pose = False
            self.localization_pose_matrix = matrix
        if self.arm_end_pose_matrix is not None and self.status:
            pose_xyzrpy = matrix_to_xyzrpy(np.dot(self.arm_end_pose_matrix, np.dot(np.linalg.inv(self.localization_pose_matrix), matrix)))
            pose_msg = PoseStamped()
            pose_msg.header = Header()
            pose_msg.header.frame_id = "map"
            pose_msg.header.stamp = self.get_clock().now().to_msg()
            pose_msg.pose.position.x = pose_xyzrpy[0]
            pose_msg.pose.position.y = pose_xyzrpy[1]
            pose_msg.pose.position.z = pose_xyzrpy[2]
            q = quaternion_from_euler(pose_xyzrpy[3], pose_xyzrpy[4], pose_xyzrpy[5])
            pose_msg.pose.orientation.x = pose_xyzrpy[3]
            pose_msg.pose.orientation.y = pose_xyzrpy[4]
            pose_msg.pose.orientation.z = pose_xyzrpy[5]
            pose_msg.pose.orientation.w = 0.0
            self.arm_end_pose_ctrl_publisher.publish(pose_msg)

    def arm_end_pose_callback(self, msg):
        roll, pitch, yaw = euler_from_quaternion((msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w))
        matrix = create_transformation_matrix(msg.pose.position.x, msg.pose.position.y, msg.pose.position.z, roll, pitch, yaw)
        if self.refresh_arm_end_pose:
            self.refresh_arm_end_pose = False
            self.arm_end_pose_matrix = matrix

    def status_changing(self):
        self.refresh_localization_pose = True
        self.refresh_arm_end_pose = True
        while rclpy.ok():
            if self.stop_thread:
                self.status = False
                self.refresh_localization_pose = False
                self.refresh_arm_end_pose = False
                break
            if not self.refresh_localization_pose and not self.refresh_arm_end_pose:
                print("遥操作开始")
                self.status = True
                break
            else:
                print("等待数据同步...")
            time.sleep(0.1)

    def teleop_trigger_callback(self, request, response):
        if self.status:
            self.status = False
            print("遥操作停止")
            self.init_pose()
        else:
            if self.thread is None or not self.thread.is_alive():
                self.stop_thread = False
                self.thread = threading.Thread(target=self.status_changing)
                self.thread.start()
            else:
                self.stop_thread = True
                self.thread.join()
                self.status = False
                print("遥操作停止")
                self.init_pose()
        return response

    def init_ros(self):
        self.declare_parameter('index_name', "")
        self.args.index_name = self.get_parameter('index_name').get_parameter_value().string_value
        
        # 订阅主设备位姿
        self.localization_pose_subscriber = self.create_subscription(
            PoseStamped, 
            f'/pika_pose{self.args.index_name}', 
            self.localization_pose_callback, 
            1
        )
        
        # 订阅机械臂 FK 结果
        self.arm_end_pose_subscriber = self.create_subscription(
            PoseStamped, 
            f'/nero_FK{self.args.index_name}/urdf_end_pose_orient', 
            self.arm_end_pose_callback, 
            1
        )
        
        # 发布控制末端位姿到 IK
        self.arm_end_pose_ctrl_publisher = self.create_publisher(
            PoseStamped, 
            f'/nero_IK{self.args.index_name}/ctrl_end_pose', 
            1
        )
        
        # 遥操作触发服务
        self.status_srv = self.create_service(
            Trigger, 
            f'/teleop_trigger{self.args.index_name}', 
            self.teleop_trigger_callback
        )
        
        # 发布关节状态
        self.arm_joint_state_publisher = self.create_publisher(
            JointState,
            f'/joint_states{self.args.index_name}',
            1
        )
        
        # 订阅关节状态（来自 relay 节点的转换后的关节状态）
        self.create_subscription(
            JointState,
            f'/joint_states{self.args.index_name}',
            self.joint_states_callback,
            1
        )
        
        time.sleep(0.5)
        self.init_pose()

    def joint_states_callback(self, msg):
        """处理从 joint_states_single 话题接收到的关节状态数据"""
        if len(msg.position) >= 7:
            self.current_joint_positions = list(msg.position[:7])
            self.joint_positions_received = True

    def init_pose(self):
        """使用线性插值实现平滑过渡到初始位置"""
        if hasattr(self.args, 'return_zero_position') and self.args.return_zero_position == "True":
            target_joint_state = [0.0] * 7
            
            if self.joint_positions_received:
                current_positions = self.current_joint_positions
                duration = 0.5
                rate = 50
                steps = int(duration * rate)
                increments = [(target - current) / steps for current, target in zip(current_positions, target_joint_state)]
                
                rate_obj = self.create_rate(rate)
                start_time = self.get_clock().now()
                
                for step in range(steps + 1):
                    interpolated_positions = [current + increment * step for current, increment in zip(current_positions, increments)]
                    
                    joint_states_msgs = JointState()
                    joint_states_msgs.header = Header()
                    joint_states_msgs.header.stamp = self.get_clock().now()
                    joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
                    joint_states_msgs.position = interpolated_positions
                    
                    self.arm_joint_state_publisher.publish(joint_states_msgs)
                    rate_obj.sleep()
                
                elapsed_time = (self.get_clock().now() - start_time).to_sec()
            else:
                start_time = self.get_clock().now()
                while (self.get_clock().now() - start_time).to_sec() < 0.5:
                    joint_states_msgs = JointState()
                    joint_states_msgs.header = Header()
                    joint_states_msgs.header.stamp = self.get_clock().now()
                    joint_states_msgs.name = [f'joint{i+1}' for i in range(7)]
                    joint_states_msgs.position = target_joint_state
                    self.arm_joint_state_publisher.publish(joint_states_msgs)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--index_name', action='store', type=str, help='index_name',
                        default="", required=False)
    parser.add_argument('--return_zero_position', action='store', type=str, help='return_zero_position',
                        default="False", required=False)
    args, unknown = parser.parse_known_args()
    return args


def main():
    args = get_arguments()
    rclpy.init()
    ros_operator = RosOperator(args)
    rclpy.spin(ros_operator)


if __name__ == "__main__":
    main()