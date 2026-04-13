#!/usr/bin/env python3
"""
Nero 夹爪 Topic 测试脚本
在没有真机的情况下模拟数据流来测试 topic 通信
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool
import time


class NeroTopicTester(Node):
    def __init__(self):
        super().__init__('nero_topic_tester')
        
        self.get_logger().info("=== Nero Topic 测试节点启动 ===")
        
        # 订阅 puppet 关节状态（包含夹爪）
        self.joint_sub = self.create_subscription(
            JointState,
            '/puppet/joint_left',
            self.joint_callback,
            10
        )
        
        # 订阅 master 关节控制回显
        self.joint_ctrl_sub = self.create_subscription(
            JointState,
            '/master/joint_left',
            self.joint_callback_ctrl,
            10
        )
        
        # 发布测试数据到 joint_ctrl_single（触发夹爪控制）
        self.joint_ctrl_pub = self.create_publisher(
            JointState,
            'joint_ctrl_single',
            10
        )
        
        # 使能标志发布
        self.enable_pub = self.create_publisher(Bool, 'enable_flag', 10)
        
        self.received_joints = False
        self.received_ctrl = False
        
        # 等待 2 秒让订阅者建立连接
        self.get_logger().info("等待订阅者连接...")
        time.sleep(2)
        
        # 开始测试
        self.run_tests()
    
    def joint_callback(self, msg):
        """接收关节状态（包含夹爪）"""
        self.received_joints = True
        self.get_logger().info(
            f"收到关节状态: positions={msg.position}, names={msg.name}"
        )
        if len(msg.position) == 8:
            self.get_logger().info(f"✓ 夹爪数据正确: gripper={msg.position[7]:.4f}m")
        else:
            self.get_logger().warn(f"✗ 关节数量不对: {len(msg.position)}, 期望 8")
    
    def joint_callback_ctrl(self, msg):
        """接收控制指令回显"""
        self.received_ctrl = True
        self.get_logger().info(
            f"收到控制回显: positions={msg.position}"
        )
    
    def run_tests(self):
        """执行测试"""
        self.get_logger().info("\n=== 开始测试 ===\n")
        
        # 测试 1: 发布使能标志
        self.get_logger().info("测试 1: 发布使能标志...")
        enable_msg = Bool()
        enable_msg.data = True
        self.enable_pub.publish(enable_msg)
        self.get_logger().info("已发布 enable_flag = True")
        
        time.sleep(0.5)
        
        # 测试 2: 发布关节控制指令（7关节 + 夹爪）
        self.get_logger().info("\n测试 2: 发布关节控制指令（包含夹爪）...")
        
        joint_msg = JointState()
        joint_msg.header.stamp = self.get_clock().now().to_msg()
        joint_msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7', 'gripper']
        joint_msg.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05]  # 夹爪开 5cm
        joint_msg.velocity = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        joint_msg.effort = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        self.joint_ctrl_pub.publish(joint_msg)
        self.get_logger().info(f"已发布: position={joint_msg.position}")
        
        # 等待响应
        time.sleep(1.0)
        
        # 测试 3: 夹爪闭合
        self.get_logger().info("\n测试 3: 测试夹爪闭合...")
        joint_msg.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 夹爪闭
        self.joint_ctrl_pub.publish(joint_msg)
        self.get_logger().info("已发布: gripper=0.0 (闭合)")
        
        time.sleep(1.0)
        
        # 测试 4: 夹爪半开
        self.get_logger().info("\n测试 4: 测试夹爪半开...")
        joint_msg.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05]  # 夹爪半开
        self.joint_ctrl_pub.publish(joint_msg)
        self.get_logger().info("已发布: gripper=0.05 (半开)")
        
        time.sleep(2.0)
        
        # 总结
        self.get_logger().info("\n=== 测试完成 ===")
        self.get_logger().info(f"收到关节状态反馈: {self.received_joints}")
        self.get_logger().info(f"收到控制回显: {self.received_ctrl}")
        
        if self.received_joints and self.received_ctrl:
            self.get_logger().info("✓ Topic 通信正常!")
        else:
            self.get_logger().warn("✗ 未收到反馈，请检查节点是否运行")


def main():
    rclpy.init()
    tester = NeroTopicTester()
    try:
        rclpy.spin(tester)
    except KeyboardInterrupt:
        pass
    finally:
        tester.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
