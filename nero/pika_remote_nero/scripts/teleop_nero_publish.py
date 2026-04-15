#!/usr/bin/env python3
"""
Nero Teleoperation Publish Node
订阅主设备位姿，发布到 IK 控制器进行遥操作
支持夹爪控制：订阅遥操夹爪角度话题，发布夹爪命令到 joint_ctrl_single
注意：实际的夹爪控制由 nero_ctrl_single_node 执行，避免创建重复连接
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
from data_msgs.msg import TeleopStatus, Gripper
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
        
        # 夹爪控制相关
        self.left_gripper_initial = None  # 左夹爪初始角度
        self.right_gripper_initial = None  # 右夹爪初始角度
        self.gripper_l_subscriber = None
        self.gripper_r_subscriber = None
        self.gripper_cmd_publisher = None  # 夹爪命令发布者
        
        # AGX_GRIPPER 夹爪控制参数
        # 遥操夹爪角度范围: 0 ~ 1.67 rad（完全张开到完全闭合，对应 enable=true）
        # AGX_GRIPPER 夹爪宽度范围: 0.0 ~ 0.1 m（完全闭合到完全张开）
        # 映射关系: 遥操角度越小，AGX_GRIPPER 宽度越大（夹爪张开）
        self.GRIPPER_ANGLE_MAX = 1.67  # 遥操夹爪最大角度 (rad)
        self.GRIPPER_WIDTH_MAX = 0.1   # AGX_GRIPPER 最大宽度 (m)
        
        self.init_ros()
        self.init_gripper()

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
                self.get_logger().info(f"标定 pika {self.args.index_name} 初始位姿完成")
            
            # 需要臂初始位姿和遥操作状态才能计算
            if self.arm_pose_initial is not None and self.status:
                # 1. 计算主设备端最原始的相对位移 (Raw Delta)
                raw_dx = x - self.pika_pose_initial[0]
                raw_dy = y - self.pika_pose_initial[1]
                raw_dz = z - self.pika_pose_initial[2]
                raw_droll = roll - self.pika_pose_initial[3]
                raw_dpitch = pitch - self.pika_pose_initial[4]
                raw_dyaw = yaw - self.pika_pose_initial[5]
                
                # 2. 根据左右臂区分坐标系映射 (Coordinate Mapping)
                # 注意：由于两个遥操设备 TF 相同，旋转映射左右臂一致
                if self.args.index_name == '_r':
                    # 【右臂逻辑】: 基座位置镜像 (y 取反)
                    # 位置映射：dx=-dy, dy=dx
                    mapped_dx = -raw_dy
                    mapped_dy = raw_dx
                    mapped_dz = raw_dz
                    # 旋转映射：与左臂相同（TF 相同）
                    mapped_droll = -raw_droll
                    mapped_dpitch = -raw_dpitch
                    mapped_dyaw = raw_dyaw
                    
                elif self.args.index_name == '_l':
                    # 【左臂逻辑】: 基座位置镜像 (x 取反)
                    # 位置映射：dx=dy, dy=-dx
                    mapped_dx = raw_dy
                    mapped_dy = -raw_dx
                    mapped_dz = raw_dz
                    # 旋转映射：与右臂相同（TF 相同）
                    mapped_droll = -raw_droll
                    mapped_dpitch = -raw_dpitch
                    mapped_dyaw = raw_dyaw
                    
                else:
                    # 默认后备逻辑
                    mapped_dx = -raw_dx
                    mapped_dy = -raw_dy
                    mapped_dz = raw_dz
                    mapped_droll = -raw_droll
                    mapped_dpitch = -raw_dpitch
                    mapped_dyaw = raw_dyaw
                
                # 3. 直接加到初始臂位姿上
                pose_xyzrpy = [
                    self.arm_pose_initial[0] + mapped_dx,
                    self.arm_pose_initial[1] + mapped_dy,
                    self.arm_pose_initial[2] + mapped_dz,
                    self.arm_pose_initial[3] + mapped_droll,
                    self.arm_pose_initial[4] + mapped_dpitch,
                    self.arm_pose_initial[5] + mapped_dyaw
                ]
                # 组装并发布 PoseStamped
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
        # 存储初始位姿为欧拉角格式（使用 ZYX 顺序，与 localization_pose_callback 一致）
        x = msg.pose.position.x
        y = msg.pose.position.y
        z = msg.pose.position.z
        roll, pitch, yaw = euler_from_quaternion((
            msg.pose.orientation.x, msg.pose.orientation.y,
            msg.pose.orientation.z, msg.pose.orientation.w
        ), 'szyx')[::-1]  # 返回 [yaw, pitch, roll]，反转得 [roll, pitch, yaw]

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
        self.declare_parameter('return_zero_position', "False")
        self.declare_parameter('gripper_control', True)
        self.declare_parameter('can_channel', "can0")
        self.args.return_zero_position = self.get_parameter('return_zero_position').get_parameter_value().string_value
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
        
        # 订阅关节状态（来自 nero_ctrl_single_node 的真实关节角度）
        # /puppet/joint_{nero_name} 发布真实关节角度（来自 get_joint_angles）
        # /master/joint_{nero_name} 发布控制指令回显（遥操作时全零）
        nero_name = "left" if self.args.index_name == "_l" else "right"
        joint_topic = f'/puppet/joint_{nero_name}'
        self.create_subscription(
            JointState,
            joint_topic,
            self.joint_states_callback,
            1
        )
        self.get_logger().info(f"[DEBUG] Subscribed to joint topic: {joint_topic}")
        
        time.sleep(0.5)
        self.init_pose()

    def joint_states_callback(self, msg):
        """处理从 joint_states_single 话题接收到的关节状态数据"""
        if len(msg.position) >= 7:
            self.current_joint_positions = list(msg.position[:7])
            self.joint_positions_received = True
            self.get_logger().info(f"joint_states: {[f'{p:.3f}' for p in msg.position[:7]]}")

    def init_gripper(self):
        """初始化夹爪控制
        
        通过发布夹爪命令到 joint_ctrl_single 话题，让 nero_ctrl_single_node 执行控制
        注意：不创建新的机械臂连接，避免与 nero_ctrl_single_node 冲突
        """
        # 获取 gripper_control 参数
        gripper_control = self.get_parameter('gripper_control').get_parameter_value().bool_value
        if not gripper_control:
            self.get_logger().info("Gripper control is disabled")
            return
        
        # 创建夹爪命令发布者，发布到 joint_ctrl_single 话题
        # nero_ctrl_single_node 会接收并控制夹爪
        self.gripper_cmd_publisher = self.create_publisher(
            JointState,
            f'joint_ctrl_single',
            1
        )
        
        # 订阅遥操夹爪角度话题
        if self.args.index_name == '_l':
            self.gripper_l_subscriber = self.create_subscription(
                Gripper,
                '/gripper_l/data',
                self.gripper_l_callback,
                1
            )
        elif self.args.index_name == '_r':
            self.gripper_r_subscriber = self.create_subscription(
                Gripper,
                '/gripper_r/data',
                self.gripper_r_callback,
                1
            )
        
        # 设置默认夹爪状态（张开）
        # self._set_gripper_open()
        
        self.get_logger().info(f"Gripper control initialized for {self.args.index_name}")

    def gripper_l_callback(self, msg):
        """左夹爪角度回调
        
        话题消息格式（data_msgs/Gripper）:
        - angle: 夹爪角度 (rad), 范围 0~1.67
        - enable: 是否使能（true 表示有有效数据）
        
        映射逻辑:
        - 遥操夹爪 angle=0 表示完全张开 -> AGX_GRIPPER width=0.1m
        - 遥操夹爪 angle=1.67 表示完全闭合 -> AGX_GRIPPER width=0.0m
        """
        # TODO: 暂不发布夹爪命令，先观察关节位置数据
        # self.get_logger().info(f"[DEBUG] Gripper L callback: angle={msg.angle:.3f}, enable={msg.enable}")
        return
    
    def gripper_r_callback(self, msg):
        """右夹爪角度回调
        
        话题消息格式（data_msgs/Gripper）:
        - angle: 夹爪角度 (rad), 范围 0~1.67
        - enable: 是否使能（true 表示有有效数据）
        
        映射逻辑同上
        """
        # TODO: 暂不发布夹爪命令，先观察关节位置数据
        # self.get_logger().info(f"[DEBUG] Gripper R callback: angle={msg.angle:.3f}, enable={msg.enable}")
        return
    
    def _publish_gripper_cmd(self, gripper_width):
        """发布夹爪命令到 joint_ctrl_single 话题
        
        Args:
            gripper_width: 夹爪宽度 (m), 范围 0.0 ~ 0.1
        """
        cmd_msg = JointState()
        cmd_msg.header.stamp = self.get_clock().now().to_msg()
        cmd_msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7', 'gripper']

        cmd_msg.position = [-0.000925,1.665288,1.5,0.001798,0.000122,0.000000,0.000140] * 7 + [float(gripper_width)]
        cmd_msg.velocity = [0.0] * 8
        cmd_msg.effort = [0.0] * 8
        
        try:
            self.gripper_cmd_publisher.publish(cmd_msg)
        except Exception:
            pass  # 忽略发布错误
    
    def _set_gripper_open(self):
        """设置夹爪为张开状态
        
        默认将夹爪张开到最大宽度
        """
        if self.gripper_cmd_publisher is not None:
            self._publish_gripper_cmd(self.GRIPPER_WIDTH_MAX)
            self.get_logger().info("Gripper set to open position")
    
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
                rate = 50  # 控制频率(Hz)
                
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
    parser.add_argument('--gripper_control', action='store', type=str, help='enable gripper control',
                        default="True", required=False)
    parser.add_argument('--can_channel', action='store', type=str, help='CAN channel for gripper control',
                        default="can0", required=False)
    args, unknown = parser.parse_known_args()
    return args


def main():
    args = get_arguments()
    rclpy.init()
    ros_operator = RosOperator(args)
    rclpy.spin(ros_operator)


if __name__ == "__main__":
    main()