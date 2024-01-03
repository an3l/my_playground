# MDEV-26231: mysql_upgrade attempts to remove plugins which it failed to install

Based on https://jira.mariadb.org/browse/MDEV-26230 (insufficient maturity level)
https://github.com/MariaDB/server/commit/e8e755ea6cbac56d561375b940281a903c7db61c#diff-92a5f59b6176fb795210e5c4ab18603360eefcc3273038bb7897fe6515f6c0f6

MariaDB_PLUGIN_MATURITY_ALPHA
mariadb_upgrade may fail during install_plugin, as stated by https://jira.mariadb.org/browse/MDEV-26231 that can lead to new error during uninstall_plugin.
We don't know did we install it plugin and if did that it should be installed, otherwise don't uninstall.


PR https://github.com/MariaDB/server/pull/2840 created


init_dynamic_string(&ds_plugin_data_types, "", 512, 256))
  Allocation of length != 0 -> verify (wrong assumption it is 0)
(gdb) p ds_plugin_data_types 
$2 = {str = 0x55555591ba18 "", length = 0, max_length = 256, alloc_increment = 256}

install_used_plugin_data_types():

(gdb) f 0
#0  install_used_plugin_data_types () at /home/anel/GitHub/mariadb/server/src/10.5/client/mysql_upgrade.c:1156
(gdb) p ds_plugin_data_types 
$2 = {str = 0x55555591ba18 "", length = 0, max_length = 256, alloc_increment = 256}

1. Install plugin (MYSQL_JSON not found):
  (gdb) bt
#0  uninstall_plugins () at /home/anel/GitHub/mariadb/server/src/10.5/client/mysql_upgrade.c:1126
#1  0x000055555557df97 in main (argc=0, argv=0x55555591b6d8) at /home/anel/GitHub/mariadb/server/src/10.5/client/mysql_upgrade.c:1499
(gdb) n
(gdb) p ds_plugin_data_types 
$5 = {str = 0x55555591ba18 "", length = 0, max_length = 256, alloc_increment = 256}


2. Install typy_mysql_json OK:
   dynstr_append(&ds_plugin_data_types, "'type_mysql_json'");
 
3. Install typy_mysql_json failed NOT OK:
  allocated length still !=0 < prove !
  
  
  
# 
- Start the server
```
$ ./sql/mariadbd --defaults-file=~/.my105.cnf --datadir=/home/anel/GitHub/mariadb/mysql-data-dir-test
2023-11-30 14:04:15 0 [ERROR] Missing system table mysql.roles_mapping; please run mysql_upgrade to create it
2023-11-30 14:04:15 0 [ERROR] Incorrect definition of table mysql.event: expected column 'sql_mode' at position 14 to have type set('REAL_AS_FLOAT','PIPES_AS_CONCAT','ANSI_QUOTES','IGNORE_SPACE','IGNORE_BAD_TABLE_OPTIONS','ONLY_FULL_GROUP_BY','NO_UNSIGNED_SUBTRACTION','NO_DIR_IN_CREATE','POSTGRESQL','ORACLE','MSSQL','DB2','MAXDB','NO_KEY_OPTIONS','NO_TABLE_OPTIONS','NO_FIELD_OPTIONS','MYSQL323','MYSQL40','ANSI','NO_AUTO_VALUE_ON_ZERO','NO_BACKSLASH_ESCAPES','STRICT_TRANS_TABLES','STRICT_ALL_TABLES','NO_ZERO_IN_DATE','NO_ZERO_DATE','INVALID_DATES','ERROR_FOR_DIVISION_BY_ZERO','TRADITIONAL','NO_AUTO_CREATE_USER','HIGH_NOT_PRECEDENCE','NO_ENGINE_SUBSTITUTION','PAD_CHAR_TO_FULL_LENGTH','EMPTY_STRING_IS_NULL','SIMULTANEOUS_ASSIGNMENT'), found type set('REAL_AS_FLOAT','PIPES_AS_CONCAT','ANSI_QUOTES','IGNORE_SPACE','NOT_USED','ONLY_FULL_GROUP_BY','NO_UNSIGNED_SUBTRACTION','NO_DIR_IN_CREATE','POSTGRESQL','ORACLE','MSSQL','DB2','MAXDB','NO_KEY_OPTIONS','NO_TABLE_OPTIONS','NO_FIELD_OPTIONS','MYSQL323','MYSQL40','ANSI','NO_AUTO_VALUE_ON_ZERO','NO_B
2023-11-30 14:04:15 0 [ERROR] mariadbd: Event Scheduler: An error occurred when initializing system tables. Disabling the Event Scheduler.
2023-11-30 14:04:15 1 [Warning] Failed to load slave replication state from table mysql.gtid_slave_pos: 1146: Table 'mysql.gtid_slave_pos' doesn't exist
2023-11-30 14:04:15 0 [Note] Reading of all Master_info entries succeeded
2023-11-30 14:04:15 0 [Note] Added new Master_info '' to hash table
2023-11-30 14:04:15 0 [Note] ./sql/mariadbd: ready for connections.
Version: '10.5.24-MariaDB-debug-log'  socket: '/tmp/mysql.sock'  port: 3306  Source distribution
```
- Check the client `mariadb`
```
$ sudo ./client/mysql -S /tmp/mysql.sock 
[sudo] password for anel: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 4
Server version: 10.5.24-MariaDB-debug-log Source distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test               |
+--------------------+
5 rows in set (0.001 sec)

MariaDB [(none)]> use test;
# 2023-11-30 14:06:11 4 [ERROR] mariadbd: Table rebuild required. Please do "ALTER TABLE `test.t` FORCE" or dump/reload to fix it!
MariaDB [test]> show create table t;
ERROR 1707 (HY000): Table rebuild required. Please do "ALTER TABLE `test.t` FORCE" or dump/reload to fix it!

MariaDB [(none)]> show plugins;

| MYSQL_JSON                    | ACTIVE   | DATA TYPE          | type_mysql_json.so | GPL     |
+-------------------------------+----------+--------------------+--------------------+---------+
```

- We don't get any more same error message
```
MariaDB [(none)]> select * from information_schema.tables where table_name='t';
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+-------------+-------------+------------+-----------------+----------+----------------+------------------------------------------------------------------------------------------+------------------+-----------+
| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | TABLE_TYPE | ENGINE | VERSION | ROW_FORMAT | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH | MAX_DATA_LENGTH | INDEX_LENGTH | DATA_FREE | AUTO_INCREMENT | CREATE_TIME | UPDATE_TIME | CHECK_TIME | TABLE_COLLATION | CHECKSUM | CREATE_OPTIONS | TABLE_COMMENT                                                                            | MAX_INDEX_LENGTH | TEMPORARY |
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+-------------+-------------+------------+-----------------+----------+----------------+------------------------------------------------------------------------------------------+------------------+-----------+
| def           | test         | t          | BASE TABLE | NULL   |    NULL | NULL       |       NULL |           NULL |        NULL |            NULL |         NULL |      NULL |           NULL | NULL        | NULL        | NULL       | NULL            |     NULL | NULL           | Table rebuild required. Please do "ALTER TABLE `test.t` FORCE" or dump/reload to fix it! |             NULL | NULL      |
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+-------------+-------------+------------+-----------------+----------+----------------+------------------------------------------------------------------------------------------+------------------+-----------+
1 row in set, 1 warning (0.001 sec)


```

- Check the client `mariadb_upgrade`
By starting we got the error in server
```
2023-11-30 14:07:23 8 [ERROR] InnoDB: Column last_update in table `mysql`.`innodb_table_stats` is BINARY(4) NOT NULL but should be INT UNSIGNED NOT NULL (flags mismatch).
2023-11-30 14:07:23 8 [ERROR] InnoDB: Fetch of persistent statistics requested for table `mysql`.`gtid_executed` but the required system tables mysql.innodb_table_stats and mysql.innodb_index_stats are not present or have unexpected structure. Using transient stats instead.
2023-11-30 14:07:23 10 [ERROR] mariadbd: Table rebuild required. Please do "ALTER TABLE `test.t` FORCE" or dump/reload to fix it!

```


# Bug
```
MariaDB [(none)]> select * from information_schema.tables where table_name='t'
    -> \G
*************************** 1. row ***************************
   TABLE_CATALOG: def
    TABLE_SCHEMA: test
      TABLE_NAME: t
      TABLE_TYPE: BASE TABLE
          ENGINE: NULL
         VERSION: NULL
      ROW_FORMAT: NULL
      TABLE_ROWS: NULL
  AVG_ROW_LENGTH: NULL
     DATA_LENGTH: NULL
 MAX_DATA_LENGTH: NULL
    INDEX_LENGTH: NULL
       DATA_FREE: NULL
  AUTO_INCREMENT: NULL
     CREATE_TIME: NULL
     UPDATE_TIME: NULL
      CHECK_TIME: NULL
 TABLE_COLLATION: NULL
        CHECKSUM: NULL
  CREATE_OPTIONS: NULL
   TABLE_COMMENT: Table rebuild required. Please do "ALTER TABLE `test.t` FORCE" or dump/reload to fix it!
MAX_INDEX_LENGTH: NULL
       TEMPORARY: NULL
1 row in set, 1 warning (0.001 sec)

MariaDB [(none)]> select table_comment from information_schema.tables where table_name='t'
    -> \G
Empty set (0.001 sec)

MariaDB [(none)]> select table_type from information_schema.tables where table_name='t';
Empty set (0.001 sec)
2023-11-30 14:16:53 12 [ERROR] mariadbd: Table rebuild required. Please do "ALTER TABLE `test.t` FORCE" or dump/reload to fix it!

MariaDB [(none)]> select table_type from information_schema.tables where table_schema='test';
Empty set (0.001 sec)

MariaDB [(none)]> select table_type from information_schema.tables where table_name='innodb_index_stats';
+------------+
| table_type |
+------------+
| BASE TABLE |
+------------+
1 row in set (0.001 sec)

```

- This works
```
MariaDB [(none)]> select * from information_schema.tables where table_comment LIKE 'Table rebuild required. Please do "ALTER TABLE %'\G
*************************** 1. row ***************************
   TABLE_CATALOG: def
    TABLE_SCHEMA: test
      TABLE_NAME: t
      TABLE_TYPE: BASE TABLE
          ENGINE: NULL
         VERSION: NULL
      ROW_FORMAT: NULL
      TABLE_ROWS: NULL
  AVG_ROW_LENGTH: NULL
     DATA_LENGTH: NULL
 MAX_DATA_LENGTH: NULL
    INDEX_LENGTH: NULL
       DATA_FREE: NULL
  AUTO_INCREMENT: NULL
     CREATE_TIME: NULL
     UPDATE_TIME: NULL
      CHECK_TIME: NULL
 TABLE_COLLATION: NULL
        CHECKSUM: NULL
  CREATE_OPTIONS: NULL
   TABLE_COMMENT: Table rebuild required. Please do "ALTER TABLE `test.t` FORCE" or dump/reload to fix it!
MAX_INDEX_LENGTH: NULL
       TEMPORARY: NULL
1 row in set, 50 warnings (0.055 sec)

MariaDB [(none)]> show warnings;
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                  |
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1707 | Table rebuild required. Please do "ALTER TABLE `test.t` FORCE" or dump/reload to fix it!                                                                 |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1356 | View 'sys.metrics' references invalid table(s) or column(s) or function(s) or definer/invoker of view lack rights to use them                            |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
| Warning | 1558 | Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error |
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------+
50 rows in set (0.001 sec)

```

- This doesn't work
```
MariaDB [(none)]> select table_comment from information_schema.tables where table_comment LIKE 'Table rebuild required. Please do "ALTER TABLE %'\G
Empty set (0.016 sec)

MariaDB [(none)]> show warnings;
Empty set (0.000 sec)
# Although the error appeared in the server
2023-11-30 14:19:48 12 [ERROR] mariadbd: Table rebuild required. Please do "ALTER TABLE `test.t` FORCE" or dump/reload to fix it!

```

- Run upgrade (when plugin is installed) plugin_load_add= type_mysql_json.so
```
$ sudo ./client/mysql_upgrade -uroot -S /tmp/mysql.sock 
MariaDB upgrade detected
Phase 1/7: Checking and upgrading mysql database
Processing databases
mysql
mysql.columns_priv                                 OK
mysql.db                                           OK
mysql.engine_cost                                  OK
mysql.event                                        OK
mysql.func                                         OK
mysql.gtid_executed                                OK
mysql.help_category                                OK
mysql.help_keyword                                 OK
mysql.help_relation                                OK
mysql.help_topic                                   OK
mysql.innodb_index_stats                           OK
mysql.innodb_table_stats                           OK
mysql.ndb_binlog_index                             OK
mysql.plugin                                       OK
mysql.proc                                         OK
mysql.procs_priv                                   OK
mysql.proxies_priv                                 OK
mysql.server_cost                                  OK
mysql.servers                                      OK
mysql.slave_master_info                            OK
mysql.slave_relay_log_info                         OK
mysql.slave_worker_info                            OK
mysql.tables_priv                                  OK
mysql.time_zone                                    OK
mysql.time_zone_leap_second                        OK
mysql.time_zone_name                               OK
mysql.time_zone_transition                         OK
mysql.time_zone_transition_type                    OK
mysql.user                                         OK
Upgrading from a version before MariaDB-10.1
Phase 2/7: Installing used storage engines
Checking for tables with unknown storage engine
Phase 3/7: Fixing views from mysql
sys.host_summary
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.host_summary_by_file_io
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.host_summary_by_file_io_type
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.host_summary_by_stages
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.host_summary_by_statement_latency
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.host_summary_by_statement_type
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.innodb_buffer_stats_by_schema
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.innodb_buffer_stats_by_table
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.innodb_lock_waits
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.io_by_thread_by_latency
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.io_global_by_file_by_bytes
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.io_global_by_file_by_latency
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.io_global_by_wait_by_bytes
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.io_global_by_wait_by_latency
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.latest_file_io
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.memory_by_host_by_current_bytes
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.memory_by_thread_by_current_bytes
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.memory_by_user_by_current_bytes
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.memory_global_by_current_bytes
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.memory_global_total
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.metrics
Error    : Unknown column 'information_schema.INNODB_METRICS.STATUS' in 'field list'
Error    : View 'sys.metrics' references invalid table(s) or column(s) or function(s) or definer/invoker of view lack rights to use them
error    : Corrupt
sys.processlist
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.ps_check_lost_instrumentation                  OK
sys.schema_auto_increment_columns                  OK
sys.schema_index_statistics
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.schema_object_overview                         OK
sys.schema_redundant_indexes                       OK
sys.schema_table_lock_waits
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.schema_table_statistics
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.schema_table_statistics_with_buffer
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.schema_tables_with_full_table_scans
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.schema_unused_indexes                          OK
sys.session
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.session_ssl_status                             OK
sys.statement_analysis
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.statements_with_errors_or_warnings
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.statements_with_full_table_scans
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.statements_with_runtimes_in_95th_percentile
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.statements_with_sorting
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.statements_with_temp_tables
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.user_summary
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.user_summary_by_file_io
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.user_summary_by_file_io_type
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.user_summary_by_stages
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.user_summary_by_statement_latency
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.user_summary_by_statement_type
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.version                                        OK
sys.wait_classes_global_by_avg_latency
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.wait_classes_global_by_latency
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.waits_by_host_by_latency
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.waits_by_user_by_latency
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.waits_global_by_latency
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
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
sys.x$ps_schema_table_statistics_io
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.x$schema_flattened_keys                        OK
sys.x$schema_index_statistics                      OK
sys.x$schema_table_lock_waits
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.x$schema_table_statistics
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
sys.x$schema_table_statistics_with_buffer
Error    : Column count of mysql.proc is wrong. Expected 21, found 20. Created with MariaDB 50744, now running 100524. Please use mariadb-upgrade to fix this error
error    : Corrupt
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
Phase 4/7: Running 'mysql_fix_privilege_tables'
Phase 5/7: Fixing table and database names
Phase 6/7: Checking and upgrading tables
Processing databases
information_schema
performance_schema
sys
sys.sys_config                                     OK
test
test.t                                             Needs upgrade

Repairing tables
test.t                                             OK
Phase 7/7: Running 'FLUSH PRIVILEGES'
OK

```


- Run upgrade (when plugin is not installed) plugin_load_add= type_mysql_json.so 
  and if we fail on query to install the plugin
  
```
MariaDB [test]> show create table t;
ERROR 4161 (HY000): Unknown data type: 'MYSQL_JSON'

```
- No error on server side
- Run `mariadb_upgrade`
```
Phase 2/7: Installing used storage engines
Checking for tables with unknown storage engine
installing plugin for MYSQL_JSON data type
ERROR 1126 (HY000) at line 1: Can't open shared library '/home/anel/GitHub/mariadb/server/build/10.5/plugin/type_mysql_json/type_mysql_json1.so' (errno: 2, cannot open shared object file: No such file or directory)

test.t
Error    : Unknown data type: 'MYSQL_JSON'
error    : Corrupt

Repairing tables
test.t
Error    : Unknown data type: 'MYSQL_JSON'
error    : Corrupt
uninstalling plugin for 'type_mysql_json' data type
ERROR 1305 (42000) at line 1: SONAME type_mysql_json.so does not exist



```


```
(gdb) p ds_result
$5 = {str = 0x55555591be48 "ERROR 1126 (HY000) at line 1: Can't open shared library '/home/anel/GitHub/mariadb/server/build/10.5/plugin/type_mysql_json/type_mysql_json1.so' (errno: 2, cannot open shared object file: No such file"..., length = 215, max_length = 512,
  alloc_increment = 512}
```

- Alternative
if(!run_query("INSTALL SONAME 'type_mysql_json1'", &ds_result, TRUE))
```
$ sudo ./client/mysql_upgrade -uroot -S /tmp/mysql.sock --force
Phase 1/7: Checking and upgrading mysql database
Processing databases
mysql
mysql.column_stats                                 OK
mysql.columns_priv                                 OK
mysql.db                                           OK
mysql.engine_cost                                  OK
mysql.event                                        OK
mysql.func                                         OK
mysql.global_priv                                  OK
mysql.gtid_executed                                OK
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
mysql.server_cost                                  OK
mysql.servers                                      OK
mysql.slave_master_info                            OK
mysql.slave_relay_log_info                         OK
mysql.slave_worker_info                            OK
mysql.table_stats                                  OK
mysql.tables_priv                                  OK
mysql.time_zone                                    OK
mysql.time_zone_leap_second                        OK
mysql.time_zone_name                               OK
mysql.time_zone_transition                         OK
mysql.time_zone_transition_type                    OK
mysql.transaction_registry                         OK
Phase 2/7: Installing used storage engines... Skipped
installing plugin for MYSQL_JSON data type
Failed to install the plugin 'type_mysql_json' for MYSQL_JSON data type
FATAL ERROR: Upgrade failed
```
