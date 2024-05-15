// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interface_package:srv/ArucoDetectSrv.idl
// generated code does not contain a copyright notice

#ifndef INTERFACE_PACKAGE__SRV__DETAIL__ARUCO_DETECT_SRV__BUILDER_HPP_
#define INTERFACE_PACKAGE__SRV__DETAIL__ARUCO_DETECT_SRV__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interface_package/srv/detail/aruco_detect_srv__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interface_package
{

namespace srv
{

namespace builder
{

class Init_ArucoDetectSrv_Request_id
{
public:
  Init_ArucoDetectSrv_Request_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interface_package::srv::ArucoDetectSrv_Request id(::interface_package::srv::ArucoDetectSrv_Request::_id_type arg)
  {
    msg_.id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interface_package::srv::ArucoDetectSrv_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::interface_package::srv::ArucoDetectSrv_Request>()
{
  return interface_package::srv::builder::Init_ArucoDetectSrv_Request_id();
}

}  // namespace interface_package


namespace interface_package
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::interface_package::srv::ArucoDetectSrv_Response>()
{
  return ::interface_package::srv::ArucoDetectSrv_Response(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace interface_package

#endif  // INTERFACE_PACKAGE__SRV__DETAIL__ARUCO_DETECT_SRV__BUILDER_HPP_
