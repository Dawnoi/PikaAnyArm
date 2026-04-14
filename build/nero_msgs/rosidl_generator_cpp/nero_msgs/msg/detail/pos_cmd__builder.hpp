// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from nero_msgs:msg/PosCmd.idl
// generated code does not contain a copyright notice

#ifndef NERO_MSGS__MSG__DETAIL__POS_CMD__BUILDER_HPP_
#define NERO_MSGS__MSG__DETAIL__POS_CMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "nero_msgs/msg/detail/pos_cmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace nero_msgs
{

namespace msg
{

namespace builder
{

class Init_PosCmd_mode2
{
public:
  explicit Init_PosCmd_mode2(::nero_msgs::msg::PosCmd & msg)
  : msg_(msg)
  {}
  ::nero_msgs::msg::PosCmd mode2(::nero_msgs::msg::PosCmd::_mode2_type arg)
  {
    msg_.mode2 = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nero_msgs::msg::PosCmd msg_;
};

class Init_PosCmd_mode1
{
public:
  explicit Init_PosCmd_mode1(::nero_msgs::msg::PosCmd & msg)
  : msg_(msg)
  {}
  Init_PosCmd_mode2 mode1(::nero_msgs::msg::PosCmd::_mode1_type arg)
  {
    msg_.mode1 = std::move(arg);
    return Init_PosCmd_mode2(msg_);
  }

private:
  ::nero_msgs::msg::PosCmd msg_;
};

class Init_PosCmd_gripper
{
public:
  explicit Init_PosCmd_gripper(::nero_msgs::msg::PosCmd & msg)
  : msg_(msg)
  {}
  Init_PosCmd_mode1 gripper(::nero_msgs::msg::PosCmd::_gripper_type arg)
  {
    msg_.gripper = std::move(arg);
    return Init_PosCmd_mode1(msg_);
  }

private:
  ::nero_msgs::msg::PosCmd msg_;
};

class Init_PosCmd_yaw
{
public:
  explicit Init_PosCmd_yaw(::nero_msgs::msg::PosCmd & msg)
  : msg_(msg)
  {}
  Init_PosCmd_gripper yaw(::nero_msgs::msg::PosCmd::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return Init_PosCmd_gripper(msg_);
  }

private:
  ::nero_msgs::msg::PosCmd msg_;
};

class Init_PosCmd_pitch
{
public:
  explicit Init_PosCmd_pitch(::nero_msgs::msg::PosCmd & msg)
  : msg_(msg)
  {}
  Init_PosCmd_yaw pitch(::nero_msgs::msg::PosCmd::_pitch_type arg)
  {
    msg_.pitch = std::move(arg);
    return Init_PosCmd_yaw(msg_);
  }

private:
  ::nero_msgs::msg::PosCmd msg_;
};

class Init_PosCmd_roll
{
public:
  explicit Init_PosCmd_roll(::nero_msgs::msg::PosCmd & msg)
  : msg_(msg)
  {}
  Init_PosCmd_pitch roll(::nero_msgs::msg::PosCmd::_roll_type arg)
  {
    msg_.roll = std::move(arg);
    return Init_PosCmd_pitch(msg_);
  }

private:
  ::nero_msgs::msg::PosCmd msg_;
};

class Init_PosCmd_z
{
public:
  explicit Init_PosCmd_z(::nero_msgs::msg::PosCmd & msg)
  : msg_(msg)
  {}
  Init_PosCmd_roll z(::nero_msgs::msg::PosCmd::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_PosCmd_roll(msg_);
  }

private:
  ::nero_msgs::msg::PosCmd msg_;
};

class Init_PosCmd_y
{
public:
  explicit Init_PosCmd_y(::nero_msgs::msg::PosCmd & msg)
  : msg_(msg)
  {}
  Init_PosCmd_z y(::nero_msgs::msg::PosCmd::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_PosCmd_z(msg_);
  }

private:
  ::nero_msgs::msg::PosCmd msg_;
};

class Init_PosCmd_x
{
public:
  Init_PosCmd_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PosCmd_y x(::nero_msgs::msg::PosCmd::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_PosCmd_y(msg_);
  }

private:
  ::nero_msgs::msg::PosCmd msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::nero_msgs::msg::PosCmd>()
{
  return nero_msgs::msg::builder::Init_PosCmd_x();
}

}  // namespace nero_msgs

#endif  // NERO_MSGS__MSG__DETAIL__POS_CMD__BUILDER_HPP_
