cmake_minimum_required(VERSION 2.8.3)
project(loam_ouster)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  sensor_msgs
  roscpp
  pcl_conversions
  rospy
  std_msgs
  tf)

SET("PCL_DIR" "/home/snake/library/pcl-master/build/lib")
find_package(PCL REQUIRED)

#SET("Eigen3_DIR" "/home/snake/library/eigen-eigen-3.3.3/build/")
find_package(Eigen3 REQUIRED)
find_package(OpenCV REQUIRED)
SET("PCL_INCLUDE_DIRS" "/home/snake/library/pcl-master/build/include/")
include_directories(
  include
	${catkin_INCLUDE_DIRS} 
	${EIGEN3_INCLUDE_DIR}
	${PCL_INCLUDE_DIRS})

catkin_package(
  CATKIN_DEPENDS geometry_msgs nav_msgs roscpp rospy std_msgs
  DEPENDS EIGEN3 PCL
  INCLUDE_DIRS include
  LIBRARIES loam
)

#add_definitions( -march=native )


add_subdirectory(src/lib)

add_executable(multiScanRegistration src/multi_scan_registration_node.cpp)
target_link_libraries(multiScanRegistration ${catkin_LIBRARIES} ${PCL_LIBRARIES} loam )

add_executable(laserOdometry src/laser_odometry_node.cpp)
target_link_libraries(laserOdometry ${catkin_LIBRARIES} ${PCL_LIBRARIES} loam )

add_executable(laserMapping src/laser_mapping_node.cpp)
target_link_libraries(laserMapping ${catkin_LIBRARIES} ${PCL_LIBRARIES} loam )

add_executable(transformMaintenance src/transform_maintenance_node.cpp)
target_link_libraries(transformMaintenance ${catkin_LIBRARIES} ${PCL_LIBRARIES} loam )

if (CATKIN_ENABLE_TESTING)
  find_package(rostest REQUIRED)
  # TODO: Download test data
  catkin_download_test_data(${PROJECT_NAME}_test_data.tar.gz
    https://dl.dropboxusercontent.com/s/y4hn486461tfmpm/velodyne_loam_test_data.tar.gz
    MD5 3d5194e6981975588b7a93caebf79ba4)
  add_custom_target(${PROJECT_NAME}_test_data
    COMMAND ${CMAKE_COMMAND} -E tar -xzf velodyne_loam_test_data.tar.gz
    DEPENDS ${PROJECT_NAME}_test_data.tar.gz)
  configure_file(tests/loam.test.in
                 ${PROJECT_BINARY_DIR}/test/loam.test)
  add_rostest(${PROJECT_BINARY_DIR}/test/loam.test
    DEPENDENCIES
      ${PROJECT_NAME}_test_data
      multiScanRegistration
      laserOdometry
      laserMapping
      transformMaintenance)
endif()


