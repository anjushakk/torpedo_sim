cmake_minimum_required(VERSION 3.8)
project(torpedo_sim)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 1. Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
# Add these for Gazebo integration
find_package(ros_gz_sim REQUIRED)
find_package(ros_gz_bridge REQUIRED)

# 2. Install directories (Crucial for simulation)
# This moves your files from 'src' to 'install' so ROS 2 can find them
install(DIRECTORY
  launch
  models
  worlds
  config
  DESTINATION share/${PROJECT_NAME}
)
# Install the teleop script
install(PROGRAMS
  scripts/teleop_node.py
  DESTINATION lib/${PROJECT_NAME}
)
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# 3. Always keep this at the very end
ament_package()
