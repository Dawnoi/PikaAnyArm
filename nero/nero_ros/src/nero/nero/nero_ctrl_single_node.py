#!/usr/bin/env python3
# -*-coding:utf8-*-
# 本文件为控制单个Nero机械臂节点
# 基于 arm_controller SDK 封装，逻辑与 piper_ctrl_single_node.py 保持一致
from typing import Optional
import rclpy
from rclpy.node import Node
import rclpy.time
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool
import time
import threading
import argparse
import math
from geometry_msgs.msg import Pose, PoseStamped
from scipy.spatial.transform import Rotation as R

from nero_sdk.arm_controller import ArmController
from nero_msgs.msg import PosCmd, NeroStatusMsg
from nero_msgs.srv import Enable


class NeroRosNode(Node):
    """Nero机械臂ROS2节点
    
    基于 nero_sdk.arm_controller.ArmController 封装
    逻辑与 piper_ctrl_single_node.py 保持一致
    """
    def __init__(self) -> None:
        super().__init__('nero_ctrl_single_node')
        
        # 外部参数
        self.declare_parameter('can_port', 'can0')
        self.declare_parameter('auto_enable', False)
        self.declare_parameter('girpper_exist', True)
        self.declare_parameter('rviz_ctrl_flag', False)
        self.declare_parameter('nero_name', 'left')
        self.declare_parameter('speed_percent', 5)

        self.can_port = self.get_parameter('can_port').get_parameter_value().string_value
        self.auto_enable = self.get_parameter('auto_enable').get_parameter_value().bool_value
        self.girpper_exist = self.get_parameter('girpper_exist').get_parameter_value().bool_value
        self.rviz_ctrl_flag = self.get_parameter('rviz_ctrl_flag').get_parameter_value().bool_value
        self.nero_name = self.get_parameter('nero_name').get_parameter_value().string_value
        self.speed_percent = self.get_parameter('speed_percent').get_parameter_value().integer_value

        self.get_logger().info(f"can_port is {self.can_port}")
        self.get_logger().info(f"auto_enable is {self.auto_enable}")
        self.get_logger().info(f"girpper_exist is {self.girpper_exist}")
        self.get_logger().info(f"rviz_ctrl_flag is {self.rviz_ctrl_flag}")
        self.get_logger().info(f"nero_name is {self.nero_name}")
        self.get_logger().info(f"speed_percent is {self.speed_percent}")

        # Publisher - 与 Piper 保持一致的话题名称
        self.joint_pub = self.create_publisher(JointState, f'/puppet/joint_{self.nero_name}', 1)
        self.joint_ctrl_pub = self.create_publisher(JointState, f'/master/joint_{self.nero_name}', 1)
        self.arm_status_pub = self.create_publisher(NeroStatusMsg, self.get_name()+'/arm_status', 1)
        self.end_pose_pub = self.create_publisher(Pose, self.get_name()+'/end_pose', 1)
        self.end_pose_stamp_pub = self.create_publisher(PoseStamped, f'/puppet/end_pose_{self.nero_name}', 1)

        # service
        self.motor_srv = self.create_service(Enable, 'enable_srv', self.handle_enable_service)

        # joint - Nero 有 7 个关节 + 1 个夹爪: joint1-joint7, gripper
        self.joint_states = JointState()
        self.joint_states.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7', 'gripper']
        self.joint_states.position = [0.0] * 8
        self.joint_states.velocity = [0.0] * 8
        self.joint_states.effort = [0.0] * 8

        # Joint ctrl
        self.joint_ctrl = JointState()
        self.joint_ctrl.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7', 'gripper']
        self.joint_ctrl.position = [0.0] * 8
        self.joint_ctrl.velocity = [0.0] * 8
        self.joint_ctrl.effort = [0.0] * 8

        # 使能标志位
        self.__enable_flag = False

        # 创建 ArmController 并连接 (使用 nero_sdk)
        self.arm_controller = ArmController(channel=self.can_port, robot_type="nero")
        self.arm_controller.connect()

        # 启动订阅线程
        self.create_subscription(PosCmd, 'pos_cmd', self.pos_callback, 1)
        self.create_subscription(JointState, 'joint_ctrl_single', self.joint_callback, 1)
        self.create_subscription(Bool, 'enable_flag', self.enable_callback, 1)

        self.publisher_thread = threading.Thread(target=self.publish_thread)
        self.publisher_thread.start()

    def get_private_topic(self, topic_name):
        return self.get_name()+'/'+topic_name

    def GetEnableFlag(self):
        return self.__enable_flag

    def publish_thread(self):
        """机械臂消息发布 - 与 Piper 逻辑一致"""
        rate = self.create_rate(200)  # 200 Hz
        enable_flag = False
        timeout = 5
        start_time = time.time()
        elapsed_time_flag = False

        while rclpy.ok():
            # 自动使能逻辑
            if self.auto_enable:
                while not enable_flag:
                    elapsed_time = time.time() - start_time
                    print("--------------------")
                    
                    # 检查所有关节使能状态
                    enable_list = self.arm_controller.robot.get_joints_enable_status_list()
                    enable_flag = all(enable_list) if enable_list else False
                    
                    print(f"使能状态: {enable_flag}")
                    
                    # 使能所有关节
                    self.arm_controller.robot.enable()
                    
                    # 夹爪初始化
                    if self.girpper_exist:
                        self.arm_controller.move_gripper(0.0, force=1.0)
                    
                    if enable_flag:
                        self.__enable_flag = True
                    
                    print("--------------------")
                    
                    if elapsed_time > timeout:
                        print("超时....")
                        elapsed_time_flag = True
                        enable_flag = True
                        break
                    time.sleep(1)
            
            if elapsed_time_flag:
                print("程序自动使能超时,退出程序")
                break

            self.PublishArmState()
            self.PublishArmJointAndGirpper()
            self.PublishArmCtrlAndGripper()
            self.PublishArmEndPose()

            rate.sleep()

    def PublishArmState(self):
        """发布机械臂状态"""
        arm_status = NeroStatusMsg()
        status = self.arm_controller.get_arm_status()
        if status is None or not hasattr(status, 'msg'):
            return
        
        msg = status.msg
        arm_status.ctrl_mode = getattr(msg, 'ctrl_mode', 0)
        arm_status.arm_status = getattr(msg, 'arm_status', 0)
        arm_status.mode_feedback = getattr(msg, 'mode_feedback', 0)
        arm_status.teach_status = getattr(msg, 'teach_status', 0)
        arm_status.motion_status = getattr(msg, 'motion_status', 0)
        arm_status.trajectory_num = getattr(msg, 'trajectory_num', 0)
        
        # 错误状态
        err_status = getattr(msg, 'err_status', None)
        if err_status is not None:
            arm_status.err_code = getattr(err_status, 'err_code', 0)
            arm_status.joint_1_angle_limit = getattr(err_status, 'joint_1_angle_limit', False)
            arm_status.joint_2_angle_limit = getattr(err_status, 'joint_2_angle_limit', False)
            arm_status.joint_3_angle_limit = getattr(err_status, 'joint_3_angle_limit', False)
            arm_status.joint_4_angle_limit = getattr(err_status, 'joint_4_angle_limit', False)
            arm_status.joint_5_angle_limit = getattr(err_status, 'joint_5_angle_limit', False)
            arm_status.joint_6_angle_limit = getattr(err_status, 'joint_6_angle_limit', False)
            arm_status.joint_7_angle_limit = getattr(err_status, 'joint_7_angle_limit', False)
            arm_status.communication_status_joint_1 = getattr(err_status, 'communication_status_joint_1', False)
            arm_status.communication_status_joint_2 = getattr(err_status, 'communication_status_joint_2', False)
            arm_status.communication_status_joint_3 = getattr(err_status, 'communication_status_joint_3', False)
            arm_status.communication_status_joint_4 = getattr(err_status, 'communication_status_joint_4', False)
            arm_status.communication_status_joint_5 = getattr(err_status, 'communication_status_joint_5', False)
            arm_status.communication_status_joint_6 = getattr(err_status, 'communication_status_joint_6', False)
            arm_status.communication_status_joint_7 = getattr(err_status, 'communication_status_joint_7', False)
        
        self.arm_status_pub.publish(arm_status)

    def PublishArmJointAndGirpper(self):
        """发布当前关节状态和夹爪状态 - 与 Piper 逻辑一致"""
        self.joint_states.header.stamp = self.get_clock().now().to_msg()

        # 获取关节角度 [j1, j2, j3, j4, j5, j6, j7] 单位 rad
        joint_angles = self.arm_controller.get_joint_angles()
        if joint_angles is None:
            return
        
        positions = list(joint_angles)
        while len(positions) < 7:
            positions.append(0.0)
        positions = positions[:7]
        
        # 获取夹爪状态
        gripper_width = 0.0
        if self.girpper_exist:
            try:
                gripper_status = self.arm_controller.get_gripper_width(timeout=0.1)
                if gripper_status is not None:
                    gripper_width = gripper_status
            except Exception:
                pass
        positions.append(gripper_width)
        
        self.joint_states.position = positions
        
        # 获取电机速度
        velocities = []
        efforts = []
        for i in range(1, 8):
            try:
                motor_state = self.arm_controller.robot.get_motor_states(i)
                if motor_state and hasattr(motor_state, 'msg'):
                    velocities.append(getattr(motor_state.msg, 'velocity', 0.0))
                    efforts.append(getattr(motor_state.msg, 'torque', 0.0))
                else:
                    velocities.append(0.0)
                    efforts.append(0.0)
            except Exception:
                velocities.append(0.0)
                efforts.append(0.0)
        
        velocities.append(0.0)  # gripper velocity
        efforts.append(0.0)    # gripper effort
        
        self.joint_states.velocity = velocities
        self.joint_states.effort = efforts
        
        self.joint_pub.publish(self.joint_states)

    def PublishArmCtrlAndGripper(self):
        """发布当前控制指令（用于回显）"""
        self.joint_ctrl.header.stamp = self.get_clock().now().to_msg()
        # 从 SDK 获取夹爪状态
        gripper_width = 0.0
        if self.girpper_exist:
            try:
                gripper_status = self.arm_controller.get_gripper_width(timeout=0.1)
                if gripper_status is not None:
                    gripper_width = gripper_status
            except Exception:
                pass
        
        # 更新 joint_ctrl 的 position（7个关节 + 夹爪）
        positions = self.joint_ctrl.position[:7] if len(self.joint_ctrl.position) >= 7 else list(self.joint_ctrl.position)
        while len(positions) < 7:
            positions.append(0.0)
        positions = positions[:7]
        positions.append(gripper_width)
        self.joint_ctrl.position = positions
        
        self.joint_ctrl_pub.publish(self.joint_ctrl)

    def PublishArmEndPose(self):
        """发布末端位姿 - 与 Piper 逻辑一致"""
        endpos = Pose()
        
        # 使用 get_tcp_pose() 获取 TCP 位姿
        tcp_pose = self.arm_controller.get_tcp_pose()
        if tcp_pose is None:
            return
        
        endpos.position.x = tcp_pose[0]
        endpos.position.y = tcp_pose[1]
        endpos.position.z = tcp_pose[2]

        # tcp_pose 返回 [x,y,z,roll,pitch,yaw] 单位 rad
        roll, pitch, yaw = tcp_pose[3], tcp_pose[4], tcp_pose[5]
        quaternion = R.from_euler('xyz', [roll, pitch, yaw]).as_quat()
        endpos.orientation.x = quaternion[0]
        endpos.orientation.y = quaternion[1]
        endpos.orientation.z = quaternion[2]
        endpos.orientation.w = quaternion[3]

        self.end_pose_pub.publish(endpos)

        end_pos_stamp = PoseStamped()
        end_pos_stamp.pose = endpos
        end_pos_stamp.header.stamp = self.get_clock().now().to_msg()
        self.end_pose_stamp_pub.publish(end_pos_stamp)

    def pos_callback(self, pos_data):
        """机械臂末端位姿订阅回调函数 - 与 Piper 逻辑一致

        Args:
            pos_data: PosCmd 消息
        """
        self.get_logger().info(f"Received PosCmd:")
        self.get_logger().info(f"x: {pos_data.x}")
        self.get_logger().info(f"y: {pos_data.y}")
        self.get_logger().info(f"z: {pos_data.z}")
        self.get_logger().info(f"roll: {pos_data.roll}")
        self.get_logger().info(f"pitch: {pos_data.pitch}")
        self.get_logger().info(f"yaw: {pos_data.yaw}")
        self.get_logger().info(f"gripper: {pos_data.gripper}")

        if self.GetEnableFlag():
            # 末端位姿控制 [x, y, z, roll, pitch, yaw]
            # 注意: SDK 的 move_p 期望法兰位姿, 如果需要 TCP 位姿控制需要转换
            pose = [pos_data.x, pos_data.y, pos_data.z,
                    pos_data.roll, pos_data.pitch, pos_data.yaw]
            self.arm_controller.move_p(pose, blocking=False)

            # 夹爪控制
            if self.girpper_exist:
                # PosCmd.gripper 单位假设是 0-100000, 转换为 0-0.1 m
                gripper_width = max(0.0, min(0.1, pos_data.gripper / 100000.0))
                self.arm_controller.move_gripper(gripper_width, force=1.0)

    def joint_callback(self, joint_data):
        """机械臂关节角回调函数 - 与 Piper 逻辑一致

        Args:
            joint_data: JointState 消息
        """
        if len(joint_data.position) >= 7:
            # 提取 7 个关节角度 (单位 rad)
            joints = list(joint_data.position[:7])
            
            if self.GetEnableFlag():
                # 设定电机速度 (如果提供)
                if joint_data.velocity and len(joint_data.velocity) >= 1:
                    all_zeros = all(v == 0 for v in joint_data.velocity)
                    if not all_zeros:
                        # 取第 7 个关节的速度作为整体速度
                        vel = joint_data.velocity[6] if len(joint_data.velocity) >= 7 else 50
                        speed = max(1, min(100, int(abs(vel))))
                        self.arm_controller.robot.set_speed_percent(speed)
                    else:
                        self.arm_controller.robot.set_speed_percent(50)
                else:
                    self.arm_controller.robot.set_speed_percent(50)
                
                # 关节运动
                self.arm_controller.move_js(joints, blocking=False)

                # 夹爪控制 (第 7 个关节之后)
                if self.girpper_exist and len(joint_data.position) > 7:
                    gripper_width = max(0.0, min(0.1, joint_data.position[7]))
                    self.arm_controller.move_gripper(gripper_width, force=1.0)

    def enable_callback(self, enable_flag: Bool):
        """机械臂使能回调函数 - 与 Piper 逻辑一致

        Args:
            enable_flag: Bool 消息
        """
        self.get_logger().info(f"Received enable flag:")
        self.get_logger().info(f"enable_flag: {enable_flag.data}")
        
        if enable_flag.data:
            self.__enable_flag = True
            self.arm_controller.robot.enable()
            if self.girpper_exist:
                self.arm_controller.move_gripper(0.0, force=1.0)
        else:
            self.__enable_flag = False
            self.arm_controller.robot.disable()
            if self.girpper_exist:
                self.arm_controller.move_gripper(0.0, force=1.0)

    def handle_enable_service(self, req, resp):
        """使能服务回调 - 与 Piper 逻辑一致"""
        self.get_logger().info(f"Received request: {req.enable_request}")
        
        enable_flag = False
        loop_flag = False
        timeout = 5
        start_time = time.time()
        elapsed_time_flag = False

        while not loop_flag:
            elapsed_time = time.time() - start_time
            self.get_logger().info("--------------------")
            
            # 获取所有关节使能状态
            enable_list = self.arm_controller.robot.get_joints_enable_status_list()
            
            if req.enable_request:
                enable_flag = all(enable_list) if enable_list else False
                self.arm_controller.robot.enable()
                if self.girpper_exist:
                    self.arm_controller.move_gripper(0.0, force=1.0)
            else:
                enable_flag = any(enable_list) if enable_list else True
                self.arm_controller.robot.disable()
                if self.girpper_exist:
                    self.arm_controller.move_gripper(0.0, force=1.0)
            
            self.get_logger().info(f"使能状态: {enable_flag}")
            self.__enable_flag = enable_flag
            self.get_logger().info("--------------------")
            
            if enable_flag == req.enable_request:
                loop_flag = True
                enable_flag = True
            else:
                loop_flag = False
                enable_flag = False
            
            if elapsed_time > timeout:
                self.get_logger().info("超时....")
                elapsed_time_flag = True
                enable_flag = False
                loop_flag = True
                break
            time.sleep(0.5)
        
        resp.enable_response = enable_flag
        self.get_logger().info(f"Returning response: {resp.enable_response}")
        return resp


def main(args=None):
    rclpy.init(args=args)
    nero_single_node = NeroRosNode()
    try:
        rclpy.spin(nero_single_node)
    except KeyboardInterrupt:
        pass
    finally:
        nero_single_node.arm_controller.disconnect()
        nero_single_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
