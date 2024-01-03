# MDEV-26231: mysql_upgrade attempts to remove plugins which it failed to install

https://jira.mariadb.org/browse/MDEV-26231

# Create MySQL 5.7 datadir
- Start the container in MySQL
```bash
$ docker run -it --name mysql-cont --rm -v"${PWD}/mysql-data-dir":/var/lib/mysql -p=3344:3306 -e MYSQL_ROOT_PASSWORD=secret -d mysql
```

- Create the table with `JSON` data with `MyISAM` storage engine:
```sql
mysql> create database test; use test; create table t(t JSON) engine=MyISAM; show create table t; insert into t values ('["a1","a2","a3"]'); insert into t values ('{"k1":"v1", "k2":"v2"}'); select * from t;

+--------------------------+
| t                        |
+--------------------------+
| ["a1", "a2", "a3"]       |
| {"k1": "v1", "k2": "v2"} |
+--------------------------+
2 rows in set (0.00 sec)

mysql> select @@version
    -> ;
+-----------+
| @@version |
+-----------+
| 8.0.33    |
+-----------+
1 row in set (0.00 sec)

```

- Stop the MySQL container and get the data from datadir (in 8.0.33) missing `frm` format, there is `sdi`
```bash
$ sudo ls mysql-data-dir/test/
t_366.sdi  t.MYD  t.MYI
```

- Do the same for 5.7 data dir (again as in 8.0 running from terminal doesn't work - need escape chars)
```
$ docker run -it --name mysql-cont-5.7 --rm -v"${PWD}/mysql-data-dir":/var/lib/mysql -eMYSQL_ALLOW_EMPTY_PASSWORD=yes -d mysql:5.7
$ docker exec -it mysql-cont-5.7 mysql -uroot -e"create database test; use test; create table t(t JSON) engine=MyISAM; show create table t; insert into t values ('["a1","a2","a3"]'); insert into t values ('{"k1":"v1", "k2":"v2"}'); select * from t;"
+-------+-----------------------------------------------------------------------------------+
| Table | Create Table                                                                      |
+-------+-----------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `t` json DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 |
+-------+-----------------------------------------------------------------------------------+
ERROR 3140 (22032) at line 1: Invalid JSON text: "Invalid value." at position 1 in value for column 't.t'.
```
- Run in termnial, works
```sql
mysql> select @@version;
+-----------+
| @@version |
+-----------+
| 5.7.44    |
+-----------+
1 row in set (0.00 sec)
```
- Get the data
```bash
$ sudo ls mysql-data-dir/test/
db.opt	t.frm  t.MYD  t.MYI
```
- Change ownership of folder
```bash
$ sudo ls -la mysql-data-dir/test/|less
drwxr-xr-x 6 systemd-coredump root             4096 Nov 13 12:14 ..
-rw-r----- 1 systemd-coredump systemd-coredump   65 Nov 13 12:12 db.opt
-rw-r----- 1 systemd-coredump systemd-coredump 8554 Nov 13 12:12 t.frm
-rw-r----- 1 systemd-coredump systemd-coredump   72 Nov 13 12:13 t.MYD
-rw-r----- 1 systemd-coredump systemd-coredump 1024 Nov 13 12:14 t.MYI

$ sudo chown -R $USER:$USER mysql-data-dir/
drwxr-x--- 2 anel anel 4096 Nov 13 12:12 .
drwxr-xr-x 6 anel anel 4096 Nov 13 12:14 ..
-rw-r----- 1 anel anel   65 Nov 13 12:12 db.opt
-rw-r----- 1 anel anel 8554 Nov 13 12:12 t.frm
-rw-r----- 1 anel anel   72 Nov 13 12:13 t.MYD
-rw-r----- 1 anel anel 1024 Nov 13 12:14 t.MYI
```

# Example when using whole MySQL 5.7 datadirecvotry
```sql
MariaDB [(none)]> select @@datadir;
+-----------------+
| @@datadir       |
+-----------------+
| /var/lib/mysql/ |
+-----------------+
1 row in set (0.000 sec)
```
- Stop service and change in configuration
```bash
$ sudo systemctl stop mariadb

$ sudo systemctl status mariadb
● mariadb.service - MariaDB 10.6.16 database server
     Loaded: loaded (/lib/systemd/system/mariadb.service; enabled; vendor preset: enabled)
    Drop-In: /etc/systemd/system/mariadb.service.d
             └─migrated-from-my.cnf-settings.conf
     Active: inactive (dead) since Mon 2023-11-13 12:31:49 CET; 35s ago
       Docs: man:mariadbd(8)
             https://mariadb.com/kb/en/library/systemd/
    Process: 22049 ExecStart=/usr/sbin/mariadbd $MYSQLD_OPTS $_WSREP_NEW_CLUSTER $_WSREP_START_POSITION (code=exited, status=0/SUCCESS)
   Main PID: 22049 (code=exited, status=0/SUCCESS)
     Status: "MariaDB server is down"

Nov 13 12:31:49 anel systemd[1]: Stopping MariaDB 10.6.16 database server...
Nov 13 12:31:49 anel mariadbd[22049]: 2023-11-13 12:31:49 0 [Note] InnoDB: FTS optimize thread exiting.
Nov 13 12:31:49 anel mariadbd[22049]: 2023-11-13 12:31:49 0 [Note] InnoDB: Starting shutdown...
Nov 13 12:31:49 anel mariadbd[22049]: 2023-11-13 12:31:49 0 [Note] InnoDB: Dumping buffer pool(s) to /var/lib/mysql/ib_buffer_pool
Nov 13 12:31:49 anel mariadbd[22049]: 2023-11-13 12:31:49 0 [Note] InnoDB: Buffer pool(s) dump completed at 231113 12:31:49
Nov 13 12:31:49 anel mariadbd[22049]: 2023-11-13 12:31:49 0 [Note] InnoDB: Removed temporary tablespace data file: "./ibtmp1"
Nov 13 12:31:49 anel mariadbd[22049]: 2023-11-13 12:31:49 0 [Note] InnoDB: Shutdown completed; log sequence number 197596042; transaction id 1371254
Nov 13 12:31:49 anel mariadbd[22049]: 2023-11-13 12:31:49 0 [Note] /usr/sbin/mariadbd: Shutdown complete
Nov 13 12:31:49 anel systemd[1]: mariadb.service: Succeeded.
```

- Change in `$ sudo vim /etc/mysql/mariadb.conf.d/50-server.cnf` to `/home/anel/GitHub/mariadb/mysql-data-dir`
- When using it and starting the `sudo systemctl start maridb` it doesn't work
```bash
-- A start job for unit mariadb.service has begun execution.
-- 
-- The job identifier is 11494.
Nov 13 12:35:06 anel mariadbd[126447]: 2023-11-13 12:35:06 0 [Warning] Can't create test file '/home/anel/GitHub/mariadb/mysql-data-dir/anel.lower-test' (Errcode: 13 "Permission denied")
Nov 13 12:35:06 anel mariadbd[126447]: [118B blob data]
Nov 13 12:35:06 anel mariadbd[126447]: 2023-11-13 12:35:06 0 [ERROR] Aborting
Nov 13 12:35:06 anel systemd[1]: mariadb.service: Main process exited, code=exited, status=1/FAILURE
-- Subject: Unit process exited
-- Defined-By: systemd
-- Support: http://www.ubuntu.com/support
-- 
-- An ExecStart= process belonging to unit mariadb.service has exited.
-- 
-- The process' exit code is 'exited' and its exit status is 1.
Nov 13 12:35:06 anel systemd[1]: mariadb.service: Failed with result 'exit-code'.
-- Subject: Unit failed
-- Defined-By: systemd
-- Support: http://www.ubuntu.com/support
-- 
-- The unit mariadb.service has entered the 'failed' state with result 'exit-code'.
Nov 13 12:35:06 anel systemd[1]: Failed to start MariaDB 10.6.16 database server.
-- Subject: A start job for unit mariadb.service has failed
-- Defined-By: systemd
-- Support: http://www.ubuntu.com/support
-- 
-- A start job for unit mariadb.service has finished with a failure.
-- 
-- The job identifier is 11494 and the job result is failed.
Nov 13 12:35:06 anel sudo[126406]: pam_unix(sudo:session): session closed for user root
Nov 13 12:35:14 anel sudo[126449]:     anel : TTY=pts/0 ; PWD=/home/anel/GitHub/mariadb ; USER=root ; COMMAND=/usr/bin/journalctl -x3
Nov 13 12:35:14 anel sudo[126449]: pam_unix(sudo:session): session opened for user root by (uid=0)
Nov 13 12:35:14 anel sudo[126449]: pam_unix(sudo:session): session closed for user root
Nov 13 12:35:17 anel sudo[126451]:     anel : TTY=pts/0 ; PWD=/home/anel/GitHub/mariadb ; USER=root ; COMMAND=/usr/bin/journalctl -xe
Nov 13 12:35:17 anel sudo[126451]: pam_unix(sudo:session): session opened for user root by (uid=0)

```
- Nor works `mysql_upgrade`
```
$ sudo mysql_upgrade
Reading datadir from the MariaDB server failed. Got the following error when executing the 'mysql' command line client
ERROR 2002 (HY000): Can't connect to local server through socket '/run/mysqld/mysqld.sock' (2)
FATAL ERROR: Upgrade failed
```

-Again change `mysql-data-dir` to `mysql` user and try again
```bash
$ sudo chown -R mysql:mysql mysql-data-dir
```


# Example works when using MySQL 5.7 database and insert into MariaDB data directory
- Copy that folder in `/var/lib/mysql` where is MariaDB server as `mysql_data_json` database
```bash
$ sudo cp -R mysql-data-dir/test/ /var/lib/mysql/mysql_data_json
anel@anel:~/GitHub/mariadb$ ls /var/lib/mysql/
aria_log.00000001        ddl_recovery-backup.log  debian-10.6.flag         ibdata1                  ibtmp1                   multi-master.info        mysql/                   mysql_upgrade_info       sys/                     
aria_log_control         ddl_recovery.log         ib_buffer_pool           ib_logfile0              modbusdb/                myEnrollmentDB/          mysql_data_json/         performance_schema/      test/    
```

- Start the server and see database:
```sql
MariaDB [(none)]> show databases like "%json";
+------------------+
| Database (%json) |
+------------------+
| mysql_data_json  |
+------------------+
1 row in set (0.000 sec)
```

- Run `mysql_upgrade` with `force`
```bash
$ sudo mysql_upgrade
This installation of MariaDB is already upgraded to 10.6.12-MariaDB.
There is no need to run mysql_upgrade again for 10.6.16-MariaDB.
You can use --force if you still want to run mysql_upgrade

$ sudo mysql_upgrade -f
Phase 4/8: Fixing views
mysql.user                                         OK
mariadb-check: Error: Couldn't get table list for database mysql_data_json: Can't read dir of './mysql_data_json/' (errno: 13 "Permission denied")

Phase 5/8: Fixing table and database names
mariadb-check: Error: Couldn't get table list for database mysql_data_json: Can't read dir of './mysql_data_json/' (errno: 13 "Permission denied")

Phase 6/8: Checking and upgrading tables
mysql_data_json
mariadb-check: Error: Couldn't get table list for database mysql_data_json: Can't read dir of './mysql_data_json/' (errno: 13 "Permission denied")

mysql_data_json
mariadb-check: Error: Couldn't get table list for database mysql_data_json: Can't read dir of './mysql_data_json/' (errno: 13 "Permission denied")
performance_schema

```
- We need to change ownership to `mysql` user since `mysql_upgrade --force` will fail
```
$ sudo ls -la /var/lib/mysql/mysql_data_json/
total 32
drwxr-x--- 2 root  root  4096 Nov 13 12:18 .
drwxr-xr-x 9 mysql mysql 4096 Nov 13 12:22 ..
-rw-r----- 1 root  root    65 Nov 13 12:18 db.opt
-rw-r----- 1 root  root  8554 Nov 13 12:18 t.frm
-rw-r----- 1 root  root    72 Nov 13 12:18 t.MYD
-rw-r----- 1 root  root  1024 Nov 13 12:18 t.MYI

$ sudo ls -la /var/lib/mysql/test/
total 1084
drwx------ 2 mysql mysql  4096 Sep 22 12:07 .
drwxr-xr-x 9 mysql mysql  4096 Nov 13 12:22 ..
-rw-rw---- 1 mysql mysql    67 Feb 21  2023 db.opt

$ sudo chown -R mysql:mysql /var/lib/mysql/mysql_data_json/
$ sudo ls -la /var/lib/mysql/mysql_data_json/
total 32
drwxr-x--- 2 mysql mysql 4096 Nov 13 12:18 .
drwxr-xr-x 9 mysql mysql 4096 Nov 13 12:22 ..
-rw-r----- 1 mysql mysql   65 Nov 13 12:18 db.opt
-rw-r----- 1 mysql mysql 8554 Nov 13 12:18 t.frm
-rw-r----- 1 mysql mysql   72 Nov 13 12:18 t.MYD
-rw-r----- 1 mysql mysql 1024 Nov 13 12:18 t.MYI
```

- Run again `mysql_upgrade --force`
```bash
$ sudo mysql_upgrade -f
Phase 1/8: Checking and upgrading mysql database
Processing databases
mysql
mysql.column_stats                                 OK
mysql.columns_priv                                 OK
mysql.db                                           OK
mysql.event                                        OK
mysql.func                                         OK
mysql.global_priv                                  OK
mysql.gtid_slave_pos                               OK
mysql.help_category                                OK
mysql.help_keyword                                 OK
mysql.help_relation                                OK
mysql.help_topic                                   OK
mysql.index_stats                                  OK
mysql.innodb_index_stats                           OK
mysql.innodb_table_stats                           OK
mysql.plugin                                       OK
mysql.proc                                         OK
mysql.procs_priv                                   OK
mysql.proxies_priv                                 OK
mysql.roles_mapping                                OK
mysql.servers                                      OK
mysql.table_stats                                  OK
mysql.tables_priv                                  OK
mysql.time_zone                                    OK
mysql.time_zone_leap_second                        OK
mysql.time_zone_name                               OK
mysql.time_zone_transition                         OK
mysql.time_zone_transition_type                    OK
mysql.transaction_registry                         OK
Phase 2/8: Installing used storage engines... Skipped
installing plugin for MYSQL_JSON data type
Phase 3/8: Running 'mysql_fix_privilege_tables'
Phase 4/8: Fixing views
mysql.user                                         OK
sys.host_summary                                   OK
sys.host_summary_by_file_io                        OK
sys.host_summary_by_file_io_type                   OK
sys.host_summary_by_stages                         OK
sys.host_summary_by_statement_latency              OK
sys.host_summary_by_statement_type                 OK
sys.innodb_buffer_stats_by_schema                  OK
sys.innodb_buffer_stats_by_table                   OK
sys.innodb_lock_waits                              OK
sys.io_by_thread_by_latency                        OK
sys.io_global_by_file_by_bytes                     OK
sys.io_global_by_file_by_latency                   OK
sys.io_global_by_wait_by_bytes                     OK
sys.io_global_by_wait_by_latency                   OK
sys.latest_file_io                                 OK
sys.memory_by_host_by_current_bytes                OK
sys.memory_by_thread_by_current_bytes              OK
sys.memory_by_user_by_current_bytes                OK
sys.memory_global_by_current_bytes                 OK
sys.memory_global_total                            OK
sys.metrics                                        OK
sys.processlist                                    OK
sys.ps_check_lost_instrumentation                  OK
sys.schema_auto_increment_columns                  OK
sys.schema_index_statistics                        OK
sys.schema_object_overview                         OK
sys.schema_redundant_indexes                       OK
sys.schema_table_lock_waits                        OK
sys.schema_table_statistics                        OK
sys.schema_table_statistics_with_buffer            OK
sys.schema_tables_with_full_table_scans            OK
sys.schema_unused_indexes                          OK
sys.session                                        OK
sys.session_ssl_status                             OK
sys.statement_analysis                             OK
sys.statements_with_errors_or_warnings             OK
sys.statements_with_full_table_scans               OK
sys.statements_with_runtimes_in_95th_percentile    OK
sys.statements_with_sorting                        OK
sys.statements_with_temp_tables                    OK
sys.user_summary                                   OK
sys.user_summary_by_file_io                        OK
sys.user_summary_by_file_io_type                   OK
sys.user_summary_by_stages                         OK
sys.user_summary_by_statement_latency              OK
sys.user_summary_by_statement_type                 OK
sys.version                                        OK
sys.wait_classes_global_by_avg_latency             OK
sys.wait_classes_global_by_latency                 OK
sys.waits_by_host_by_latency                       OK
sys.waits_by_user_by_latency                       OK
sys.waits_global_by_latency                        OK
sys.x$host_summary                                 OK
sys.x$host_summary_by_file_io                      OK
sys.x$host_summary_by_file_io_type                 OK
sys.x$host_summary_by_stages                       OK
sys.x$host_summary_by_statement_latency            OK
sys.x$host_summary_by_statement_type               OK
sys.x$innodb_buffer_stats_by_schema                OK
sys.x$innodb_buffer_stats_by_table                 OK
sys.x$innodb_lock_waits                            OK
sys.x$io_by_thread_by_latency                      OK
sys.x$io_global_by_file_by_bytes                   OK
sys.x$io_global_by_file_by_latency                 OK
sys.x$io_global_by_wait_by_bytes                   OK
sys.x$io_global_by_wait_by_latency                 OK
sys.x$latest_file_io                               OK
sys.x$memory_by_host_by_current_bytes              OK
sys.x$memory_by_thread_by_current_bytes            OK
sys.x$memory_by_user_by_current_bytes              OK
sys.x$memory_global_by_current_bytes               OK
sys.x$memory_global_total                          OK
sys.x$processlist                                  OK
sys.x$ps_digest_95th_percentile_by_avg_us          OK
sys.x$ps_digest_avg_latency_distribution           OK
sys.x$ps_schema_table_statistics_io                OK
sys.x$schema_flattened_keys                        OK
sys.x$schema_index_statistics                      OK
sys.x$schema_table_lock_waits                      OK
sys.x$schema_table_statistics                      OK
sys.x$schema_table_statistics_with_buffer          OK
sys.x$schema_tables_with_full_table_scans          OK
sys.x$session                                      OK
sys.x$statement_analysis                           OK
sys.x$statements_with_errors_or_warnings           OK
sys.x$statements_with_full_table_scans             OK
sys.x$statements_with_runtimes_in_95th_percentile  OK
sys.x$statements_with_sorting                      OK
sys.x$statements_with_temp_tables                  OK
sys.x$user_summary                                 OK
sys.x$user_summary_by_file_io                      OK
sys.x$user_summary_by_file_io_type                 OK
sys.x$user_summary_by_stages                       OK
sys.x$user_summary_by_statement_latency            OK
sys.x$user_summary_by_statement_type               OK
sys.x$wait_classes_global_by_avg_latency           OK
sys.x$wait_classes_global_by_latency               OK
sys.x$waits_by_host_by_latency                     OK
sys.x$waits_by_user_by_latency                     OK
sys.x$waits_global_by_latency                      OK
Phase 5/8: Fixing table and database names
Phase 6/8: Checking and upgrading tables
Processing databases
information_schema
modbusdb
modbusdb.auth_group                                OK
modbusdb.auth_group_permissions                    OK
modbusdb.auth_permission                           OK
modbusdb.auth_user                                 OK
modbusdb.auth_user_groups                          OK
modbusdb.auth_user_user_permissions                OK
modbusdb.device_parent                             OK
modbusdb.django_admin_log                          OK
modbusdb.django_content_type                       OK
modbusdb.django_migrations                         OK
modbusdb.django_session                            OK
modbusdb.django_site                               OK
modbusdb.modbus_app_customer                       OK
modbusdb.modbus_app_globalsettings                 OK
modbusdb.modbus_app_logevents                      OK
modbusdb.modbus_app_modbusdata                     OK
modbusdb.modbus_app_resolutioncurrentvalue         OK
modbusdb.modbus_app_tariff                         OK
modbusdb.modbus_app_variable                       OK
modbusdb.modbus_devices_tbl                        OK
myEnrollmentDB
myEnrollmentDB.PupilClassesCoursesGrades           OK
myEnrollmentDB.acknowledgments                     OK
myEnrollmentDB.auth_group                          OK
myEnrollmentDB.auth_group_permissions              OK
myEnrollmentDB.auth_permission                     OK
myEnrollmentDB.cantons                             OK
myEnrollmentDB.courses_secondary                   OK
myEnrollmentDB.django_admin_log                    OK
myEnrollmentDB.django_content_type                 OK
myEnrollmentDB.django_migrations                   OK
myEnrollmentDB.django_session                      OK
myEnrollmentDB.pupils                              OK
myEnrollmentDB.secondarySchools                    OK
myEnrollmentDB.studentClass                        OK
myEnrollmentDB.student_courses                     OK
myEnrollmentDB.student_specialcoursesperdesiredchoice OK
myEnrollmentDB.teachers                            OK
myEnrollmentDB.teachers_groups                     OK
myEnrollmentDB.teachers_user_permissions           OK
mysql_data_json
mysql_data_json.t                                  Needs upgrade
performance_schema
sys
sys.sys_config                                     OK
test
test.guests                                        OK
test.log                                           OK
test.log1                                          OK
test.myjsontbl                                     OK
test.s                                             OK
test.s1                                            OK
test.t                                             OK
test.t1                                            OK
test.t2                                            OK
test.vips                                          OK

Repairing tables
mysql_data_json.t                                  OK
Phase 7/8: uninstalling plugins
uninstalling plugin for 'type_mysql_json' data type
Phase 8/8: Running 'FLUSH PRIVILEGES'
OK

```


# MDEV-32235: mysql_json cannot be used on newly created table

https://jira.mariadb.org/browse/MDEV-32235

- Testing on MariaDB 10.6
```sql
MariaDB [mysql_data_json]> CREATE TABLE testjson (t mysql_json NOT NULL);
ERROR 4161 (HY000): Unknown data type: 'mysql_json'

MariaDB [mysql_data_json]> install soname 'type_mysql_json';
Query OK, 0 rows affected (0.015 sec)

MariaDB [mysql_data_json]> CREATE TABLE testjson (t mysql_json NOT NULL);
Query OK, 0 rows affected (0.031 sec)

MariaDB [mysql_data_json]> show create table testjson;
+----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table    | Create Table                                                                                                                                                             |
+----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| testjson | CREATE TABLE `testjson` (
  `t` json /* MySQL 5.7 */ CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci |
+----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.000 sec)


MariaDB [mysql_data_json]> INSERT INTO testjson VALUES ('{"k1":"v1"}'); # insert is not allowed
Query OK, 1 row affected (0.015 sec)

MariaDB [mysql_data_json]> select * from testjson;
ERROR 1105 (HY000): Error parsing MySQL JSON format, please dump this table from MySQL and then restore it to be able to use it in MariaDB.


```


Razlika - radi
```sql
CREATE TABLE `t2` (
  `j` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`j`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
```
Ne radi
```sql
CREATE TABLE `testjson` (
  `t` json /* MySQL 5.7 */ CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci
```

Reason is because JSON shouldn't have any collation/character set attributes as a field, while longtext should.


# MySQL container bug
```
$ docker run --name mysql-cont --rm -v"${PWD}/mysql-data-dir":/var/lib/mysql -p 3344:3306 -eMYSQL_ROOT_PASSWORD=secret -d mysql
b293ac758ad13750bb48b22857679375eca559f24d1e5dc79e92acb832fba8b9

$ docker exec -it mysql-cont mysql -uroot -psecret
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)
```
- However if not using -psecret but instead only -p and then "password" then works
- Alternative to specify the IPV4 host
```
$ docker run --name mysql-cont --rm -v"${PWD}/mysql-data-dir":/var/lib/mysql -p 127.0.0.1:3344:3306 -eMYSQL_ROOT_PASSWORD=secret -d mysql
$ docker exec -it mysql-cont mysql -uroot -psecret # this will work
```

- Trying to connect with `mariadb`, doens't work for 8.0.33.
```
$ ./client/mariadb -uroot -psecret -h127.0.0.1 -P3344 --protocol=tcp
ERROR 1045 (28000): Plugin caching_sha2_password could not be loaded: /usr/local/mysql/lib/plugin/caching_sha2_password.so: cannot open shared object file: No such file or directory

$ ./client/mysql_upgrade -uroot -psecret -h127.0.0.1 -P3344 --protocol=tcp
Reading datadir from the MariaDB server failed. Got the following error when executing the 'mysql' command line client
ERROR 1045 (28000): Plugin caching_sha2_password could not be loaded: /usr/local/mysql/lib/plugin/caching_sha2_password.so: cannot open shared object file: No such file or directory
FATAL ERROR: Upgrade failed

```

- It works for 5.7
```
$ docker run --name mysql-cont --rm -v"${PWD}/mysql-data-dir":/var/lib/mysql -p 127.0.0.1:3344:3306 -eMYSQL_ROOT_PASSWORD=secret -d mysql:5.7


$ ./client/mariadb -uroot -psecret -h127.0.0.1 -P3344 --protocol=tcp
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.44 MySQL Community Server (GPL)

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]> exit
Bye


$ ./client/mysql_upgrade -uroot -psecret -h127.0.0.1 -P3344 --protocol=tcp
Reading datadir from the MariaDB server failed. Got the following error when executing the 'mysql' command line client
ERROR 1193 (HY000) at line 1: Unknown system variable 'WSREP_ON'
FATAL ERROR: Upgrade failed


# Same happened with
$ ./client/mysql_upgrade -P 3344 -uroot -hlocalhost --protocol=tcp
Reading datadir from the MariaDB server failed. Got the following error when executing the 'mysql' command line client
ERROR 1193 (HY000) at line 1: Unknown system variable 'WSREP_ON'
FATAL ERROR: Upgrade failed

```
