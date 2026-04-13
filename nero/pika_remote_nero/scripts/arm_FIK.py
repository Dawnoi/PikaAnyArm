#!/usr/bin/env python3
"""
Nero Arm Forward/Inverse Kinematics
基于 Pinocchio 和 CasADi 的运动学求解器
适配 Nero 七轴机械臂
"""

import casadi
import meshcat.geometry as mg
import math
import numpy as np
import pinocchio as pin
from pinocchio import casadi as cpin
from pinocchio.visualize import MeshcatVisualizer
from transformations import quaternion_from_euler, euler_from_quaternion, quaternion_from_matrix
import os
import sys
from ament_index_python.packages import get_package_share_directory

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

os.environ['MKL_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'


def matrix_to_xyzrpy(matrix):
    """从变换矩阵提取位置和欧拉角"""
    x = matrix[0, 3]
    y = matrix[1, 3]
    z = matrix[2, 3]
    roll = math.atan2(matrix[2, 1], matrix[2, 2])
    pitch = math.asin(-matrix[2, 0])
    yaw = math.atan2(matrix[1, 0], matrix[0, 0])
    return [x, y, z, roll, pitch, yaw]


def create_transformation_matrix(x, y, z, roll, pitch, yaw):
    """创建 4x4 齐次变换矩阵"""
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


class Arm_FK:
    """Nero 机械臂正运动学计算"""
    def __init__(self, args):
        self.args = args
        np.set_printoptions(precision=5, suppress=True, linewidth=200)

        # 获取 nero_description 包路径
        package_path = get_package_share_directory('nero_description')
        urdf_path = os.path.join(package_path, 'urdf', 'nero_description.urdf')

        # 加载 URDF 模型
        self.robot = pin.RobotWrapper.BuildFromURDF(
            urdf_path,
            package_dirs=package_path
        )

        # 锁定夹爪关节（prismatic joints）
        self.jointsToLockIDs = ["gripper_joint1", "gripper_joint2"]
        self.reduced_robot = self.robot.buildReducedRobot(
            list_of_joints_to_lock=self.jointsToLockIDs,
            reference_configuration=np.array([0] * self.robot.model.nq),
        )

        # 末端执行器偏移矩阵（相对于 link7）
        # gripper_flange 通过 fixed joint 连接 link7
        self.first_matrix = create_transformation_matrix(0, 0, 0, 0, 0, 0)
        self.second_matrix = create_transformation_matrix(
            self.args.gripper_xyzrpy[0], self.args.gripper_xyzrpy[1], self.args.gripper_xyzrpy[2],
            self.args.gripper_xyzrpy[3], self.args.gripper_xyzrpy[4], self.args.gripper_xyzrpy[5]
        )
        self.last_matrix = np.dot(self.first_matrix, self.second_matrix)
        q = quaternion_from_matrix(self.last_matrix)
        # 使用 'joint7' 而不是 'link7'（link7 是 link 名称，joint7 才是关节名称）
        joint7_id = self.reduced_robot.model.getJointId('joint7')
        self.reduced_robot.model.addFrame(
            pin.Frame('ee',
                      joint7_id,
                      pin.SE3(
                          pin.Quaternion(q[3], q[0], q[1], q[2]),
                          np.array([self.last_matrix[0, 3], self.last_matrix[1, 3], self.last_matrix[2, 3]]),
                      ),
                      pin.FrameType.OP_FRAME)
        )

    def get_pose(self, q):
        """根据关节角度计算末端位姿"""
        joint7_id = self.reduced_robot.model.getJointId('joint7')
        pin.forwardKinematics(self.reduced_robot.model, self.reduced_robot.data, np.concatenate([q], axis=0))
        
        end_pose = create_transformation_matrix(
            self.reduced_robot.data.oMi[joint7_id].translation[0],
            self.reduced_robot.data.oMi[joint7_id].translation[1],
            self.reduced_robot.data.oMi[joint7_id].translation[2],
            math.atan2(self.reduced_robot.data.oMi[joint7_id].rotation[2, 1], self.reduced_robot.data.oMi[joint7_id].rotation[2, 2]),
            math.asin(-self.reduced_robot.data.oMi[joint7_id].rotation[2, 0]),
            math.atan2(self.reduced_robot.data.oMi[joint7_id].rotation[1, 0], self.reduced_robot.data.oMi[joint7_id].rotation[0, 0])
        )
        end_pose = np.dot(end_pose, self.last_matrix)
        return matrix_to_xyzrpy(end_pose)


class Arm_IK:
    """Nero 机械臂逆运动学计算（基于数值优化）"""
    def __init__(self, args):
        self.args = args
        np.set_printoptions(precision=5, suppress=True, linewidth=200)

        # 获取 nero_description 包路径
        package_path = get_package_share_directory('nero_description')
        urdf_path = os.path.join(package_path, 'urdf', 'nero_description.urdf')

        # 加载 URDF 模型
        self.robot = pin.RobotWrapper.BuildFromURDF(
            urdf_path,
            package_dirs=package_path,
        )

        # 锁定夹爪关节
        self.jointsToLockIDs = ["gripper_joint1", "gripper_joint2"]
        self.reduced_robot = self.robot.buildReducedRobot(
            list_of_joints_to_lock=self.jointsToLockIDs,
            reference_configuration=np.array([0] * self.robot.model.nq),
        )

        # 末端执行器偏移矩阵
        self.first_matrix = create_transformation_matrix(0, 0, 0, 0, 0, 0)
        self.second_matrix = create_transformation_matrix(
            self.args.gripper_xyzrpy[0], self.args.gripper_xyzrpy[1], self.args.gripper_xyzrpy[2],
            self.args.gripper_xyzrpy[3], self.args.gripper_xyzrpy[4], self.args.gripper_xyzrpy[5]
        )
        self.last_matrix = np.dot(self.first_matrix, self.second_matrix)
        q = quaternion_from_matrix(self.last_matrix)
        # 使用 'joint7' 而不是 'link7'（link7 是 link 名称，joint7 才是关节名称）
        joint7_id = self.reduced_robot.model.getJointId('joint7')
        self.reduced_robot.model.addFrame(
            pin.Frame('ee',
                      joint7_id,
                      pin.SE3(
                          pin.Quaternion(q[3], q[0], q[1], q[2]),
                          np.array([self.last_matrix[0, 3], self.last_matrix[1, 3], self.last_matrix[2, 3]]),
                      ),
                      pin.FrameType.OP_FRAME)
        )

        # 碰撞检测模型
        self.geom_model = pin.buildGeomFromUrdf(self.robot.model, urdf_path, pin.GeometryType.COLLISION)
        for i in range(4, 10):
            for j in range(0, 3):
                self.geom_model.addCollisionPair(pin.CollisionPair(i, j))
        self.geometry_data = pin.GeometryData(self.geom_model)

        # 初始化数据
        self.init_data = np.zeros(self.reduced_robot.model.nq)
        self.history_data = np.zeros(self.reduced_robot.model.nq)

        # 初始化 MeshCat 可视化器
        self.vis = MeshcatVisualizer(self.reduced_robot.model, self.reduced_robot.collision_model, self.reduced_robot.visual_model)
        self.vis.initViewer(open=True)
        self.vis.loadViewerModel("pinocchio")
        self.vis.displayFrames(True, frame_ids=[self.reduced_robot.model.getFrameId('ee')], axis_length=0.15, axis_width=5)
        self.vis.display(pin.neutral(self.reduced_robot.model))

        # 目标末端执行器帧可视化
        frame_viz_names = ['ee_target']
        FRAME_AXIS_POSITIONS = (
            np.array([[0, 0, 0], [1, 0, 0],
                      [0, 0, 0], [0, 1, 0],
                      [0, 0, 0], [0, 0, 1]]).astype(np.float32).T
        )
        FRAME_AXIS_COLORS = (
            np.array([[1, 0, 0], [1, 0.6, 0],
                      [0, 1, 0], [0.6, 1, 0],
                      [0, 0, 1], [0, 0.6, 1]]).astype(np.float32).T
        )
        axis_length = 0.1
        axis_width = 10
        for frame_viz_name in frame_viz_names:
            self.vis.viewer[frame_viz_name].set_object(
                mg.LineSegments(
                    mg.PointsGeometry(
                        position=axis_length * FRAME_AXIS_POSITIONS,
                        color=FRAME_AXIS_COLORS,
                    ),
                    mg.LineBasicMaterial(
                        linewidth=axis_width,
                        vertexColors=True,
                    ),
                )
            )

        # 创建 CasADi 模型进行符号计算
        self.cmodel = cpin.Model(self.reduced_robot.model)
        self.cdata = self.cmodel.createData()

        # 符号变量
        self.cq = casadi.SX.sym("q", self.reduced_robot.model.nq, 1)
        self.cTf = casadi.SX.sym("tf", 4, 4)
        cpin.framesForwardKinematics(self.cmodel, self.cdata, self.cq)

        # 获取末端执行器帧 ID 并定义误差函数
        self.gripper_id = self.reduced_robot.model.getFrameId("ee")
        self.error = casadi.Function(
            "error",
            [self.cq, self.cTf],
            [
                casadi.vertcat(
                    cpin.log6(
                        self.cdata.oMf[self.gripper_id].inverse() * cpin.SE3(self.cTf)
                    ).vector,
                )
            ],
        )

        # 定义优化问题
        self.opti = casadi.Opti()
        self.var_q = self.opti.variable(self.reduced_robot.model.nq)
        self.param_tf = self.opti.parameter(4, 4)

        # 误差函数：位置 + 姿态
        error_vec = self.error(self.var_q, self.param_tf)
        pos_error = error_vec[:3]
        ori_error = error_vec[3:]
        weight_position = 1.0
        weight_orientation = 0.1
        self.totalcost = casadi.sumsqr(weight_position * pos_error) + casadi.sumsqr(weight_orientation * ori_error)
        self.regularization = casadi.sumsqr(self.var_q)

        # 设置约束和目标
        self.opti.subject_to(self.opti.bounded(
            self.reduced_robot.model.lowerPositionLimit,
            self.var_q,
            self.reduced_robot.model.upperPositionLimit)
        )
        self.opti.minimize(20 * self.totalcost + 0.01 * self.regularization)

        # IPOPT 求解器配置
        opts = {
            'ipopt': {
                'print_level': 0,
                'max_iter': 50,
                'tol': 1e-4
            },
            'print_time': False
        }
        self.opti.solver("ipopt", opts)

    def ik_fun(self, target_pose, gripper=0, motorstate=None, motorV=None):
        """逆运动学求解"""
        gripper = np.array([gripper/2.0, -gripper/2.0])
        if motorstate is not None:
            self.init_data = motorstate
        self.opti.set_initial(self.var_q, self.init_data)

        # 可视化目标位姿
        self.vis.viewer['ee_target'].set_transform(target_pose)

        self.opti.set_value(self.param_tf, target_pose)

        try:
            sol = self.opti.solve_limited()
            sol_q = self.opti.value(self.var_q)

            if self.init_data is not None:
                max_diff = max(abs(self.history_data - sol_q))
                self.init_data = sol_q
                if max_diff > 30.0/180.0*3.1415:
                    self.init_data = np.zeros(self.reduced_robot.model.nq)
            else:
                self.init_data = sol_q

            self.history_data = sol_q
            self.vis.display(sol_q)

            if motorV is not None:
                v = motorV * 0.0
            else:
                v = (sol_q - self.init_data) * 0.0

            tau_ff = pin.rnea(self.reduced_robot.model, self.reduced_robot.data, sol_q, v,
                              np.zeros(self.reduced_robot.model.nv))

            is_collision = self.check_self_collision(sol_q, gripper)
            dist = self.get_dist(sol_q, target_pose[:3, 3])
            return sol_q, tau_ff, not is_collision

        except Exception as e:
            print(f"IK 求解失败: {e}")
            return None, '', False

    def check_self_collision(self, q, gripper=np.array([0, 0])):
        """碰撞检测"""
        pin.forwardKinematics(self.robot.model, self.robot.data, np.concatenate([q, gripper], axis=0))
        pin.updateGeometryPlacements(self.robot.model, self.robot.data, self.geom_model, self.geometry_data)
        collision = pin.computeCollisions(self.geom_model, self.geometry_data, False)
        return collision

    def get_dist(self, q, xyz):
        """计算当前位置到目标位置的距离"""
        joint7_id = self.reduced_robot.model.getJointId('joint7')
        pin.forwardKinematics(self.reduced_robot.model, self.reduced_robot.data, np.concatenate([q], axis=0))
        dist = math.sqrt(
            pow((xyz[0] - self.reduced_robot.data.oMi[joint7_id].translation[0]), 2) +
            pow((xyz[1] - self.reduced_robot.data.oMi[joint7_id].translation[1]), 2) +
            pow((xyz[2] - self.reduced_robot.data.oMi[joint7_id].translation[2]), 2)
        )
        return dist

    def get_pose(self, q):
        """根据关节角度计算末端位姿"""
        joint7_id = self.reduced_robot.model.getJointId('joint7')
        pin.forwardKinematics(self.reduced_robot.model, self.reduced_robot.data, np.concatenate([q], axis=0))
        end_pose = create_transformation_matrix(
            self.reduced_robot.data.oMi[joint7_id].translation[0],
            self.reduced_robot.data.oMi[joint7_id].translation[1],
            self.reduced_robot.data.oMi[joint7_id].translation[2],
            math.atan2(self.reduced_robot.data.oMi[joint7_id].rotation[2, 1], self.reduced_robot.data.oMi[joint7_id].rotation[2, 2]),
            math.asin(-self.reduced_robot.data.oMi[joint7_id].rotation[2, 0]),
            math.atan2(self.reduced_robot.data.oMi[joint7_id].rotation[1, 0], self.reduced_robot.data.oMi[joint7_id].rotation[0, 0])
        )
        end_pose = np.dot(end_pose, self.last_matrix)
        return matrix_to_xyzrpy(end_pose)
