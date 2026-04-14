# 可视化nero urdf双臂的流程
用于检验双臂模型是否正确

假设项目结构为
```
~/agx_arm_ws/
  src/
    agx_arm_ros/
    nero-dual-arm/
```

以可视化 ` ~/agx_arm_ws/src/nero-dual-arm/src/agx_arm_urdf/nero/urdf/nero_dual_arm_generated.urdf ` 为例

## 0. 从xacro生成urdf

以 ` ~/agx_arm_ws/src/nero-dual-arm/src/agx_arm_urdf/nero/urdf/nero_dual_arm_description.xacro ` 为例

```
xacro ~/agx_arm_ws/src/nero-dual-arm/src/agx_arm_urdf/nero/urdf/nero_dual_arm_description.xacro > ~/agx_arm_ws/src/nero-dual-arm/src/agx_arm_urdf/nero/urdf/nero_dual_arm_generated.urdf
```


## 1. 终端1
启动 robot_state_publisher（发布机器人结构）

```
# 准备环境
source /opt/ros/humble/setup.bash
export ROS_PACKAGE_PATH=~/agx_arm_ws/src/nero-dual-arm/src:$ROS_PACKAGE_PATH

# 发布机器人结构
ros2 run robot_state_publisher robot_state_publisher \
  --ros-args -p robot_description:="$(cat ~/agx_arm_ws/src/nero-dual-arm/src/agx_arm_urdf/nero/urdf/nero_dual_arm_generated.urdf)"
```

预期输出：

```
[INFO] [1773900535.491929253] [robot_state_publisher]: got segment body
[INFO] [1773900535.491976751] [robot_state_publisher]: got segment left_base_link
[INFO] [1773900535.491980437] [robot_state_publisher]: got segment left_link1
[INFO] [1773900535.491982658] [robot_state_publisher]: got segment left_link2
[INFO] [1773900535.491984387] [robot_state_publisher]: got segment left_link3
[INFO] [1773900535.491986045] [robot_state_publisher]: got segment left_link4
[INFO] [1773900535.491987622] [robot_state_publisher]: got segment left_link5
[INFO] [1773900535.491989216] [robot_state_publisher]: got segment left_link6
[INFO] [1773900535.491990919] [robot_state_publisher]: got segment left_link7
[INFO] [1773900535.491992486] [robot_state_publisher]: got segment right_base_link
[INFO] [1773900535.491994173] [robot_state_publisher]: got segment right_link1
[INFO] [1773900535.491995753] [robot_state_publisher]: got segment right_link2
[INFO] [1773900535.491997367] [robot_state_publisher]: got segment right_link3
[INFO] [1773900535.491999315] [robot_state_publisher]: got segment right_link4
[INFO] [1773900535.492000844] [robot_state_publisher]: got segment right_link5
[INFO] [1773900535.492002424] [robot_state_publisher]: got segment right_link6
[INFO] [1773900535.492003922] [robot_state_publisher]: got segment right_link7
[INFO] [1773900535.492005454] [robot_state_publisher]: got segment world
```


## 2. 终端2
启动 joint_state_publisher（发布关节状态）

```
# 准备环境
source /opt/ros/humble/setup.bash
export ROS_PACKAGE_PATH=~/agx_arm_ws/src/nero-dual-arm/src:$ROS_PACKAGE_PATH

# 发布关节状态
ros2 run joint_state_publisher joint_state_publisher
```

## 3. 终端3
启动 RViz2（可视化）

```
ros2 run rviz2 rviz2
```

随后在该命令打开的窗口中进行RViz2配置，以加载模型

| 步骤            | 操作                                         |
| :------------ | :----------------------------------------- |
| 添加RobotModel  | 左下角 **Add** → **RobotModel** → **OK**      |
| 设置Topic       | RobotModel面板中，Topic选择 `/robot_description` |
| 设置Fixed Frame | Global Options中，Fixed Frame改为 `world`      |


尝试查看其坐标轴


| 步骤                 | 操作                                                                                    |
| :----------------- | :------------------------------------------------------------------------------------ |              
| 添加 TF 显示      | 左下角 **Add** → **TF** → **OK**                                                         |
| 确认全局坐标系      | Global Options 中，确认 Fixed Frame 为 `world`（或你当前使用的全局坐标系）                               |
| 查看坐标轴          | 展开 TF 树，找到 `body` 帧，观察坐标轴小三叉标识：<br>• **红色** = x 轴<br>• **绿色** = y 轴<br>• **蓝色** = z 轴 |
| 验证对齐          | 若 `body` 与 `world` 重合且同向，两者的坐标轴应基本重叠                                                  |

