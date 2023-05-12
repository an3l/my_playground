When running {{cmake --trace-extend}}, with {{cmake}} version 3.16, noted error
{code:noformat}
/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2543):  set(tag MD5=e77873199e897ca9f780479ad68e25b1 )
/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2544):  configure_file(/usr/share/cmake-3.16/Modules/RepositoryInfo.txt.in /home/anel/GitHub/mariadb/server/build/connect-java/extra/libfmt/src/libfmt-stamp/libfmt-urlinfo.txt @ONLY )
/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2549):  list(APPEND depends /home/anel/GitHub/mariadb/server/build/connect-java/extra/libfmt/src/libfmt-stamp/libfmt-urlinfo.txt )
/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2551):  list(LENGTH url url_list_length )
/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2552):  if(NOT 1 STREQUAL 1 )
/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2563):  if(IS_DIRECTORY https://github.com/fmtlib/fmt/releases/download/8.0.1/fmt-8.0.1.zip )
/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2568):  else()
/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2569):  get_property(no_extract TARGET libfmt PROPERTY _EP_DOWNLOAD_NO_EXTRACT SET )
/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2570):  if(https://github.com/fmtlib/fmt/releases/download/8.0.1/fmt-8.0.1.zip MATCHES ^[a-z]+:// )
/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2572):  if(x STREQUAL x )
/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2573):  set(fname https://github.com/fmtlib/fmt/releases/download/8.0.1/fmt-8.0.1.zip )
CMake Error at /usr/share/cmake-3.16/Modules/ExternalProject.cmake:2575 (if):
  Syntax error in cmake code when parsing string

    ([^/\?#]+(\.|=)(7z|tar|tar\.bz2|tar\.gz|tar\.xz|tbz2|tgz|txz|zip))([/?#].*)?$

  Invalid escape sequence \?
Call Stack (most recent call first):
  /usr/share/cmake-3.16/Modules/ExternalProject.cmake:3236 (_ep_add_download_command)
  cmake/libfmt.cmake:15 (ExternalProject_Add)
  cmake/libfmt.cmake:47 (BUNDLE_LIBFMT)
  CMakeLists.txt:396 (CHECK_LIBFMT)


/usr/share/cmake-3.16/Modules/ExternalProject.cmake(2575):  if(https://github.com/fmtlib/fmt/releases/download/8.0.1/fmt-8.0.1.zip MATCHES ([^/\?#]+(\.|=)(7z|tar|tar\.bz2|tar\.gz|tar\.xz|tbz2|tgz|txz|zip))([/?#].*)?$ )
-- Configuring incomplete, errors occurred!
See also "/home/anel/GitHub/mariadb/server/build/connect-java/CMakeFiles/CMakeOutput.log".
See also "/home/anel/GitHub/mariadb/server/build/connect-java/CMakeFiles/CMakeError.log".
{code}

However cmake regex is good. 
Tested: https://regexr.com/7dmes

This seems to be {{cmake}} bug. 
New patch [3351b7b82c2|https://gitlab.kitware.com/cmake/cmake/-/commit/3351b7b82c2] from {{cmake}} 3.24+ works, I have verified and tested.


Not sure should we indicate that in our codebase somehow?


### Install new version of cmake
```bash
$ sudo apt remove cmake
$ # Install from source
$ wget https://github.com/Kitware/CMake/releases/download/v3.26.3/cmake-3.26.3.tar.gz
$ tar xzvf cmake-3.26.3.tar.gz 
$ cd cmake-3.26.3/
$ sudo ./bootstrap
$ sudo make install
$ cmake --version #
```
