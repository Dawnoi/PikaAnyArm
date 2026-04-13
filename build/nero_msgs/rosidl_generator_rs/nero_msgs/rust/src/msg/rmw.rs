#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "nero_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__nero_msgs__msg__NeroStatusMsg() -> *const std::ffi::c_void;
}

#[link(name = "nero_msgs__rosidl_generator_c")]
extern "C" {
    fn nero_msgs__msg__NeroStatusMsg__init(msg: *mut NeroStatusMsg) -> bool;
    fn nero_msgs__msg__NeroStatusMsg__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<NeroStatusMsg>, size: usize) -> bool;
    fn nero_msgs__msg__NeroStatusMsg__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<NeroStatusMsg>);
    fn nero_msgs__msg__NeroStatusMsg__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<NeroStatusMsg>, out_seq: *mut rosidl_runtime_rs::Sequence<NeroStatusMsg>) -> bool;
}

// Corresponds to nero_msgs__msg__NeroStatusMsg
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct NeroStatusMsg {

    // This member is not documented.
    #[allow(missing_docs)]
    pub ctrl_mode: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub arm_status: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mode_feedback: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub teach_status: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub motion_status: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub trajectory_num: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub err_code: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_1_angle_limit: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_2_angle_limit: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_3_angle_limit: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_4_angle_limit: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_5_angle_limit: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_6_angle_limit: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_7_angle_limit: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub communication_status_joint_1: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub communication_status_joint_2: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub communication_status_joint_3: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub communication_status_joint_4: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub communication_status_joint_5: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub communication_status_joint_6: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub communication_status_joint_7: bool,

}



impl Default for NeroStatusMsg {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !nero_msgs__msg__NeroStatusMsg__init(&mut msg as *mut _) {
        panic!("Call to nero_msgs__msg__NeroStatusMsg__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for NeroStatusMsg {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__msg__NeroStatusMsg__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__msg__NeroStatusMsg__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__msg__NeroStatusMsg__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for NeroStatusMsg {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for NeroStatusMsg where Self: Sized {
  const TYPE_NAME: &'static str = "nero_msgs/msg/NeroStatusMsg";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__nero_msgs__msg__NeroStatusMsg() }
  }
}


#[link(name = "nero_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__nero_msgs__msg__PosCmd() -> *const std::ffi::c_void;
}

#[link(name = "nero_msgs__rosidl_generator_c")]
extern "C" {
    fn nero_msgs__msg__PosCmd__init(msg: *mut PosCmd) -> bool;
    fn nero_msgs__msg__PosCmd__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PosCmd>, size: usize) -> bool;
    fn nero_msgs__msg__PosCmd__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PosCmd>);
    fn nero_msgs__msg__PosCmd__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PosCmd>, out_seq: *mut rosidl_runtime_rs::Sequence<PosCmd>) -> bool;
}

// Corresponds to nero_msgs__msg__PosCmd
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PosCmd {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub roll: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pitch: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub yaw: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gripper: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mode1: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mode2: i32,

}



impl Default for PosCmd {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !nero_msgs__msg__PosCmd__init(&mut msg as *mut _) {
        panic!("Call to nero_msgs__msg__PosCmd__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PosCmd {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__msg__PosCmd__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__msg__PosCmd__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__msg__PosCmd__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PosCmd {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PosCmd where Self: Sized {
  const TYPE_NAME: &'static str = "nero_msgs/msg/PosCmd";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__nero_msgs__msg__PosCmd() }
  }
}


