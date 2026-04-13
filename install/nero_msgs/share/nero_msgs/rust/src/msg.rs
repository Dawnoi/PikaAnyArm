#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to nero_msgs__msg__NeroStatusMsg

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::NeroStatusMsg::default())
  }
}

impl rosidl_runtime_rs::Message for NeroStatusMsg {
  type RmwMsg = super::msg::rmw::NeroStatusMsg;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ctrl_mode: msg.ctrl_mode,
        arm_status: msg.arm_status,
        mode_feedback: msg.mode_feedback,
        teach_status: msg.teach_status,
        motion_status: msg.motion_status,
        trajectory_num: msg.trajectory_num,
        err_code: msg.err_code,
        joint_1_angle_limit: msg.joint_1_angle_limit,
        joint_2_angle_limit: msg.joint_2_angle_limit,
        joint_3_angle_limit: msg.joint_3_angle_limit,
        joint_4_angle_limit: msg.joint_4_angle_limit,
        joint_5_angle_limit: msg.joint_5_angle_limit,
        joint_6_angle_limit: msg.joint_6_angle_limit,
        joint_7_angle_limit: msg.joint_7_angle_limit,
        communication_status_joint_1: msg.communication_status_joint_1,
        communication_status_joint_2: msg.communication_status_joint_2,
        communication_status_joint_3: msg.communication_status_joint_3,
        communication_status_joint_4: msg.communication_status_joint_4,
        communication_status_joint_5: msg.communication_status_joint_5,
        communication_status_joint_6: msg.communication_status_joint_6,
        communication_status_joint_7: msg.communication_status_joint_7,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      ctrl_mode: msg.ctrl_mode,
      arm_status: msg.arm_status,
      mode_feedback: msg.mode_feedback,
      teach_status: msg.teach_status,
      motion_status: msg.motion_status,
      trajectory_num: msg.trajectory_num,
      err_code: msg.err_code,
      joint_1_angle_limit: msg.joint_1_angle_limit,
      joint_2_angle_limit: msg.joint_2_angle_limit,
      joint_3_angle_limit: msg.joint_3_angle_limit,
      joint_4_angle_limit: msg.joint_4_angle_limit,
      joint_5_angle_limit: msg.joint_5_angle_limit,
      joint_6_angle_limit: msg.joint_6_angle_limit,
      joint_7_angle_limit: msg.joint_7_angle_limit,
      communication_status_joint_1: msg.communication_status_joint_1,
      communication_status_joint_2: msg.communication_status_joint_2,
      communication_status_joint_3: msg.communication_status_joint_3,
      communication_status_joint_4: msg.communication_status_joint_4,
      communication_status_joint_5: msg.communication_status_joint_5,
      communication_status_joint_6: msg.communication_status_joint_6,
      communication_status_joint_7: msg.communication_status_joint_7,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      ctrl_mode: msg.ctrl_mode,
      arm_status: msg.arm_status,
      mode_feedback: msg.mode_feedback,
      teach_status: msg.teach_status,
      motion_status: msg.motion_status,
      trajectory_num: msg.trajectory_num,
      err_code: msg.err_code,
      joint_1_angle_limit: msg.joint_1_angle_limit,
      joint_2_angle_limit: msg.joint_2_angle_limit,
      joint_3_angle_limit: msg.joint_3_angle_limit,
      joint_4_angle_limit: msg.joint_4_angle_limit,
      joint_5_angle_limit: msg.joint_5_angle_limit,
      joint_6_angle_limit: msg.joint_6_angle_limit,
      joint_7_angle_limit: msg.joint_7_angle_limit,
      communication_status_joint_1: msg.communication_status_joint_1,
      communication_status_joint_2: msg.communication_status_joint_2,
      communication_status_joint_3: msg.communication_status_joint_3,
      communication_status_joint_4: msg.communication_status_joint_4,
      communication_status_joint_5: msg.communication_status_joint_5,
      communication_status_joint_6: msg.communication_status_joint_6,
      communication_status_joint_7: msg.communication_status_joint_7,
    }
  }
}


// Corresponds to nero_msgs__msg__PosCmd

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::PosCmd::default())
  }
}

impl rosidl_runtime_rs::Message for PosCmd {
  type RmwMsg = super::msg::rmw::PosCmd;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x: msg.x,
        y: msg.y,
        z: msg.z,
        roll: msg.roll,
        pitch: msg.pitch,
        yaw: msg.yaw,
        gripper: msg.gripper,
        mode1: msg.mode1,
        mode2: msg.mode2,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      x: msg.x,
      y: msg.y,
      z: msg.z,
      roll: msg.roll,
      pitch: msg.pitch,
      yaw: msg.yaw,
      gripper: msg.gripper,
      mode1: msg.mode1,
      mode2: msg.mode2,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x: msg.x,
      y: msg.y,
      z: msg.z,
      roll: msg.roll,
      pitch: msg.pitch,
      yaw: msg.yaw,
      gripper: msg.gripper,
      mode1: msg.mode1,
      mode2: msg.mode2,
    }
  }
}


