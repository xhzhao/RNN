IF (APPLE)
    cmake_minimum_required(VERSION 3.4)
ELSE()
    cmake_minimum_required(VERSION 2.8)
ENDIF()

project(rnn_release)

IF (NOT APPLE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp -O2")
ENDIF()

IF (APPLE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O2")
    add_definitions(-DAPPLE)
ENDIF()

include_directories(include)


option(WITH_OMP "compile intel-RNN with openmp." ON)

if(NOT WITH_OMP)
    add_definitions(-DCTC_DISABLE_OMP)
endif()

# need to be at least 30 or __shfl_down in reduce wont compile

FIND_PACKAGE(Torch)

MESSAGE(STATUS "Torch found ${Torch_DIR}")

IF (APPLE)
    EXEC_PROGRAM(uname ARGS -v  OUTPUT_VARIABLE DARWIN_VERSION)
    STRING(REGEX MATCH "[0-9]+" DARWIN_VERSION ${DARWIN_VERSION})
    MESSAGE(STATUS "DARWIN_VERSION=${DARWIN_VERSION}")

    #for el capitain have to use rpath

    IF (DARWIN_VERSION LESS 15)
        set(CMAKE_SKIP_RPATH TRUE)
    ENDIF ()

ELSE()
    #always skip for linux
    set(CMAKE_SKIP_RPATH TRUE)
ENDIF()

SET(WITH_CPU TRUE)
IF (WITH_CPU)
    MESSAGE(STATUS "Building shared library with no GPU support")

    if (NOT APPLE)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O2")
    ENDIF()

    ADD_LIBRARY(intelRNN SHARED src/rnn_entrypoint.cpp)

    add_executable(test_cpu tests/test_cpu.cpp )
    TARGET_LINK_LIBRARIES(test_cpu intelRNN)
    SET_TARGET_PROPERTIES(test_cpu PROPERTIES COMPILE_FLAGS "${CMAKE_CXX_FLAGS} --std=c++11")

    INSTALL(TARGETS intelRNN
            RUNTIME DESTINATION "bin"
            LIBRARY DESTINATION "lib"
            ARCHIVE DESTINATION "lib")

    INSTALL(FILES include/rnn.h DESTINATION "include")

    SET(Torch_FOUND FALSE)
    IF (Torch_FOUND)
        MESSAGE(STATUS "Building Torch Bindings with no GPU support")
        add_definitions(-DTORCH_NOGPU)
        INCLUDE_DIRECTORIES(${Torch_INSTALL_INCLUDE} ${Torch_INSTALL_INCLUDE}/TH)

        TARGET_LINK_LIBRARIES(intelRNN luajit luaT TH)

        INSTALL(TARGETS intelRNN
                RUNTIME DESTINATION "${Torch_INSTALL_BIN_SUBDIR}"
                LIBRARY DESTINATION "${Torch_INSTALL_LIB_SUBDIR}"
                ARCHIVE DESTINATION "${Torch_INSTALL_LIB_SUBDIR}")

        SET(src torch_binding/binding.cpp torch_binding/utils.c)
        SET(luasrc torch_binding/init.lua)

        ADD_TORCH_PACKAGE(intel_RNN "${src}" "${luasrc}")
        IF (APPLE)
            TARGET_LINK_LIBRARIES(intel_RNN intelRNN luajit luaT TH)
        ELSE()
            TARGET_LINK_LIBRARIES(intel_RNN intelRNN luajit luaT TH gomp)
        ENDIF()
    ENDIF()

ENDIF()


