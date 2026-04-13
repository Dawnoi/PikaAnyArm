#!/usr/bin/env python3
# -*-coding:utf8-*-
# 本文件为控制单个Nero机械臂节点
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
    """Nero机械臂ros2节点
    """
    def __init__(self) -> None:
        super().__init__('nero_ctrl_single_node')
        # 外部参数
        self.declare_parameter('can_port', 'can0')
        self.declare_parameter('auto_enable', False)
        self.declare_parameter('girpper_exist', True)
        self.declare_parameter('rviz_ctrl_flag', False)
        self.declare_parameter('nero_name', 'left')

        self.can_port = self.get_parameter('can_port').get_parameter_value().string_value
        self.auto_enable = self.get_parameter('auto_enable').get_parameter_value().bool_value
        self.girpper_exist = self.get_parameter('girpper_exist').get_parameter_value().bool_value
        self.rviz_ctrl_flag = self.get_parameter('rviz_ctrl_flag').get_parameter_value().bool_value
        self.nero_name = self.get_parameter('nero_name').get_parameter_value().string_value

        self.get_logger().info(f"can_port is {self.can_port}")
        self.get_logger().info(f"auto_enable is {self.auto_enable}")
        self.get_logger().info(f"girpper_exist is {self.girpper_exist}")
        self.get_logger().info(f"rviz_ctrl_flag is {self.rviz_ctrl_flag}")
        self.get_logger().info(f"nero_name is {self.nero_name}")

        # Publisher
        self.joint_pub = self.create_publisher(JointState, f'/puppet/joint_{self.nero_name}', 1)
        self.joint_ctrl_pub = self.create_publisher(JointState, f'/master/joint_{self.nero_name}', 1)
        self.arm_status_pub = self.create_publisher(NeroStatusMsg, self.get_name()+'/arm_status', 1)
        self.end_pose_pub = self.create_publisher(Pose, self.get_name()+'/end_pose', 1)
        self.end_pose_stamp_pub = self.create_publisher(PoseStamped, f'/puppet/end_pose_{self.nero_name}', 1)

        # service
        self.motor_srv = self.create_service(Enable, 'enable_srv', self.handle_enable_service)

        # joint - URDF 中 joint1-joint7 共7个关节
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

        # 创建Nero控制器并连接
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
        """机械臂消息发布
        """
        rate = self.create_rate(200)  # 200 Hz
        while rclpy.ok():
            self.PublishArmState()
            self.PublishArmJointAndGirpper()
            self.PublishArmCtrlAndGripper()
            self.PubilsArmEndPose()
            rate.sleep()

    def PublishArmState(self):
        """发布机械臂状态"""
        arm_status = NeroStatusMsg()
        arm_status_data = self.arm_controller.get_arm_status()
        if arm_status_data is None:
            return
        
        # 从 SDK 获取状态数据
        if hasattr(arm_status_data, 'msg'):
            status_msg = arm_status_data.msg
            arm_status.ctrl_mode = getattr(status_msg, 'ctrl_mode', 0)
            arm_status.arm_status = getattr(status_msg, 'arm_status', 0)
            arm_status.mode_feedback = getattr(status_msg, 'mode_feedback', 0)
            arm_status.teach_status = getattr(status_msg, 'teach_status', 0)
            arm_status.motion_status = getattr(status_msg, 'motion_status', 0)
            arm_status.trajectory_num = getattr(status_msg, 'trajectory_num', 0)
            arm_status.err_code = getattr(status_msg, 'err_code', 0)
        
        self.arm_status_pub.publish(arm_status)

    def PublishArmJointAndGirpper(self):
        """发布当前关节状态和夹爪状态"""
        self.joint_states.header.stamp = self.get_clock().now().to_msg()

        joint_angles = self.arm_controller.get_joint_angles()
        if joint_angles is None:
            return

        # Nero URDF: joint1-6 (6个臂关节) + joint7 (末端关节) + 夹爪
        # FK/IK 读取 [:7]，期望 position[6] = joint7, position[7] = 夹爪
        # 填充到8个位置: 6个臂关节 + joint7(=0) + 夹爪宽度
        gripper_width = self.arm_controller.get_gripper_width() or 0.0
        
        # 确保有足够的关节数据
        positions = list(joint_angles)
        while len(positions) < 7:
            positions.append(0.0)  # 填充 joint7
        positions.append(gripper_width)  # 添加夹爪
        
        self.joint_states.position = positions[:8]
        self.joint_states.velocity = [0.0] * 8
        self.joint_states.effort = [0.0] * 8

        self.joint_pub.publish(self.joint_states)

    def PublishArmCtrlAndGripper(self):
        """发布当前控制指令（用于回显）"""
        self.joint_ctrl.header.stamp = self.get_clock().now().to_msg()
        # TODO: 从 SDK 获取当前控制指令
        self.joint_ctrl.position = [0.0] * 8
        self.joint_ctrl_pub.publish(self.joint_ctrl)

    def PubilsArmEndPose(self):
        """发布末端位姿"""
        endpos = Pose()
        tcp_pose = self.arm_controller.get_tcp_pose()
        if tcp_pose is None:
            return

        endpos.position.x = tcp_pose[0]
        endpos.position.y = tcp_pose[1]
        endpos.position.z = tcp_pose[2]

        # tcp_pose 返回 [x,y,z,roll,pitch,yaw]
        roll, pitch, yaw = tcp_pose[3:6]
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
        """机械臂末端位姿订阅回调函数

        Args:
            pos_data (): PosCmd 消息
        """
        self.get_logger().info(f"Received PosCmd:")
        self.get_logger().info(f"x: {pos_data.x}")
        self.get_logger().info(f"y: {pos_data.y}")
        self.get_logger().info(f"z: {pos_data.z}")
        self.get_logger().info(f"roll: {pos_data.roll}")
        self.get_logger().info(f"pitch: {pos_data.pitch}")
        self.get_logger().info(f"yaw: {pos_data.yaw}")
        self.get_logger().info(f"gripper: {pos_data.gripper}")

        if(self.GetEnableFlag()):
            # 末端位姿控制 [x, y, z, roll, pitch, yaw]
            pose = [pos_data.x, pos_data.y, pos_data.z,
                    pos_data.roll, pos_data.pitch, pos_data.yaw]
            self.arm_controller.move_p(pose, blocking=False)

            # 夹爪控制
            if(self.girpper_exist):
                gripper_width = pos_data.gripper / 100000.0  # 假设 PosCmd 的 gripper 单位转换为米
                self.arm_controller.move_gripper(gripper_width, force=1.0)

    def joint_callback(self, joint_data):
        """机械臂关节角回调函数

        Args:
            joint_data (): JointState 消���
        """
        # self.get_logger().info(f"Received Joint States:")
        if(len(joint_data.position) >= 6):
            joints = list(joint_data.position[:6])
            if(self.GetEnableFlag()):
                self.arm_controller.move_j(joints, blocking=False)

                # 夹爪控制 (第7个关节)
                if(self.girpper_exist and len(joint_data.position) >= 7):
                    gripper_width = joint_data.position[6]
                    self.arm_controller.move_gripper(gripper_width, force=1.0)

    def enable_callback(self, enable_flag:Bool):
        """机械臂使能回调函数

        Args:
            enable_flag ():
        """
        self.get_logger().info(f"Received enable flag:")
        self.get_logger().info(f"enable_flag: {enable_flag.data}")
        if(enable_flag.data):
            self.__enable_flag = True
            self.arm_controller.connect()
        else:
            self.__enable_flag = False
            self.arm_controller.disconnect()

    def handle_enable_service(self, req, resp):
        """使能服务回调"""
        self.get_logger().info(f"Received request: {req.enable_request}")
        try:
            if req.enable_request:
                self.arm_controller.connect()
                resp.enable_response = True
            else:
                self.arm_controller.disconnect()
                resp.enable_response = False
        except Exception as e:
            self.get_logger().error(f"Enable service error: {e}")
            resp.enable_response = False
        return resp


def main(args=None):
    rclpy.init(args=args)
    nero_single_node = NeroRosNode()
    try:
        rclpy.spin(nero_single_node)
    except KeyboardInterrupt:
        pass
    finally:
        nero_single_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
