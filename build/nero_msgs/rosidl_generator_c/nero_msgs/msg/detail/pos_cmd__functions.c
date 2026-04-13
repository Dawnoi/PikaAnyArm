// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from nero_msgs:msg/PosCmd.idl
// generated code does not contain a copyright notice
#include "nero_msgs/msg/detail/pos_cmd__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
nero_msgs__msg__PosCmd__init(nero_msgs__msg__PosCmd * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  // z
  // roll
  // pitch
  // yaw
  // gripper
  // mode1
  // mode2
  return true;
}

void
nero_msgs__msg__PosCmd__fini(nero_msgs__msg__PosCmd * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
  // z
  // roll
  // pitch
  // yaw
  // gripper
  // mode1
  // mode2
}

bool
nero_msgs__msg__PosCmd__are_equal(const nero_msgs__msg__PosCmd * lhs, const nero_msgs__msg__PosCmd * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  // roll
  if (lhs->roll != rhs->roll) {
    return false;
  }
  // pitch
  if (lhs->pitch != rhs->pitch) {
    return false;
  }
  // yaw
  if (lhs->yaw != rhs->yaw) {
    return false;
  }
  // gripper
  if (lhs->gripper != rhs->gripper) {
    return false;
  }
  // mode1
  if (lhs->mode1 != rhs->mode1) {
    return false;
  }
  // mode2
  if (lhs->mode2 != rhs->mode2) {
    return false;
  }
  return true;
}

bool
nero_msgs__msg__PosCmd__copy(
  const nero_msgs__msg__PosCmd * input,
  nero_msgs__msg__PosCmd * output)
{
  if (!input || !output) {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  // roll
  output->roll = input->roll;
  // pitch
  output->pitch = input->pitch;
  // yaw
  output->yaw = input->yaw;
  // gripper
  output->gripper = input->gripper;
  // mode1
  output->mode1 = input->mode1;
  // mode2
  output->mode2 = input->mode2;
  return true;
}

nero_msgs__msg__PosCmd *
nero_msgs__msg__PosCmd__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nero_msgs__msg__PosCmd * msg = (nero_msgs__msg__PosCmd *)allocator.allocate(sizeof(nero_msgs__msg__PosCmd), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(nero_msgs__msg__PosCmd));
  bool success = nero_msgs__msg__PosCmd__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
nero_msgs__msg__PosCmd__destroy(nero_msgs__msg__PosCmd * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    nero_msgs__msg__PosCmd__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
nero_msgs__msg__PosCmd__Sequence__init(nero_msgs__msg__PosCmd__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nero_msgs__msg__PosCmd * data = NULL;

  if (size) {
    data = (nero_msgs__msg__PosCmd *)allocator.zero_allocate(size, sizeof(nero_msgs__msg__PosCmd), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = nero_msgs__msg__PosCmd__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        nero_msgs__msg__PosCmd__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
nero_msgs__msg__PosCmd__Sequence__fini(nero_msgs__msg__PosCmd__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      nero_msgs__msg__PosCmd__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

nero_msgs__msg__PosCmd__Sequence *
nero_msgs__msg__PosCmd__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nero_msgs__msg__PosCmd__Sequence * array = (nero_msgs__msg__PosCmd__Sequence *)allocator.allocate(sizeof(nero_msgs__msg__PosCmd__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = nero_msgs__msg__PosCmd__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
nero_msgs__msg__PosCmd__Sequence__destroy(nero_msgs__msg__PosCmd__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    nero_msgs__msg__PosCmd__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
nero_msgs__msg__PosCmd__Sequence__are_equal(const nero_msgs__msg__PosCmd__Sequence * lhs, const nero_msgs__msg__PosCmd__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!nero_msgs__msg__PosCmd__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
nero_msgs__msg__PosCmd__Sequence__copy(
  const nero_msgs__msg__PosCmd__Sequence * input,
  nero_msgs__msg__PosCmd__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(nero_msgs__msg__PosCmd);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    nero_msgs__msg__PosCmd * data =
      (nero_msgs__msg__PosCmd *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!nero_msgs__msg__PosCmd__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          nero_msgs__msg__PosCmd__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!nero_msgs__msg__PosCmd__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
