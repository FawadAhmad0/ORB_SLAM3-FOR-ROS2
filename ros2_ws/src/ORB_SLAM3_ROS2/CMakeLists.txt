cmake_minimum_required(VERSION 3.5)

# Ignore active Conda environment paths to prevent linking incompatibilities (e.g. libgdal, libcurl, libtiff mismatches)
if(DEFINED ENV{CONDA_PREFIX})
  list(APPEND CMAKE_IGNORE_PREFIX_PATH "$ENV{CONDA_PREFIX}")
  list(APPEND CMAKE_IGNORE_PATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/bin" "$ENV{CONDA_PREFIX}/include")
endif()

project(orbslam3)

# You should set the PYTHONPATH to your own python site-packages path
set(ENV{PYTHONPATH} "/opt/ros/humble/lib/python3.10/site-packages")

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/CMakeModules)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(message_filters REQUIRED)
find_package(Sophus REQUIRED)
find_package(Pangolin REQUIRED)
find_package(ORB_SLAM3 REQUIRED)

# Find only the OpenCV components ORB-SLAM3 actually needs.
# Using all OpenCV modules pulls in contrib libs (e.g. opencv_ovis/sfm)
# that transitively depend on libgdal, causing unresolved curl/tiff symbols.
find_package(OpenCV REQUIRED COMPONENTS core imgproc highgui features2d calib3d imgcodecs)

include_directories(
  include
  ${ORB_SLAM3_ROOT_DIR}/include
  ${ORB_SLAM3_ROOT_DIR}/include/CameraModels
  ${ORB_SLAM3_ROOT_DIR}/Thirdparty/Sophus
)

link_directories(
  include
)

add_executable(mono
  src/monocular/mono.cpp
  src/monocular/monocular-slam-node.cpp
)
ament_target_dependencies(mono rclcpp sensor_msgs cv_bridge ORB_SLAM3 Pangolin)
target_link_libraries(mono ${OpenCV_LIBS} curl tiff)

add_executable(rgbd
  src/rgbd/rgbd.cpp
  src/rgbd/rgbd-slam-node.cpp
)
ament_target_dependencies(rgbd rclcpp sensor_msgs cv_bridge message_filters ORB_SLAM3 Pangolin)
target_link_libraries(rgbd ${OpenCV_LIBS} curl tiff)

add_executable(stereo
  src/stereo/stereo.cpp
  src/stereo/stereo-slam-node.cpp
)
ament_target_dependencies(stereo rclcpp sensor_msgs cv_bridge message_filters ORB_SLAM3 Pangolin)
target_link_libraries(stereo ${OpenCV_LIBS} curl tiff)

add_executable(stereo-inertial
  src/stereo-inertial/stereo-inertial.cpp
  src/stereo-inertial/stereo-inertial-node.cpp
)
ament_target_dependencies(stereo-inertial rclcpp sensor_msgs cv_bridge ORB_SLAM3 Pangolin)
target_link_libraries(stereo-inertial ${OpenCV_LIBS} curl tiff)

install(TARGETS mono rgbd stereo stereo-inertial DESTINATION lib/${PROJECT_NAME})

# Install launch files.
#install(DIRECTORY launch config vocabulary
#  DESTINATION share/${PROJECT_NAME}/)

ament_package()

