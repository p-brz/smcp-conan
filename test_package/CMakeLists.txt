project(SmcpExample1)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(example1 examples/example-1.c)
target_link_libraries(example1 ${CONAN_LIBS})

add_executable(example4 examples/example-4.c)
target_link_libraries(example4 ${CONAN_LIBS})
