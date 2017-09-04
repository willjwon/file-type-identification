cmake_minimum_required(VERSION 3.8)
project(FileFragmentGenerator)

set(CMAKE_CXX_STANDARD 17)

set(SOURCE_FILES main.cpp json.hpp FileManager.cpp FileManager.hpp FragmentManager.cpp FragmentManager.hpp)
add_executable(FileFragmentGenerator ${SOURCE_FILES})