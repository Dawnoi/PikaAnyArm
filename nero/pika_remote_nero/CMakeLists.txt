cmake_minimum_required(VERSION 3.5)
project(pika_remote_nero)
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(nero_description REQUIRED)
find_package(data_msgs REQUIRED)

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

install(
  DIRECTORY scripts
  DESTINATION share/${PROJECT_NAME}/
)

# Install Python executables
install(PROGRAMS
  scripts/nero_FK.py
  scripts/nero_IK.py
  scripts/teleop_nero_publish.py
  scripts/transformations.py
  scripts/arm_FIK.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
