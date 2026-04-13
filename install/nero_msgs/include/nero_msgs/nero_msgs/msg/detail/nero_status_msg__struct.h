// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from nero_msgs:msg/NeroStatusMsg.idl
// generated code does not contain a copyright notice

#ifndef NERO_MSGS__MSG__DETAIL__NERO_STATUS_MSG__STRUCT_H_
#define NERO_MSGS__MSG__DETAIL__NERO_STATUS_MSG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/NeroStatusMsg in the package nero_msgs.
typedef struct nero_msgs__msg__NeroStatusMsg
{
  uint8_t ctrl_mode;
  uint8_t arm_status;
  uint8_t mode_feedback;
  uint8_t teach_status;
  uint8_t motion_status;
  uint8_t trajectory_num;
  int64_t err_code;
  bool joint_1_angle_limit;
  bool joint_2_angle_limit;
  bool joint_3_angle_limit;
  bool joint_4_angle_limit;
  bool joint_5_angle_limit;
  bool joint_6_angle_limit;
  bool joint_7_angle_limit;
  bool communication_status_joint_1;
  bool communication_status_joint_2;
  bool communication_status_joint_3;
  bool communication_status_joint_4;
  bool communication_status_joint_5;
  bool communication_status_joint_6;
  bool communication_status_joint_7;
} nero_msgs__msg__NeroStatusMsg;

// Struct for a sequence of nero_msgs__msg__NeroStatusMsg.
typedef struct nero_msgs__msg__NeroStatusMsg__Sequence
{
  nero_msgs__msg__NeroStatusMsg * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nero_msgs__msg__NeroStatusMsg__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NERO_MSGS__MSG__DETAIL__NERO_STATUS_MSG__STRUCT_H_
