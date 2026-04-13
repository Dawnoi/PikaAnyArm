// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from nero_msgs:srv/Enable.idl
// generated code does not contain a copyright notice

#ifndef NERO_MSGS__SRV__DETAIL__ENABLE__BUILDER_HPP_
#define NERO_MSGS__SRV__DETAIL__ENABLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "nero_msgs/srv/detail/enable__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace nero_msgs
{

namespace srv
{

namespace builder
{

class Init_Enable_Request_enable_request
{
public:
  Init_Enable_Request_enable_request()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::nero_msgs::srv::Enable_Request enable_request(::nero_msgs::srv::Enable_Request::_enable_request_type arg)
  {
    msg_.enable_request = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nero_msgs::srv::Enable_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::nero_msgs::srv::Enable_Request>()
{
  return nero_msgs::srv::builder::Init_Enable_Request_enable_request();
}

}  // namespace nero_msgs


namespace nero_msgs
{

namespace srv
{

namespace builder
{

class Init_Enable_Response_enable_response
{
public:
  Init_Enable_Response_enable_response()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::nero_msgs::srv::Enable_Response enable_response(::nero_msgs::srv::Enable_Response::_enable_response_type arg)
  {
    msg_.enable_response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nero_msgs::srv::Enable_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::nero_msgs::srv::Enable_Response>()
{
  return nero_msgs::srv::builder::Init_Enable_Response_enable_response();
}

}  // namespace nero_msgs

#endif  // NERO_MSGS__SRV__DETAIL__ENABLE__BUILDER_HPP_
