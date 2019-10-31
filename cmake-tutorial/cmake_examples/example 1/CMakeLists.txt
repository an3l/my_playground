cmake_minimum_required(VERSION 2.4)

project(hello_world)

add_executable(app main.cpp)

# Out-of-source build: mkdir bld, cd bld, cmake .. (by default we are using MSVSC generator), cmake --build . --config Debug 
# Output will be visible in bld/Debug/app.exe
# To remove dir in windows => rd /s /q "bld"
# To echo dir in windows => echo %cd%
# To show process in windows => tasklist
# To kill process in windows => taskkill /F /PID #PID