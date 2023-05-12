# Bug 1 - cmake

When compiled with Connect
```
```
cmake outputs good message:
```
The following features have been enabled:

 * CONNECT_VCT, Support for VCT in the CONNECT storage engine
 * CONNECT_LIBXML2, Support for LIBXML2 in the CONNECT storage engine
 * CONNECT_ODBC, Support for ODBC in the CONNECT storage engine
 * CONNECT_ZIP, Support for ZIP in the CONNECT storage engine
 * CONNECT_REST, Support for REST API in the CONNECT storage engine
 * CONNECT_XMAP, Support for index file mapping in the CONNECT storage engine
 * CONNECT, Storage Engine MODULE

```
and also cmake outputs wrong message:
```

- The following features have been disabled:

 * CONNECT_JDBC, Support for JDBC in the CONNECT storage engine
 * CONNECT_MONGODB, Support for MongoDB in the CONNECT storage engine

$ cmake . -LAH|grep CONNECT_
CMake Warning (dev) at CMakeLists.txt:30 (PROJECT):
  Policy CMP0048 is not set: project() command manages VERSION variables.
  Run "cmake --help-policy CMP0048" for policy details.  Use the cmake_policy
  command to set the policy and suppress this warning.

  The following variable(s) would be set to empty:

    CMAKE_PROJECT_VERSION
    CMAKE_PROJECT_VERSION_MAJOR
    CMAKE_PROJECT_VERSION_MINOR
    CMAKE_PROJECT_VERSION_PATCH
This warning is for project developers.  Use -Wno-dev to suppress it.

== Configuring MariaDB Connector/C
CONNECT_WITH_BSON:BOOL=ON
CONNECT_WITH_JDBC:BOOL=ON  < wrong>
CONNECT_WITH_LIBXML2:BOOL=ON
CONNECT_WITH_MONGO:BOOL=ON <wrong>
CONNECT_WITH_ODBC:BOOL=ON
CONNECT_WITH_REST:BOOL=ON
CONNECT_WITH_VCT:BOOL=ON
CONNECT_WITH_XMAP:BOOL=ON
CONNECT_WITH_ZIP:BOOL=ON
```

Comes from 751ebe44fda4
```
commit 751ebe44fda4deb715fc2235548517c287f2a559
Author: Heinz Wiesinger <heinz@m2mobi.com>
Date:   Wed Aug 9 21:39:18 2017 +0200

    Add feature summary at the end of cmake.
    
    This gives a short overview over found/missing dependencies as well
    as enabled/disabled features.
    
    Initial author Heinz Wiesinger <heinz@m2mobi.com>
    Additions by Vicențiu Ciorbaru <vicentiu@mariadb.org>
    * Report all plugins enabled via MYSQL_ADD_PLUGIN
    * Simplify code. Eliminate duplication by making use of WITH_xxx
      variable values to set feature "ON" / "OFF" state.
    
    Reviewed by: wlad@mariadb.com (code details) serg@mariadb.com (the idea)

```

## With patch
- No java installed, error reported
```
CMake Error at /usr/share/cmake-3.16/Modules/FindPackageHandleStandardArgs.cmake:146 (message):
  Could NOT find Java (missing: Java_JAVA_EXECUTABLE Java_JAR_EXECUTABLE
  Java_JAVAC_EXECUTABLE Java_JAVAH_EXECUTABLE Java_JAVADOC_EXECUTABLE)
  (Required is at least version "1.6")
Call Stack (most recent call first):
  /usr/share/cmake-3.16/Modules/FindPackageHandleStandardArgs.cmake:393 (_FPHSA_FAILURE_MESSAGE)
  /usr/share/cmake-3.16/Modules/FindJava.cmake:332 (find_package_handle_standard_args)
  storage/connect/CMakeLists.txt:282 (FIND_PACKAGE)
```
- Use cached variables `CONNECT_WITH_JDBC`

I cannot see usage of FindJava and FindJNI files:
- Without:
```
-- Could NOT find LibXml2 (missing: LIBXML2_LIBRARY LIBXML2_INCLUDE_DIR) 
CMake Error at /usr/share/cmake-3.16/Modules/FindPackageHandleStandardArgs.cmake:146 (message):
  Could NOT find Java (missing: Java_JAVA_EXECUTABLE Java_JAR_EXECUTABLE
  Java_JAVAC_EXECUTABLE Java_JAVAH_EXECUTABLE Java_JAVADOC_EXECUTABLE)
  (Required is at least version "1.6")
Call Stack (most recent call first):
  /usr/share/cmake-3.16/Modules/FindPackageHandleStandardArgs.cmake:393 (_FPHSA_FAILURE_MESSAGE)
  /usr/share/cmake-3.16/Modules/FindJava.cmake:332 (find_package_handle_standard_args)
  storage/connect/CMakeLists.txt:281 (FIND_PACKAGE)
```

- With them:
```
CMake Error at /usr/share/cmake-3.16/Modules/FindPackageHandleStandardArgs.cmake:146 (message):
  Could NOT find JNI (missing: JAVA_AWT_LIBRARY JAVA_JVM_LIBRARY
  JAVA_INCLUDE_PATH JAVA_INCLUDE_PATH2 JAVA_AWT_INCLUDE_PATH)
Call Stack (most recent call first):
  /usr/share/cmake-3.16/Modules/FindPackageHandleStandardArgs.cmake:393 (_FPHSA_FAILURE_MESSAGE)
  /usr/share/cmake-3.16/Modules/FindJNI.cmake:372 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
  cmake/FindJNI.cmake:12 (include)
  storage/connect/CMakeLists.txt:283 (FIND_PACKAGE)
```

- Install `openjdk-11-jdk-headless ` [405MB], Java found, but not JNI
```
-- Found Java: /usr/bin/java (found suitable version "11.0.18", minimum required is "1.6") 
CMake Error at /usr/share/cmake-3.16/Modules/FindPackageHandleStandardArgs.cmake:146 (message):
  Could NOT find JNI (missing: JAVA_AWT_LIBRARY JAVA_AWT_INCLUDE_PATH)
Call Stack (most recent call first):
  /usr/share/cmake-3.16/Modules/FindPackageHandleStandardArgs.cmake:393 (_FPHSA_FAILURE_MESSAGE)
  /usr/share/cmake-3.16/Modules/FindJNI.cmake:372 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
  storage/connect/CMakeLists.txt:283 (FIND_PACKAGE)
```



Additionally this changed
```
-- The following REQUIRED packages have been found:

 * Curses
 * Java (required version >= 1.6)
 * JNI
```

`jni.h` (/usr/lib/jvm/java-11-openjdk-amd64/include/jni.h) used in `javaconn.h` 
```
$ openjdk-11-jdk-headless:amd64: /usr/lib/jvm/java-11-openjdk-amd64/include/jni.h
```
Tried to remove it, but cannot build the binary, need to have JNI\



# Bug 2 - JavaWrappers.jar

Note: Only test that is ussing the wrapper is disabled
```
0a96c9c4aab6 (Olivier Bertrand 2016-06-13 14:28:02 +0200 15) jdbc_postgresql : Variable settings depend on machine configuration
```
Actually, everything that is using `-- source jdbconn.inc` that includes the file is disabled in mtr

```
$ git blame debian/not-installed|grep Java
b5edb4ca3a39 (Otto Kekäläinen 2018-01-12 16:56:55 +0000   8) usr/lib/mysql/plugin/JavaWrappers.jar # These are only built if JNI/libjawt.so is installed from e.g. openjdk-8-jre-headless
```

- TESTED
```
-- jar file: /home/anel/GitHub/mariadb/server/build/connect-java/storage/connect/jarFiles/JdbcInterface.jar,
-- CLASS DIR: /home/anel/GitHub/mariadb/server/build/connect-java/storage/connect/CMakeFiles/JdbcInterface.dir

```

- Problems:
1. javaconn.cpp is appending JavaWrappers.jar that is precompiled from /share directory


Patch:
- Created .jar file
```
$ find .|grep JdbcInterface
./storage/connect/connect_jars/JdbcInterface.jar
```
Note that it is not created with `make connect` (empty `jarFiles` directory),
but when is run `make` it works (because it is not part of `connect` target.
Not sure how is created (`ha_connect.so` - `connect` target, it should be part of `cmake/plugin.cmake`))

- Debian:
Since `debian/mariadb-test-data.install` is using `usr/share/mysql/mysql-test/std_data` that is no more visible,
it will not be anymore there, however we need to create new package for Jdbcinterface


- Test
  - Have changed docker compose volume directly from generated jar file, when testing JDBC
  ```
     - /home/anel/GitHub/mariadb/server/build/connect-java/storage/connect/jarFiles/:/jdbc/
  ```
  - Have change target.cnf that is mounted in `/etc/mysql/conf.d`
  ```
  # connect_class_path=/usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JavaWrappers.jar:/usr/share/java/mariadb-java-client-2.7.4.jar
  connect_class_path=/jdbc/JdbcInterface.jar:/usr/share/java/mariadb-java-client-2.7.4.jar
  ```

- Got an error when using .sql with JDBC connection url on localhost script during startup:
```
mariadb-target  | ERROR 1105 (HY000) at line 6: Connecting: java.sql.SQLNonTransientConnectionException: Could not connect to address=(host=localhost)(port=3306)(type=master) : Socket fail to connect to host:localhost, port:3306. Connection refused (Connection refused) rc=-2
```