#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "nero_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__nero_msgs__srv__Enable_Request() -> *const std::ffi::c_void;
}

#[link(name = "nero_msgs__rosidl_generator_c")]
extern "C" {
    fn nero_msgs__srv__Enable_Request__init(msg: *mut Enable_Request) -> bool;
    fn nero_msgs__srv__Enable_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Enable_Request>, size: usize) -> bool;
    fn nero_msgs__srv__Enable_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Enable_Request>);
    fn nero_msgs__srv__Enable_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Enable_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<Enable_Request>) -> bool;
}

// Corresponds to nero_msgs__srv__Enable_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Enable_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_request: bool,

}



impl Default for Enable_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !nero_msgs__srv__Enable_Request__init(&mut msg as *mut _) {
        panic!("Call to nero_msgs__srv__Enable_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Enable_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__srv__Enable_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__srv__Enable_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__srv__Enable_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Enable_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Enable_Request where Self: Sized {
  const TYPE_NAME: &'static str = "nero_msgs/srv/Enable_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__nero_msgs__srv__Enable_Request() }
  }
}


#[link(name = "nero_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__nero_msgs__srv__Enable_Response() -> *const std::ffi::c_void;
}

#[link(name = "nero_msgs__rosidl_generator_c")]
extern "C" {
    fn nero_msgs__srv__Enable_Response__init(msg: *mut Enable_Response) -> bool;
    fn nero_msgs__srv__Enable_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Enable_Response>, size: usize) -> bool;
    fn nero_msgs__srv__Enable_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Enable_Response>);
    fn nero_msgs__srv__Enable_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Enable_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<Enable_Response>) -> bool;
}

// Corresponds to nero_msgs__srv__Enable_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Enable_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_response: bool,

}



impl Default for Enable_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !nero_msgs__srv__Enable_Response__init(&mut msg as *mut _) {
        panic!("Call to nero_msgs__srv__Enable_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Enable_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__srv__Enable_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__srv__Enable_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { nero_msgs__srv__Enable_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Enable_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Enable_Response where Self: Sized {
  const TYPE_NAME: &'static str = "nero_msgs/srv/Enable_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__nero_msgs__srv__Enable_Response() }
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


