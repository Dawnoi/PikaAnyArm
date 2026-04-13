// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from nero_msgs:msg/PosCmd.idl
// generated code does not contain a copyright notice

#ifndef NERO_MSGS__MSG__DETAIL__POS_CMD__STRUCT_H_
#define NERO_MSGS__MSG__DETAIL__POS_CMD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/PosCmd in the package nero_msgs.
typedef struct nero_msgs__msg__PosCmd
{
  double x;
  double y;
  double z;
  double roll;
  double pitch;
  double yaw;
  double gripper;
  int32_t mode1;
  int32_t mode2;
} nero_msgs__msg__PosCmd;

// Struct for a sequence of nero_msgs__msg__PosCmd.
typedef struct nero_msgs__msg__PosCmd__Sequence
{
  nero_msgs__msg__PosCmd * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nero_msgs__msg__PosCmd__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NERO_MSGS__MSG__DETAIL__POS_CMD__STRUCT_H_
