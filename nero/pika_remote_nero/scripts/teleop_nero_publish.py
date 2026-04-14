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
from data_msgs.msg import TeleopStatus
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
        self.pika_pose_initial = None   # [x, y, z, roll, pitch, yaw] - pika 初始位姿
        self.arm_pose_initial = None    # [x, y, z, roll, pitch, yaw] - 臂末端初始位姿
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
        # 提取当前位置（base_link 系）
        x = msg.pose.position.x
        y = msg.pose.position.y
        z = msg.pose.position.z
        roll, pitch, yaw = euler_from_quaternion((
            msg.pose.orientation.x, msg.pose.orientation.y,
            msg.pose.orientation.z, msg.pose.orientation.w
        ))
        
        # 标定初始位姿
        if self.refresh_localization_pose:
            self.refresh_localization_pose = False
            self.pika_pose_initial = [x, y, z, roll, pitch, yaw]
            self.get_logger().info("标定 pika 初始位姿完成")
        
        # 需要臂初始位姿和遥操作状态才能计算
        if self.arm_pose_initial is not None and self.status:
            # 计算欧拉角差值（相对运动）
            # 根据测试结果修正轴方向：
            # X（前后）、Y（左右）、绕X、绕Y 需要取反
            dx = -(x - self.pika_pose_initial[0])   # X轴：向前推臂向右 -> 取反
            dy = -(y - self.pika_pose_initial[1])   # Y轴：向右推臂向后 -> 取反
            dz = z - self.pika_pose_initial[2]      # Z轴：正常
            droll = -(roll - self.pika_pose_initial[3])  # 绕X：反的 -> 取反
            dpitch = -(pitch - self.pika_pose_initial[4])  # 绕Y：反的 -> 取反
            dyaw = yaw - self.pika_pose_initial[5]  # 绕Z：正常
            
            # 直接加到初始臂位姿上
            pose_xyzrpy = [
                self.arm_pose_initial[0] + dx*0.5,
                self.arm_pose_initial[1] + dy*0.5,
                self.arm_pose_initial[2] + dz*0.5,
                self.arm_pose_initial[3] + droll*0.5,
                self.arm_pose_initial[4] + dpitch*0.5,
                self.arm_pose_initial[5] + dyaw*0.5
            ]
            
            pose_msg = PoseStamped()
            pose_msg.header = Header()
            pose_msg.header.frame_id = "map"
            pose_msg.header.stamp = self.get_clock().now().to_msg()
            pose_msg.pose.position.x = pose_xyzrpy[0]
            pose_msg.pose.position.y = pose_xyzrpy[1]
            pose_msg.pose.position.z = pose_xyzrpy[2]
            q = quaternion_from_euler(pose_xyzrpy[3], pose_xyzrpy[4], pose_xyzrpy[5])
            pose_msg.pose.orientation.x = q[0]
            pose_msg.pose.orientation.y = q[1]
            pose_msg.pose.orientation.z = q[2]
            pose_msg.pose.orientation.w = q[3]
            self.arm_end_pose_ctrl_publisher.publish(pose_msg)
            status_msg = TeleopStatus()
            status_msg.quit = False
            status_msg.fail = False
            self.teleop_status_publisher.publish(status_msg)

    def arm_end_pose_callback(self, msg):
        # 存储初始位姿为欧拉角格式
        x = msg.pose.position.x
        y = msg.pose.position.y
        z = msg.pose.position.z
        roll, pitch, yaw = euler_from_quaternion((
            msg.pose.orientation.x, msg.pose.orientation.y,
            msg.pose.orientation.z, msg.pose.orientation.w
        ))
        if self.refresh_arm_end_pose:
            self.refresh_arm_end_pose = False
            self.arm_pose_initial = [x, y, z, roll, pitch, yaw]

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
                print("start")
                self.status = True
                break
            else:
                status_msg = TeleopStatus()
                status_msg.quit = False
                status_msg.fail = True
                print("wait")
                self.teleop_status_publisher.publish(status_msg)
            time.sleep(0.1)

    def teleop_trigger_callback(self, request, response):
        if self.status:
            self.status = False
            status_msg = TeleopStatus()
            status_msg.quit = True
            status_msg.fail = False
            self.teleop_status_publisher.publish(status_msg)
            print("close")
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
                status_msg = TeleopStatus()
                status_msg.quit = True
                status_msg.fail = False
                self.teleop_status_publisher.publish(status_msg)
                print("close")
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
        
        # 遥操作状态发布器
        self.teleop_status_publisher = self.create_publisher(
            TeleopStatus,
            f'/teleop_status{self.args.index_name}',
            1
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
            f'/joint_states_gripper{self.args.index_name}',
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
        if self.args.return_zero_position == "True":
            # 目标关节位置
            target_joint_state = [-0.000925,1.665288,1.5,0.001798,0.000122,0.000000,0.000140]
            
            # 获取当前关节位置
            # 如果已经接收到关节位置数据，使用实际的当前位置
            # 否则会一步调整到位
            if self.joint_positions_received:
                current_positions = self.current_joint_positions
                
                # 设置过渡时间和控制频率
                duration = 0.5  # 过渡持续时间(秒)
                rate = 30  # 控制频率(Hz)
                
                # 计算总步数
                steps = int(duration * rate)
                
                # 计算每一步的增量
                increments = [(target - current) / steps for current, target in zip(current_positions, target_joint_state)]
                
                # 创建ROS2的Rate对象控制循环频率
                rate_obj = self.create_rate(rate)
                
                # 记录开始时间（用于日志）
                start_time = self.get_clock().now()
                
                # 逐步移动到目标位置
                for step in range(steps + 1):
                    # 计算当前步骤的位置
                    interpolated_positions = [current + increment * step for current, increment in zip(current_positions, increments)]
                    
                    # 发布关节状态消息
                    joint_states_msgs = JointState()
                    joint_states_msgs.header = Header()
                    joint_states_msgs.header.stamp = self.get_clock().now()
                    joint_states_msgs.name = [f'joint{i+1}{self.args.index_name}' for i in range(7)]
                    joint_states_msgs.position = interpolated_positions
                    
                    # 发布消息
                    self.arm_joint_state_publisher.publish(joint_states_msgs)
                    
                    # 按照指定频率控制循环
                    rate_obj.sleep()
                
                # 确保最后一帧是精确的目标位置
                joint_states_msgs = JointState()
                joint_states_msgs.header = Header()
                joint_states_msgs.header.stamp = self.get_clock().now()
                joint_states_msgs.name = [f'joint{i+1}{self.args.index_name}' for i in range(7)]
                joint_states_msgs.position = target_joint_state
                self.arm_joint_state_publisher.publish(joint_states_msgs)
                
                # 计算实际用时
                elapsed_time = (self.get_clock().now() - start_time).to_sec()
                
            else:
                start_time = self.get_clock().now()  # 获取当前时间
                while (self.get_clock().now() - start_time).to_sec() < 0.5:  # 持续发送0.5秒
                    joint_states_msgs = JointState()
                    joint_states_msgs.header = Header()
                    joint_states_msgs.header.stamp = self.get_clock().now()
                    joint_states_msgs.name = [f'joint{i+1}{self.args.index_name}' for i in range(7)]
                    joint_states_msgs.position = target_joint_state
                    self.arm_joint_state_publisher.publish(joint_states_msgs)
        else:
            return


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