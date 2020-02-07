# We name our project
project(greeting)

# This tells CMake to compile main.c and name it main
add_executable(greeting main.c)

# We add the file as a static library called TimeLibrary
#add_library(TimeLibrary STATIC print_time.c)

# Add library as a shared library
add_library(TimeLibrary SHARED print_time.c)

# This tells CMake to link greeting with the TimeLibrary
target_link_libraries(greeting TimeLibrary)
