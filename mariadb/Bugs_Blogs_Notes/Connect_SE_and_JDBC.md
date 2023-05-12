# Connect and JDBC
[Documentation link](https://mariadb.com/kb/en/connect-jdbc-table-type-accessing-tables-from-another-dbms/)

We need:
1. `Java SDK` installed
2. java wrapper class files
3. JDBC driver

  - With connect we don't get java wrapper class files (`JavaWrappers.jar`) on a system (2)
  - Based on KB default wrapper is `JdbcInterface` to access JDBC driver
  - Binary distro have that wrapper as `JdbcInterface.jar` installed in `plugin` dir,
    whose path is included in the class file of the `JVM` < TODO: NOT TRUE FOR `list.launchpad`
    Later jar file (`JdbcInterface.jar `) has been installed in the mysql share directory whose path is always automatically included in the class path available to the JVM. Is it `plugin` or `share`?
  - `JavaWrappers.jar` adds all `JdbcInterface`, `AppacheInterface` , `MariaDBInterface`togetther
  - Controlled by [connect_java_wrapper](https://mariadb.com/kb/en/connect-system-variables/#connect_java_wrapper)
    session variable.


- By default there is no connect SE, using MariaDB 10.6 docker container
```bash
$ ls /usr/lib/mysql/plugin/
auth_ed25519.so    auth_pam_v1.so          ha_archive.so    ha_federatedx.so  locales.so             query_response_time.so    sql_errlog.so
auth_pam.so        disks.so                ha_blackhole.so  ha_sphinx.so      metadata_lock_info.so  server_audit.so           type_mysql_json.so
auth_pam_tool_dir  file_key_management.so  ha_federated.so  handlersocket.so  query_cache_info.so    simple_password_check.so  wsrep_info.so
```

### Install mariadb-plugin-connect (mariadb.org)
```bash
$ apt install
$ curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash -s -- --mariadb-server-version="mariadb-10.6"
```
### Install mariadb-plugin-connect (list.launchpad)

- Install `mariadb-plugin-connect`
```bash
$ ls /usr/lib/mysql/plugin/|grep connect
ha_connect.so

$ dpkg -l mariadb-plugin-connect
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name                   Version                 Architecture Description
+++-======================-=======================-============-==================================
ii  mariadb-plugin-connect 1:10.6.12+maria~ubu2004 amd64        Connect storage engine for MariaDB

$ dpkg -s mariadb-plugin-connect
Maintainer: MariaDB Developers <maria-developers@lists.launchpad.net>

$ dpkg -L mariadb-plugin-connect
/.
/etc
/etc/mysql
/etc/mysql/mariadb.conf.d
/etc/mysql/mariadb.conf.d/connect.cnf
/usr
/usr/lib
/usr/lib/mysql
/usr/lib/mysql/plugin
/usr/lib/mysql/plugin/ha_connect.so
/usr/share
/usr/share/doc
/usr/share/doc/mariadb-plugin-connect
/usr/share/doc/mariadb-plugin-connect/changelog.gz
/usr/share/doc/mariadb-plugin-connect/copyright
```

- Install `mariadb-test-data` package
```bash
$ dpkg -L mariadb-test-data|grep -e Java -e Jdbc
/usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JavaWrappers.jar
/usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JdbcMariaDB.jar

```

## Java things
### JDK
For the purpose of building and running a Java application using CMake,
you only need to install the JDK (Java Development Kit).
The JDK includes the JRE (Java Runtime Environment), so you do not need to install both separately.
The JDK includes the necessary tools to compile and run Java code, as well as to generate and manage Java libraries and JAR files. 

### JRE
The JRE, on the other hand, only includes the tools to run Java applications, but not to develop them.
In summary, you only need to install the JDK to build and run a Java application using the CMake example we've discussed earlier.

### jar command
`jar` command is part of JDK (Java development Kit), required to compile and run Java programs
and  not in `JRE` (Java Runtime Environment)

## Install JDK

```bash
$ sudo apt-get install default-jdk
```
From `mariadb-test-data` we can get needed wrappers
```bash
$ jar tf usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JdbcMariaDB.jar |grep wrappers
wrappers/
wrappers/ApacheInterface.class
wrappers/Client.class
wrappers/HikariCPInterface.Copie
wrappers/JdbcInterface.class
wrappers/MariadbInterface.class
wrappers/MysqlInterface.class
wrappers/OracleInterface.class
wrappers/PostgresqlInterface.class

```
JVM (Java Virtual Machine) is loading JAR files
```bash
$ java -cp /path/to/myjar.jar com.example.MyProgram
export CLASSPATH=/path/to/myjar.jar:$CLASSPATH
```

## Get jvm.so
```bash
$ ./usr/lib/jvm/java-11-openjdk-amd64/lib/server/libjvm.so

```
Test
```sql
MariaDB [(none)]> select @@connect_jvm_path;
+--------------------+
| @@connect_jvm_path |
+--------------------+
| NULL               |
+--------------------+
1 row in set (0.000 sec)

MariaDB [(none)]> select @@connect_java_wrapper;
+------------------------+
| @@connect_java_wrapper |
+------------------------+
| wrappers/JdbcInterface |
+------------------------+
1 row in set (0.000 sec)


MariaDB [(none)]> set global connect_jvm_path='/usr/lib/jvm/java-11-openjdk-amd64/lib/server/';
Query OK, 0 rows affected (0.000 sec)

MariaDB [(none)]> select @@connect_jvm_path;
+------------------------------------------------+
| @@connect_jvm_path                             |
+------------------------------------------------+
| /usr/lib/jvm/java-11-openjdk-amd64/lib/server/ |
+------------------------------------------------+
1 row in set (0.000 sec)


```


# Use classpath
```bash
$ export CLASSPATH=/usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JavaWrappers.jar
```
Test
```sql
MariaDB [(none)]> create function envar returns string soname 'ha_connect.so';
Query OK, 0 rows affected (0.015 sec)

MariaDB [(none)]> select envar('CLASSPATH');
+--------------------+
| envar('CLASSPATH') |
+--------------------+
| NULL               |
+--------------------+
1 row in set (0.000 sec)

```
# Move .jar file to plugin
```bash
$ cp /usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JavaWrappers.jar /usr/lib/mysql/plugin/
```
```sql
Empty
```
# Set directly
```sql
MariaDB [(none)]> set global connect_class_path='/usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JavaWrappers.jar';
Query OK, 0 rows affected (0.000 sec)

MariaDB [(none)]> select @@connect_class_path;
+------------------------------------------------------------------------------+
| @@connect_class_path                                                         |
+------------------------------------------------------------------------------+
| /usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JavaWrappers.jar |
+------------------------------------------------------------------------------+
1 row in set (0.000 sec)
```
restart the container




## Test connection
```sql

MariaDB [test]> create table jboys engine=connect table_type=JDBC tabname=boys connection='jdbc:mysql://localhost/dbname?user=root';
ERROR 1105 (HY000): Connecting: java.sql.SQLException: No suitable driver found for jdbc:mysql://localhost/dbname?user=root rc=-2
```

### Install JDBC driver
```bash
$ curl -LO https://ftp.bme.hu/pub/mirrors/mariadb/connector-java-3.1.3/mariadb-java-client-3.1.3-sources.jar
# $ mv mariadb-java-client-3.1.3-sources.jar /usr/share/mysql/
$ mv mariadb-java-client-3.1.3-sources.jar /usr/lib/jvm/default-java/lib/
```
- Test
```sql

>> create table boys (
name char(12),
city char(12),
birth date,
hired date);


# Does not work
>> set global connect_jvm_path='/usr/lib/jvm/java-11-openjdk-amd64/lib/server/:/usr/lib/jvm/default-java/lib/';
 
# Move to jvm_path - doesn't work
$ cd /usr/lib/jvm/default-java/lib/
$ mv mariadb-java-client-3.1.3-sources.jar ../../java-11-openjdk-amd64/lib/server/
$ cd /usr/lib/jvm/java-11-openjdk-amd64/lib/server


# Restart container
set global connect_jvm_path='/usr/lib/jvm/java-11-openjdk-amd64/lib/server/';
set global connect_class_path='/usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JavaWrappers.jar';
```

- Don't use source version driver from mariadb.org instead from mariadb.com
```bash
# Have sent it to  /usr/lib/jvm/java-11-openjdk-amd64/lib/server/
Doesn't work
# Have use it in class path as it should

set global connect_jvm_path='/usr/lib/jvm/java-11-openjdk-amd64/lib/server/';
> set global connect_class_path='/usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JavaWrappers.jar:/usr/lib/jvm/java-11-openjdk-amd64/lib/server/mariadb-java-client-3.1.3.jar';
```

- After restart:
```
MariaDB [test]> create table jboys engine=connect table_type=JDBC tabname=boys connection='jdbc:mysql://localhost/dbname?user=root';
ERROR 1105 (HY000): Error loading shared library libjvm.so: libjvm.so: cannot open shared object file: No such file or directory
MariaDB [test]> 

MariaDB [test]> set global connect_jvm_path='/usr/lib/jvm/java-11-openjdk-amd64/lib/server/';
Query OK, 0 rows affected (0.000 sec)

MariaDB [test]> create table jboys engine=connect table_type=JDBC tabname=boys connection='jdbc:mysql://localhost/dbname?user=root';
ERROR 1105 (HY000): ERROR: class wrappers/JdbcInterface not found!

set global connect_class_path='/usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JavaWrappers.jar:/usr/lib/jvm/java-11-openjdk-amd64/lib/server/mariadb-java-client-3.1.3.jar';
MariaDB [test]> create table jboys engine=connect table_type=JDBC tabname=boys connection='jdbc:mysql://localhost/dbname?user=root';
ERROR 1105 (HY000): ERROR: class wrappers/JdbcInterface not found!

set global connect_class_path='/usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JavaWrappers.jar'

```


## Downloaded mysql connector
```
$ mkdir connectors
$ curl -LO https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j_8.0.32-1ubuntu20.04_all.deb

$ ls
mariadb-java-client-3.1.3.jar  mysql-connector-j_8.0.32-1ubuntu20.04_all.deb
```

Config
```
# Ne radi
plugin_load_add=ha_connect.so
plugin_dir=/usr/lib/mysql/plugin/
connect_class_path='/usr/share/mysql/mysql-test/plugin/connect/connect/std_data/:/connectors/mariadb-java-client-3.1.3.jar'
connect_jvm_path='/usr/lib/jvm/java-11-openjdk-amd64/lib/server/'

$ cp /usr/share/mysql/mysql-test/plugin/connect/connect/std_data/JavaWrappers.jar connectors/

# New configuration
plugin_load_add=ha_connect.so
plugin_dir=/usr/lib/mysql/plugin/
connect_class_path='/connectors/JavaWrappers.jar:/connectors/mariadb-java-client-3.1.3.jar'
connect_jvm_path='/usr/lib/jvm/java-11-openjdk-amd64/lib/server/'


# Got something new, see the difference between mariadb and mysql connectors:
MariaDB [test]> create table jboys engine=connect table_type=JDBC tabname=boys connection='jdbc:mariadb://localhost/dbname?user=root';
ERROR 1105 (HY000): Connecting: java.sql.SQLInvalidAuthorizationSpecException: (conn=6) Access denied for user 'root'@'127.0.0.1' (using password: NO) rc=-2
MariaDB [test]> create table jboys engine=connect table_type=JDBC tabname=boys connection='jdbc:mysql://localhost/dbname?user=root';
ERROR 1105 (HY000): Connecting: java.sql.SQLException: No suitable driver found for jdbc:mysql://localhost/dbname?user=root rc=-2



# And this works
MariaDB [test]> create table jboys engine=connect table_type=JDBC tabname=boys connection='jdbc:mariadb://localhost/test?user=root&password=123';
Query OK, 0 rows affected (0.050 sec)

MariaDB [test]> show tables;
+----------------+
| Tables_in_test |
+----------------+
| boys           |
| jboys          |
+----------------+
2 rows in set (0.000 sec)


MariaDB [test]> show create table jboys\G
*************************** 1. row ***************************
       Table: jboys
Create Table: CREATE TABLE `jboys` (
  `name` char(12) DEFAULT NULL,
  `city` char(12) DEFAULT NULL,
  `birth` date DEFAULT NULL,
  `hired` date DEFAULT NULL
) ENGINE=CONNECT DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci CONNECTION='jdbc:mariadb://localhost/test?user=root&password=123' `TABLE_TYPE`='JDBC' `TABNAME`='boys'
1 row in set (0.000 sec)

```










# Literautre
[1] [KB documentation JDBC and Connect](https://mariadb.com/kb/en/connect-jdbc-table-type-accessing-tables-from-another-dbms/)
