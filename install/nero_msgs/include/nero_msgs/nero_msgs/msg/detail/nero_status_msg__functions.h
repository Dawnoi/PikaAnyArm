// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from nero_msgs:msg/NeroStatusMsg.idl
// generated code does not contain a copyright notice

#ifndef NERO_MSGS__MSG__DETAIL__NERO_STATUS_MSG__FUNCTIONS_H_
#define NERO_MSGS__MSG__DETAIL__NERO_STATUS_MSG__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "nero_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "nero_msgs/msg/detail/nero_status_msg__struct.h"

/// Initialize msg/NeroStatusMsg message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * nero_msgs__msg__NeroStatusMsg
 * )) before or use
 * nero_msgs__msg__NeroStatusMsg__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
bool
nero_msgs__msg__NeroStatusMsg__init(nero_msgs__msg__NeroStatusMsg * msg);

/// Finalize msg/NeroStatusMsg message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
void
nero_msgs__msg__NeroStatusMsg__fini(nero_msgs__msg__NeroStatusMsg * msg);

/// Create msg/NeroStatusMsg message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * nero_msgs__msg__NeroStatusMsg__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
nero_msgs__msg__NeroStatusMsg *
nero_msgs__msg__NeroStatusMsg__create();

/// Destroy msg/NeroStatusMsg message.
/**
 * It calls
 * nero_msgs__msg__NeroStatusMsg__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
void
nero_msgs__msg__NeroStatusMsg__destroy(nero_msgs__msg__NeroStatusMsg * msg);

/// Check for msg/NeroStatusMsg message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
bool
nero_msgs__msg__NeroStatusMsg__are_equal(const nero_msgs__msg__NeroStatusMsg * lhs, const nero_msgs__msg__NeroStatusMsg * rhs);

/// Copy a msg/NeroStatusMsg message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
bool
nero_msgs__msg__NeroStatusMsg__copy(
  const nero_msgs__msg__NeroStatusMsg * input,
  nero_msgs__msg__NeroStatusMsg * output);

/// Initialize array of msg/NeroStatusMsg messages.
/**
 * It allocates the memory for the number of elements and calls
 * nero_msgs__msg__NeroStatusMsg__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
bool
nero_msgs__msg__NeroStatusMsg__Sequence__init(nero_msgs__msg__NeroStatusMsg__Sequence * array, size_t size);

/// Finalize array of msg/NeroStatusMsg messages.
/**
 * It calls
 * nero_msgs__msg__NeroStatusMsg__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
void
nero_msgs__msg__NeroStatusMsg__Sequence__fini(nero_msgs__msg__NeroStatusMsg__Sequence * array);

/// Create array of msg/NeroStatusMsg messages.
/**
 * It allocates the memory for the array and calls
 * nero_msgs__msg__NeroStatusMsg__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
nero_msgs__msg__NeroStatusMsg__Sequence *
nero_msgs__msg__NeroStatusMsg__Sequence__create(size_t size);

/// Destroy array of msg/NeroStatusMsg messages.
/**
 * It calls
 * nero_msgs__msg__NeroStatusMsg__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
void
nero_msgs__msg__NeroStatusMsg__Sequence__destroy(nero_msgs__msg__NeroStatusMsg__Sequence * array);

/// Check for msg/NeroStatusMsg message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
bool
nero_msgs__msg__NeroStatusMsg__Sequence__are_equal(const nero_msgs__msg__NeroStatusMsg__Sequence * lhs, const nero_msgs__msg__NeroStatusMsg__Sequence * rhs);

/// Copy an array of msg/NeroStatusMsg messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_nero_msgs
bool
nero_msgs__msg__NeroStatusMsg__Sequence__copy(
  const nero_msgs__msg__NeroStatusMsg__Sequence * input,
  nero_msgs__msg__NeroStatusMsg__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // NERO_MSGS__MSG__DETAIL__NERO_STATUS_MSG__FUNCTIONS_H_
