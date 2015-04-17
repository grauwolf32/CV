#!/bin/bash

echo "Compiling $2..."
echo "cmake_minimum_required(VERSION 2.8) \n\
project( $1 ) \n\
find_package( OpenCV REQUIRED )
include_directories( \${OpenCV_INCLUDE_DIRS} ) \n\
add_executable( $1 $2 ) \n\
target_link_libraries( $1 \${OpenCV_LIBS} )\n" > CMakeLists.txt

cmake .
make 

rm -r CMakeFiles
ls | grep "ake"| xargs rm
echo "Done!"




