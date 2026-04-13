// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from nero_msgs:srv/Enable.idl
// generated code does not contain a copyright notice

#ifndef NERO_MSGS__SRV__DETAIL__ENABLE__STRUCT_H_
#define NERO_MSGS__SRV__DETAIL__ENABLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/Enable in the package nero_msgs.
typedef struct nero_msgs__srv__Enable_Request
{
  bool enable_request;
} nero_msgs__srv__Enable_Request;

// Struct for a sequence of nero_msgs__srv__Enable_Request.
typedef struct nero_msgs__srv__Enable_Request__Sequence
{
  nero_msgs__srv__Enable_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nero_msgs__srv__Enable_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/Enable in the package nero_msgs.
typedef struct nero_msgs__srv__Enable_Response
{
  bool enable_response;
} nero_msgs__srv__Enable_Response;

// Struct for a sequence of nero_msgs__srv__Enable_Response.
typedef struct nero_msgs__srv__Enable_Response__Sequence
{
  nero_msgs__srv__Enable_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nero_msgs__srv__Enable_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NERO_MSGS__SRV__DETAIL__ENABLE__STRUCT_H_
