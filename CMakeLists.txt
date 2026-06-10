cmake_minimum_required(VERSION 3.22)

project(docker_googletest_cpp LANGUAGES CXX)

option(ENABLE_COVERAGE "Enable GCC/Clang coverage flags" OFF)
option(ENABLE_SANITIZERS "Enable Address/Undefined sanitizers" OFF)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
endif()

# -------------------------------------------------------------------
# Compiler warnings compatible Windows/MSVC and Linux/GCC/Clang
# -------------------------------------------------------------------
function(enable_project_warnings target_name)
  if(MSVC)
    target_compile_options(${target_name} PRIVATE /W4 /permissive-)
  else()
    target_compile_options(${target_name} PRIVATE -Wall -Wextra -Wpedantic)
  endif()
endfunction()

# -------------------------------------------------------------------
# Core library
# -------------------------------------------------------------------
add_library(calculator_core
  src/Calculator.cpp
  src/ExpressionParser.cpp
  src/CalculatorService.cpp
)

target_include_directories(calculator_core PUBLIC include)

enable_project_warnings(calculator_core)

# -------------------------------------------------------------------
# Coverage flags, only for GCC/Clang
# -------------------------------------------------------------------
if(ENABLE_COVERAGE AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(calculator_core PUBLIC --coverage -O0 -g)
  target_link_options(calculator_core PUBLIC --coverage)
endif()

# -------------------------------------------------------------------
# Sanitizers, only for GCC/Clang
# -------------------------------------------------------------------
if(ENABLE_SANITIZERS AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(calculator_core PUBLIC
    -fsanitize=address,undefined
    -fno-omit-frame-pointer
    -g
  )
  target_link_options(calculator_core PUBLIC
    -fsanitize=address,undefined
  )
endif()

# -------------------------------------------------------------------
# CLI executable
# -------------------------------------------------------------------
add_executable(calculator_cli
  src/main.cpp
)

target_link_libraries(calculator_cli PRIVATE
  calculator_core
)

enable_project_warnings(calculator_cli)

# -------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------
include(CTest)

if(BUILD_TESTING)

  include(FetchContent)

  # Prevent GoogleTest from overriding MSVC runtime settings.
  # Important under Windows / Visual Studio.
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

  FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.15.2.zip
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  )

  FetchContent_MakeAvailable(googletest)

  include(GoogleTest)

  add_executable(calculator_tests
    tests/CalculatorTest.cpp
    tests/ExpressionParserTest.cpp
    tests/CalculatorParameterizedTest.cpp
    tests/CalculatorMockTest.cpp
  )

  target_link_libraries(calculator_tests PRIVATE
    calculator_core
    GTest::gtest
    GTest::gtest_main
    GTest::gmock
  )

  enable_project_warnings(calculator_tests)

  if(ENABLE_COVERAGE AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(calculator_tests PUBLIC --coverage -O0 -g)
    target_link_options(calculator_tests PUBLIC --coverage)
  endif()

  if(ENABLE_SANITIZERS AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(calculator_tests PUBLIC
      -fsanitize=address,undefined
      -fno-omit-frame-pointer
      -g
    )
    target_link_options(calculator_tests PUBLIC
      -fsanitize=address,undefined
    )
  endif()

  gtest_discover_tests(calculator_tests
    DISCOVERY_TIMEOUT 30
    XML_OUTPUT_DIR ${CMAKE_BINARY_DIR}/test-results
  )

endif()