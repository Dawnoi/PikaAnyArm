#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to nero_msgs__srv__Enable_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Enable_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_request: bool,

}



impl Default for Enable_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Enable_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Enable_Request {
  type RmwMsg = super::srv::rmw::Enable_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        enable_request: msg.enable_request,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      enable_request: msg.enable_request,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      enable_request: msg.enable_request,
    }
  }
}


// Corresponds to nero_msgs__srv__Enable_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Enable_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_response: bool,

}



impl Default for Enable_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Enable_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Enable_Response {
  type RmwMsg = super::srv::rmw::Enable_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        enable_response: msg.enable_response,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      enable_response: msg.enable_response,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      enable_response: msg.enable_response,
    }
  }
}






#[link(name = "nero_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__nero_msgs__srv__Enable() -> *const std::ffi::c_void;
}

// Corresponds to nero_msgs__srv__Enable
#[allow(missing_docs, non_camel_case_types)]
pub struct Enable;

impl rosidl_runtime_rs::Service for Enable {
    type Request = Enable_Request;
    type Response = Enable_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__nero_msgs__srv__Enable() }
    }
}


