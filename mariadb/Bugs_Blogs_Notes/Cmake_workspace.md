# Cmake how to

- Traditional Cmake uses "targets"
  - Build requirements (to build the targets - `PRIVATE` properties)
    
  - Usage requirements (to use the targets -  `INTERFACE` properties)
  
  - Build and usage requirements (`PUBLIC` properties)
 
# Example:
File struct:
```bash
.
├── CMakeLists.txt
├── app
│   ├── CMakeLists.txt
│   └── src
│       ├── key-file.cpp
│       └── main.cpp
├── external
│   ├── CMakeLists.txt
│   ├── boost
│   │   └── CMakeLists.txt
│   └── boost_outcome
│       └── CMakeLists.txt
└── library
    ├── CMakeLists.txt
    ├── include
    │   ├── Math.h
    │   └── MathAPI.h
    └── src
        ├── BasicMath.cpp
        ├── ExtendedMath.cpp
        └── HeavyMath.cpp

```

## `./external/boost/CMakeListst.txt`
```cmake
./external/boost/CMakeListst.txt
set(BOOST_VERSION 1.58.0)

# Settings for correct Boost libraries
set( Boost_USE_STATIC_LIBS FALSE )
set( Boost_USE_MULTITHREADED TRUE )
set( Boost_USE_STATIC_RUNTIME FALSE )
set( Boost_ADDITIONAL VERSINS "${BOOST_VERSION}" )
set( Boost_COMPILER "-gcc" )
find_package(Boost ${BOOST_VERSION} EXACT REQUIRED COMPONENTES program_options graph)
```

- If package is found:
  - `Boost_INCLUDE_DIRS` - contains include-path
  - `Boost_LIBRARIES` - contains file-path to shared libraries
  -  `IMPORTED` targets created (carry and can propagate their usage requirements, `non-global` scope):
    - `Boost::boost`
    - `Boost::program_options`
    - `Boost::graph`
    
    
## - `./CMakeListst.txt`
```cmake
cmake_minimum_required ( VERSOIN 2.8.10)

project ( Example_for_CMake )
set ( VERSION 2.8.10 )
set ( DESCRIPTION "EXAMPLE")

# alwaysuse  -fPIC/-fPIE option
set ( CMAKE_POSITION_INDEPENDENT_CODE ON)

# Make external libraries globally available
add_subdirectory( external ) # doesn't work for Boost
# update_1:
include ( external/boost/CMakeLists.txt)


# Create targets for building the (local) libraries
add_subdirectory ( library )

# Create the targets for the entire app

add_subdirectory ( app )
```

### Update 2 IMPORTED global scope
- Boost `./external/boost/CMakeListst.txt` 
```cmake
# same as above +
if ( Boost_FOUND )

  set_target_properties ( Boost::boost
                          Boost::program_options
                          Boost::graph
      PROPERTIES IMPORTED_GLOBAL TRUE)
end_if()
```

- Top file `./CMakeListst.txt` update_2:
```cmake
# Make external libraries globally available
add_subdirectory( external ) # NOW works for Boost too
# update_1 is no longer needed, can be removed
~include ( external/boost/CMakeLists.txt)~
```


- Note: Promted/Global `IMPORTED` targets cannot be demoted
- NOte: Variables created by `find_package` are not promoted to global scope

## - `./external/CMakeListst.txt`
```cmake
# Now we can use it
add_subdirectory ( boost )
add_subdirectory ( boost_outcome )

```



# Modules
CMake modules are files that define additional functionality for CMake. 
They can be used to add custom build rules, define new variables, and configure third-party libraries. 

You can use the CMAKE_MODULE_PATH variable to specify one or more directories where CMake should look for modules. By default, CMake searches for modules in the following directories:

The Modules subdirectory of the current source directory
The Modules subdirectory of the CMake installation
The directories listed in the CMAKE_MODULE_PATH variable.
So, if you have custom modules that are stored in a non-default location, you can add the directory to CMAKE_MODULE_PATH to make them available to CMake.



















