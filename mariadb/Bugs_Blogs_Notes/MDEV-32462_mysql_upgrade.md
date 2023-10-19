# MDEV-32462

```bash
 ./scripts/mariadb-install-db --srcdir=../../10.5 --defaults-file=~/.my105.cnf
 
 $ cp mysql-test/std_data/mysql_json/mysql_json_test.* /tmp/10.5/mysql/
 
 
 $ ./client/mysql -S /tmp/mysql.sock
MariaDB [mysql]> select * from mysql_json_test;
ERROR 1707 (HY000): Table rebuild required. Please do "ALTER TABLE `mysql.mysql_json_test` FORCE" or dump/reload to fix it!

MariaDB [(none)]> set global general_log=1;
Query OK, 0 rows affected (0.000 sec)

MariaDB [(none)]> select @@general_log;
+---------------+
| @@general_log |
+---------------+
|             1 |
+---------------+
1 row in set (0.000 sec)

MariaDB [(none)]> select @@log_output;
+--------------+
| @@log_output |
+--------------+
| FILE         |
+--------------+
1 row in set (0.000 sec)

MariaDB [(none)]> select @@general_log_file;
+--------------------+
| @@general_log_file |
+--------------------+
| anel.log           |
+--------------------+
1 row in set (0.000 sec)
```

- Run `mariadb-upgrade` and check the general_log_file
```
$ sudo ./client/mariadb-upgrade -s --socket=/tmp/mysql.sock --verbose --force
Looking for 'mariadb' as: ./client/mariadb
Looking for 'mariadb-check' as: ./client/mariadb-check
The --upgrade-system-tables option was used, user tables won't be touched.
Phase 1/7: Checking and upgrading mysql database

mysql.innodb_table_stats                           OK
mysql.mysql_json_test                              Needs upgrade


Repairing tables
mysql.mysql_json_test                              OK
Phase 2/7: Installing used storage engines... Skipped
Phase 3/7: Fixing views... Skipped


$ cat /tmp/10.5/anel.log |grep table_comment
		    13 Query	SELECT table_comment FROM information_schema.tables WHERE table_comment LIKE 'Unknown data type: %'
# see more

		    13 Connect	root@localhost on mysql using Socket
		    13 Query	SET SQL_LOG_BIN=0, WSREP_ON=OFF
		    13 Query	SELECT table_comment FROM information_schema.tables WHERE table_comment LIKE 'Unknown data type: %'

```
 
 - If `log_output=TABLE` than instead from file `SELECT * FROM mysql.general_log` can be obtained from table;
 
 - Scenario 2 - there is user table `mysql_json` (it becomes system table) in `mysql` and upgrade is run with `-s`
 ```bash
 # From source directory
$ cp mysql-test/std_data/mysql_json/mysql_json_test.* /tmp/10.5/mysql/ && cp mysql-test/std_data/mysql_json/mysql_json_test.* /tmp/10.5/test/
 ```
 - 
 ```sql
 MariaDB [mysql]> show tables from test;
+-----------------+
| Tables_in_test  |
+-----------------+
| mysql_json_test |
+-----------------+
1 row in set (0.001 sec)

MariaDB [mysql]> show tables from mysql like '%json%';
+--------------------------+
| Tables_in_mysql (%json%) |
+--------------------------+
| mysql_json_test          |
+--------------------------+
1 row in set (0.001 sec)
```
```bash
MariaDB [mysql]> select * from mysql.mysql_json_test;
ERROR 1707 (HY000): Table rebuild required. Please do "ALTER TABLE `mysql.mysql_json_test` FORCE" or dump/reload to fix it!
MariaDB [mysql]> select * from test.mysql_json_test;
ERROR 1707 (HY000): Table rebuild required. Please do "ALTER TABLE `test.mysql_json_test` FORCE" or dump/reload to fix it!
```

- Check with `mariadb_upgrade`
```bash
$ sudo ./client/mariadb-upgrade -s --socket=/tmp/mysql.sock --verbose
[sudo] password for anel: 
Looking for 'mariadb' as: ./client/mariadb
Looking for 'mariadb-check' as: ./client/mariadb-check
The --upgrade-system-tables option was used, user tables won't be touched.
This installation of MariaDB is already upgraded to 10.5.23-MariaDB.
There is no need to run mysql_upgrade again for 10.5.23-MariaDB.
You can use --force if you still want to run mysql_upgrade


$ sudo ./client/mariadb-upgrade -s --socket=/tmp/mysql.sock --verbose --verbose
Looking for 'mariadb' as: ./client/mariadb
Looking for 'mariadb-check' as: ./client/mariadb-check
The --upgrade-system-tables option was used, user tables won't be touched.
This installation of MariaDB is already upgraded to 10.5.23-MariaDB.
There is no need to run mysql_upgrade again for 10.5.23-MariaDB.
You can use --force if you still want to run mysql_upgrade
Running 'mariadb-check' with connection arguments: --port='3305' --socket='/run/mysqld/mysqld.sock' --socket='/tmp/mysql.sock'

```
- Running with `force`
```
$ sudo ./client/mariadb-upgrade -s --socket=/tmp/mysql.sock --port=3306 --verbose --verbose --verbose --force
[sudo] password for anel: 
Looking for 'mariadb' as: ./client/mariadb
Looking for 'mariadb-check' as: ./client/mariadb-check
The --upgrade-system-tables option was used, user tables won't be touched.
Phase 1/7: Checking and upgrading mysql database
Running 'mariadb-check' with connection arguments: --port='3305' --socket='/run/mysqld/mysqld.sock' --socket='/tmp/mysql.sock' --port='3306' 
# Connecting to localhost...
# Disconnecting from localhost...
Processing databases
mysql
CHECK TABLE `column_stats`  FOR UPGRADE
mysql.column_stats                                 OK
CHECK TABLE `columns_priv`  FOR UPGRADE
mysql.columns_priv                                 OK
CHECK TABLE `db`  FOR UPGRADE
mysql.db                                           OK
CHECK TABLE `event`  FOR UPGRADE
mysql.event                                        OK
CHECK TABLE `func`  FOR UPGRADE
mysql.func                                         OK
CHECK TABLE `global_priv`  FOR UPGRADE
mysql.global_priv                                  OK
CHECK TABLE `gtid_slave_pos`  FOR UPGRADE
mysql.gtid_slave_pos                               OK
CHECK TABLE `help_category`  FOR UPGRADE
mysql.help_category                                OK
CHECK TABLE `help_keyword`  FOR UPGRADE
mysql.help_keyword                                 OK
CHECK TABLE `help_relation`  FOR UPGRADE
mysql.help_relation                                OK
CHECK TABLE `help_topic`  FOR UPGRADE
mysql.help_topic                                   OK
CHECK TABLE `index_stats`  FOR UPGRADE
mysql.index_stats                                  OK
CHECK TABLE `innodb_index_stats`  FOR UPGRADE
mysql.innodb_index_stats                           OK
CHECK TABLE `innodb_table_stats`  FOR UPGRADE
mysql.innodb_table_stats                           OK
CHECK TABLE `mysql_json_test`  FOR UPGRADE
mysql.mysql_json_test                              Needs upgrade
CHECK TABLE `plugin`  FOR UPGRADE
mysql.plugin                                       OK
CHECK TABLE `proc`  FOR UPGRADE
mysql.proc                                         OK
CHECK TABLE `procs_priv`  FOR UPGRADE
mysql.procs_priv                                   OK
CHECK TABLE `proxies_priv`  FOR UPGRADE
mysql.proxies_priv                                 OK
CHECK TABLE `roles_mapping`  FOR UPGRADE
mysql.roles_mapping                                OK
CHECK TABLE `servers`  FOR UPGRADE
mysql.servers                                      OK
CHECK TABLE `table_stats`  FOR UPGRADE
mysql.table_stats                                  OK
CHECK TABLE `tables_priv`  FOR UPGRADE
mysql.tables_priv                                  OK
CHECK TABLE `time_zone`  FOR UPGRADE
mysql.time_zone                                    OK
CHECK TABLE `time_zone_leap_second`  FOR UPGRADE
mysql.time_zone_leap_second                        OK
CHECK TABLE `time_zone_name`  FOR UPGRADE
mysql.time_zone_name                               OK
CHECK TABLE `time_zone_transition`  FOR UPGRADE
mysql.time_zone_transition                         OK
CHECK TABLE `time_zone_transition_type`  FOR UPGRADE
mysql.time_zone_transition_type                    OK
CHECK TABLE `transaction_registry`  FOR UPGRADE
mysql.transaction_registry                         OK

Repairing tables
REPAIR NO_WRITE_TO_BINLOG TABLE `mysql`.`mysql_json_test` 
mysql.mysql_json_test                              OK
Phase 2/7: Installing used storage engines... Skipped
Phase 3/7: Fixing views... Skipped
Phase 4/7: Running 'mysql_fix_privilege_tables'
Phase 5/7: Fixing table and database names ... Skipped
Phase 6/7: Checking and upgrading tables... Skipped
Phase 7/7: Running 'FLUSH PRIVILEGES'
OK
Running 'mariadb-check' with connection arguments: --port='3305' --socket='/run/mysqld/mysqld.sock' --socket='/tmp/mysql.sock' --port='3306' 

```

It is visible in `general_log`
```bash
 17 Connect	root@localhost on mysql using Socket
		    17 Query	SET SQL_LOG_BIN=0, WSREP_ON=OFF
		    17 Query	SELECT table_comment FROM information_schema.tables WHERE table_schema='mysql' and table_comment LIKE 'Unknown data type: %'

```


