// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from nero_msgs:srv/Enable.idl
// generated code does not contain a copyright notice
#include "nero_msgs/srv/detail/enable__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
nero_msgs__srv__Enable_Request__init(nero_msgs__srv__Enable_Request * msg)
{
  if (!msg) {
    return false;
  }
  // enable_request
  return true;
}

void
nero_msgs__srv__Enable_Request__fini(nero_msgs__srv__Enable_Request * msg)
{
  if (!msg) {
    return;
  }
  // enable_request
}

bool
nero_msgs__srv__Enable_Request__are_equal(const nero_msgs__srv__Enable_Request * lhs, const nero_msgs__srv__Enable_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // enable_request
  if (lhs->enable_request != rhs->enable_request) {
    return false;
  }
  return true;
}

bool
nero_msgs__srv__Enable_Request__copy(
  const nero_msgs__srv__Enable_Request * input,
  nero_msgs__srv__Enable_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // enable_request
  output->enable_request = input->enable_request;
  return true;
}

nero_msgs__srv__Enable_Request *
nero_msgs__srv__Enable_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nero_msgs__srv__Enable_Request * msg = (nero_msgs__srv__Enable_Request *)allocator.allocate(sizeof(nero_msgs__srv__Enable_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(nero_msgs__srv__Enable_Request));
  bool success = nero_msgs__srv__Enable_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
nero_msgs__srv__Enable_Request__destroy(nero_msgs__srv__Enable_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    nero_msgs__srv__Enable_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
nero_msgs__srv__Enable_Request__Sequence__init(nero_msgs__srv__Enable_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nero_msgs__srv__Enable_Request * data = NULL;

  if (size) {
    data = (nero_msgs__srv__Enable_Request *)allocator.zero_allocate(size, sizeof(nero_msgs__srv__Enable_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = nero_msgs__srv__Enable_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        nero_msgs__srv__Enable_Request__fini(&data[i - 1]);
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
nero_msgs__srv__Enable_Request__Sequence__fini(nero_msgs__srv__Enable_Request__Sequence * array)
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
      nero_msgs__srv__Enable_Request__fini(&array->data[i]);
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

nero_msgs__srv__Enable_Request__Sequence *
nero_msgs__srv__Enable_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nero_msgs__srv__Enable_Request__Sequence * array = (nero_msgs__srv__Enable_Request__Sequence *)allocator.allocate(sizeof(nero_msgs__srv__Enable_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = nero_msgs__srv__Enable_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
nero_msgs__srv__Enable_Request__Sequence__destroy(nero_msgs__srv__Enable_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    nero_msgs__srv__Enable_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
nero_msgs__srv__Enable_Request__Sequence__are_equal(const nero_msgs__srv__Enable_Request__Sequence * lhs, const nero_msgs__srv__Enable_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!nero_msgs__srv__Enable_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
nero_msgs__srv__Enable_Request__Sequence__copy(
  const nero_msgs__srv__Enable_Request__Sequence * input,
  nero_msgs__srv__Enable_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(nero_msgs__srv__Enable_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    nero_msgs__srv__Enable_Request * data =
      (nero_msgs__srv__Enable_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!nero_msgs__srv__Enable_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          nero_msgs__srv__Enable_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!nero_msgs__srv__Enable_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
nero_msgs__srv__Enable_Response__init(nero_msgs__srv__Enable_Response * msg)
{
  if (!msg) {
    return false;
  }
  // enable_response
  return true;
}

void
nero_msgs__srv__Enable_Response__fini(nero_msgs__srv__Enable_Response * msg)
{
  if (!msg) {
    return;
  }
  // enable_response
}

bool
nero_msgs__srv__Enable_Response__are_equal(const nero_msgs__srv__Enable_Response * lhs, const nero_msgs__srv__Enable_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // enable_response
  if (lhs->enable_response != rhs->enable_response) {
    return false;
  }
  return true;
}

bool
nero_msgs__srv__Enable_Response__copy(
  const nero_msgs__srv__Enable_Response * input,
  nero_msgs__srv__Enable_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // enable_response
  output->enable_response = input->enable_response;
  return true;
}

nero_msgs__srv__Enable_Response *
nero_msgs__srv__Enable_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nero_msgs__srv__Enable_Response * msg = (nero_msgs__srv__Enable_Response *)allocator.allocate(sizeof(nero_msgs__srv__Enable_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(nero_msgs__srv__Enable_Response));
  bool success = nero_msgs__srv__Enable_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
nero_msgs__srv__Enable_Response__destroy(nero_msgs__srv__Enable_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    nero_msgs__srv__Enable_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
nero_msgs__srv__Enable_Response__Sequence__init(nero_msgs__srv__Enable_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nero_msgs__srv__Enable_Response * data = NULL;

  if (size) {
    data = (nero_msgs__srv__Enable_Response *)allocator.zero_allocate(size, sizeof(nero_msgs__srv__Enable_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = nero_msgs__srv__Enable_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        nero_msgs__srv__Enable_Response__fini(&data[i - 1]);
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
nero_msgs__srv__Enable_Response__Sequence__fini(nero_msgs__srv__Enable_Response__Sequence * array)
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
      nero_msgs__srv__Enable_Response__fini(&array->data[i]);
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

nero_msgs__srv__Enable_Response__Sequence *
nero_msgs__srv__Enable_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nero_msgs__srv__Enable_Response__Sequence * array = (nero_msgs__srv__Enable_Response__Sequence *)allocator.allocate(sizeof(nero_msgs__srv__Enable_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = nero_msgs__srv__Enable_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
nero_msgs__srv__Enable_Response__Sequence__destroy(nero_msgs__srv__Enable_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    nero_msgs__srv__Enable_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
nero_msgs__srv__Enable_Response__Sequence__are_equal(const nero_msgs__srv__Enable_Response__Sequence * lhs, const nero_msgs__srv__Enable_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!nero_msgs__srv__Enable_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
nero_msgs__srv__Enable_Response__Sequence__copy(
  const nero_msgs__srv__Enable_Response__Sequence * input,
  nero_msgs__srv__Enable_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(nero_msgs__srv__Enable_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    nero_msgs__srv__Enable_Response * data =
      (nero_msgs__srv__Enable_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!nero_msgs__srv__Enable_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          nero_msgs__srv__Enable_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!nero_msgs__srv__Enable_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
