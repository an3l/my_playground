mariadb-upgrade

# Testing 10.4 access from root and normal user / weird behaviour
- Create datadir
```bash
$ ./scripts/mysql_install_db --srcdir=../../src/10.4 --datadir=../../datadir/10.4
Installing MariaDB/MySQL system tables in '../../datadir/10.4' ...
OK
```
- Check configuration:
```config
$ cat ~/.my104.cnf
[mariadb]
datadir=/home/anel/GitHub/mariadb/server/datadir/10.4
#datadir=/tmp/10.4
lc_messages_dir=/home/anel/GitHub/mariadb/server/build/10.4/sql/share
#plugin_load_add=ha_connect.so
#plugin_dir=/home/anel/GitHub/mariadb/server/build/10.3/storage/connect
```
- Start the server
```bash
$ ./sql/mysqld --defaults-file=~/.my104.cnf
2023-03-13 13:14:17 0 [Note] Starting MariaDB 10.4.29-MariaDB-debug source revision 3b3eda53632d99e33845ad375889a099309b81b8 as process 32690
2023-03-13 13:14:17 0 [Note] InnoDB: !!!!!!!! UNIV_DEBUG switched on !!!!!!!!!
2023-03-13 13:14:17 0 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
2023-03-13 13:14:17 0 [Note] InnoDB: Uses event mutexes
2023-03-13 13:14:17 0 [Note] InnoDB: Compressed tables use zlib 1.2.11
2023-03-13 13:14:17 0 [Note] InnoDB: Number of pools: 1
2023-03-13 13:14:17 0 [Note] InnoDB: Using SSE2 crc32 instructions
2023-03-13 13:14:17 0 [Note] InnoDB: Initializing buffer pool, total size = 128M, instances = 1, chunk size = 128M
2023-03-13 13:14:18 0 [Note] InnoDB: Completed initialization of buffer pool
2023-03-13 13:14:18 0 [Note] InnoDB: If the mysqld execution user is authorized, page cleaner thread priority can be changed. See the man page of setpriority().
2023-03-13 13:14:18 0 [Note] InnoDB: 128 out of 128 rollback segments are active.
2023-03-13 13:14:18 0 [Note] InnoDB: Creating shared tablespace for temporary tables
2023-03-13 13:14:18 0 [Note] InnoDB: Setting file './ibtmp1' size to 12 MB. Physically writing the file full; Please wait ...
2023-03-13 13:14:18 0 [Note] InnoDB: File './ibtmp1' size is now 12 MB.
2023-03-13 13:14:18 0 [Note] InnoDB: Waiting for purge to start
2023-03-13 13:14:18 0 [Note] InnoDB: 10.4.29 started; log sequence number 61535; transaction id 20
2023-03-13 13:14:18 0 [Note] InnoDB: Loading buffer pool(s) from /home/anel/GitHub/mariadb/server/datadir/10.4/ib_buffer_pool
2023-03-13 13:14:18 0 [Note] Plugin 'FEEDBACK' is disabled.
2023-03-13 13:14:18 0 [Note] InnoDB: Buffer pool(s) load completed at 230313 13:14:18
2023-03-13 13:14:18 0 [Note] Server socket created on IP: '::'.
2023-03-13 13:14:18 0 [ERROR] Can't start server : Bind on unix socket: Address already in use
2023-03-13 13:14:18 0 [ERROR] Do you already have another mysqld server running on socket: /tmp/mysql.sock ?
2023-03-13 13:14:18 0 [ERROR] Aborting
```

And there is no socket listening (in `/run/`)
```bash
$ ss -l|grep tmp
```
- When run systemd process (socket is in `/var/run/mysqld/mysqld.sock`):
```bash
$ ls /var/run/mysqld/mysqld.sock 
/var/run/mysqld/mysqld.sock

$ ss -l |grep mysql
u_str  LISTEN  0       80                               /run/mysqld/mysqld.sock 149636                                           * 0                            
tcp    LISTEN  0       80                                             127.0.0.1:mysql                                      0.0.0.0:* 
```

Note ^ is unix socket (there is also netlink) that are used to [communicate with local kernel](https://unix.stackexchange.com/questions/309083/how-do-i-list-all-sockets-which-are-open-to-remote-machines)


# Working example with defaults-file and root
```bash
$ sudo ./client/mariadb-upgrade --defaults-file=/home/anel/.my104.cnf -vv -uroot
Looking for 'mysql' as: ./client/mysql
Looking for 'mysqlcheck' as: ./client/mysqlcheck
This installation of MariaDB is already upgraded to 10.4.29-MariaDB.
There is no need to run mysql_upgrade again for 10.4.29-MariaDB.
You can use --force if you still want to run mysql_upgrade
Running 'mariadb-check' with connection arguments: --socket='/tmp/anel.sock' 
```


## Different versions of server and client
```bash
$ sudo ./client/mariadb-upgrade --defaults-file=/home/anel/.my104.cnf -vv -uroot
Looking for 'mysql' as: ./client/mysql
Looking for 'mysqlcheck' as: ./client/mysqlcheck
Empty or non existent /home/anel/GitHub/mariadb/server/datadir/11.0/mysql_upgrade_info. Assuming mysql_upgrade has to be run!
Error: Server version (11.0.1-MariaDB-debug) does not match with the version of
the server (10.4.29-MariaDB) with which this program was built/distributed. You can
use --skip-version-check to skip this check.
Running 'mariadb-check' with connection arguments: --socket='/tmp/anel.sock' 
FATAL ERROR: Upgrade failed
```
# Previous tests
1. Error in documentation

- single time - more information
```bash
$ sudo mysql_upgrade -vv -uroot
Looking for 'mariadb' as: mariadb
Looking for 'mariadb-check' as: mariadb-check
This installation of MariaDB is already upgraded to 10.6.11-MariaDB.
There is no need to run mysql_upgrade again for 10.6.12-MariaDB.
You can use --force if you still want to run mysql_upgrade
```

- double time - connectino arguments - not visible for empty - but should ! `run_mysqlcheck_upgrade` -> `print_conn_args` -> here checks for 3 level 
```bash
$ sudo mysql_upgrade -vv -uroot
Looking for 'mariadb' as: mariadb
Looking for 'mariadb-check' as: mariadb-check
This installation of MariaDB is already upgraded to 10.6.11-MariaDB.
There is no need to run mysql_upgrade again for 10.6.12-MariaDB.
You can use --force if you still want to run mysql_upgrade
```

- 3. time - use check/rename/alter table commands - not visible for empty
```bash
$ sudo mysql_upgrade -vvv -uroot
Looking for 'mariadb' as: mariadb
Looking for 'mariadb-check' as: mariadb-check
This installation of MariaDB is already upgraded to 10.6.11-MariaDB.
There is no need to run mysql_upgrade again for 10.6.12-MariaDB.
You can use --force if you still want to run mysql_upgrade
```

- 4.time - will show mysqlcheck commands - visible for empty
```bash
$ sudo mysql_upgrade -vvvv -uroot
Looking for 'mariadb' as: mariadb
'mariadb' --no-defaults --help 2>&1 > /dev/null 
'mariadb' --defaults-file=/tmp/mysql_upgrade-T2knE4 --database=mysql --batch --skip-force --silent < /tmp/sqlUcF5V5 2>&1 
Looking for 'mariadb-check' as: mariadb-check
'mariadb-check' --no-defaults --help 2>&1 > /dev/null 
This installation of MariaDB is already upgraded to 10.6.11-MariaDB.
There is no need to run mysql_upgrade again for 10.6.12-MariaDB.
You can use --force if you still want to run mysql_upgrade
```

- Potential bug `run_mysqlcheck_views` -> `print_conn_args` (on mysqlcheck, while mysqlcheck_upgrade runs on mariadb-check) - here adds 1 level
                `run_mysqlcheck_fixnames`->-- (here checks for 3 level for mysqlcheck)
                
                


- NOT A BUG with message in mariadb_upgrade
Noticed that when upgrading from 10.6.11 -> 10.6.12 {{mysql_upgrade_info}} file wasn't updated, which means that upgrade of data directory wasn't executed (based on [KB|https://mariadb.com/kb/en/mysql_upgrade/])
However, after checking the upgrade, it say it is already updated to installed/old version and that there is no need to update to current/higher version.
However with major upgrade from 10.6.11 -> 10.11 the message correclty identifies the running server and 

```bash
$ cat /etc/apt/sources.list.d/mariadb.org.list 
deb [arch=amd64] https://ftp.bme.hu/pub/mirrors/mariadb/repo/10.6/ubuntu focal main

$ dpkg -l mariadb-server
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name           Version                 Architecture Description
+++-==============-=======================-============-=====================================================================
ii  mariadb-server 1:10.6.12+maria~ubu2004 all          MariaDB database server (metapackage depending on the latest version)


# Server version
$ sudo mysqld --version
mysqld  Ver 10.6.12-MariaDB-1:10.6.12+maria~ubu2004 for debian-linux-gnu on x86_64 (mariadb.org binary distribution)

# Upgrade version
$ sudo mysql_upgrade -uroot --version
mysql_upgrade  Ver 2.0 Distrib 10.6.12-MariaDB, for debian-linux-gnu (x86_64)


# Run upgrade (10.6.11? instead of 10.6.12)
$ sudo mysql_upgrade -uroot
This installation of MariaDB is already upgraded to 10.6.11-MariaDB.
There is no need to run mysql_upgrade again for 10.6.12-MariaDB.
You can use --force if you still want to run mysql_upgrade

#Datadir
$ echo " show variables like 'datadir'" | sudo mysql -uroot
Variable_name	Value
datadir	/var/lib/mysql/

# mysql_upgrade_info has lower version
$ cat /var/lib/mysql/mysql_upgrade_info 
10.6.11-MariaDB
```

```bash
# Try different version
$ sudo ./client/mariadb-upgrade -uroot --version
./client/mariadb-upgrade  Ver 2.0 Distrib 10.11.2-MariaDB, for Linux (x86_64)


# This happens (error message correctly identified server version, different than mariadb_upgrade version):
$ sudo ./client/mariadb-upgrade -uroot
Major version upgrade detected from 10.6.11-MariaDB to 10.11.2-MariaDB. Check required!
Error: Server version (10.6.12-MariaDB-1:10.6.12+maria~ubu2004) does not match with the version of
the server (10.11.2-MariaDB) with which this program was built/distributed. You can
use --skip-version-check to skip this check.
FATAL ERROR: Upgrade failed

```
- When I used `--force` 
```bash
$ sudo mysql_upgrade -uroot --force
Phase 1/7: Checking and upgrading mysql database
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
Phase 2/7: Installing used storage engines... Skipped
Phase 3/7: Fixing views
mysql.user                                         OK
sys.host_summary
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.host_summary_by_file_io
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.host_summary_by_file_io_type
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.host_summary_by_stages
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.host_summary_by_statement_latency
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.host_summary_by_statement_type
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.innodb_buffer_stats_by_schema
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.innodb_buffer_stats_by_table
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.innodb_lock_waits
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.io_by_thread_by_latency
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.io_global_by_file_by_bytes
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.io_global_by_file_by_latency
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.io_global_by_wait_by_bytes
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.io_global_by_wait_by_latency
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.latest_file_io
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.memory_by_host_by_current_bytes
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.memory_by_thread_by_current_bytes
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.memory_by_user_by_current_bytes
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.memory_global_by_current_bytes
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.memory_global_total
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.metrics                                        OK
sys.processlist
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.ps_check_lost_instrumentation                  OK
sys.schema_auto_increment_columns                  OK
sys.schema_index_statistics
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.schema_object_overview                         OK
sys.schema_redundant_indexes                       OK
sys.schema_table_lock_waits
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.schema_table_statistics
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.schema_table_statistics_with_buffer
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.schema_tables_with_full_table_scans
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.schema_unused_indexes                          OK
sys.session
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.session_ssl_status                             OK
sys.statement_analysis
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.statements_with_errors_or_warnings
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.statements_with_full_table_scans
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.statements_with_runtimes_in_95th_percentile
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.statements_with_sorting
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.statements_with_temp_tables
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.user_summary
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.user_summary_by_file_io
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.user_summary_by_file_io_type
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.user_summary_by_stages
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.user_summary_by_statement_latency
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.user_summary_by_statement_type
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.version                                        OK
sys.wait_classes_global_by_avg_latency
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.wait_classes_global_by_latency
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.waits_by_host_by_latency
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.waits_by_user_by_latency
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.waits_global_by_latency
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
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
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.x$schema_flattened_keys                        OK
sys.x$schema_index_statistics                      OK
sys.x$schema_table_lock_waits
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.x$schema_table_statistics
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
error    : Corrupt
sys.x$schema_table_statistics_with_buffer
Error    : Cannot load from mysql.proc. The table is probably corrupted
Error    : Cannot load from mysql.proc. The table is probably corrupted
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
myEnrollmentDB
myEnrollmentDB.auth_group                          OK
myEnrollmentDB.auth_group_permissions              OK
myEnrollmentDB.auth_permission                     OK
myEnrollmentDB.cantons                             OK
myEnrollmentDB.courses_secondary                   OK
myEnrollmentDB.django_admin_log                    OK
myEnrollmentDB.django_content_type                 OK
myEnrollmentDB.django_migrations                   OK
myEnrollmentDB.django_session                      OK
myEnrollmentDB.secondarySchools                    OK
myEnrollmentDB.teachers                            OK
myEnrollmentDB.teachers_groups                     OK
myEnrollmentDB.teachers_user_permissions           OK
performance_schema
sys
sys.sys_config                                     OK
test
test.myjsontbl                                     OK
user1DB
Phase 7/7: Running 'FLUSH PRIVILEGES'
OK

```
I do get new version of `mariadb_upgrade_info` file
```bash
$ cat /var/lib/mysql/mysql_upgrade_info 
10.6.12-MariaDB
```
And how to check verbosity
```bash
$ sudo mysql_upgrade -uroot  -vvv
Looking for 'mariadb' as: mariadb
Looking for 'mariadb-check' as: mariadb-check
This installation of MariaDB is already upgraded to 10.6.12-MariaDB.
There is no need to run mysql_upgrade again for 10.6.12-MariaDB.
You can use --force if you still want to run mysql_upgrade

$ sudo mysql_upgrade -uroot  -vvvv
Looking for 'mariadb' as: mariadb
'mariadb' --no-defaults --help 2>&1 > /dev/null 
'mariadb' --defaults-file=/tmp/mysql_upgrade-YV5a2J --database=mysql --batch --skip-force --silent < /tmp/sqlSnq28J 2>&1 
Looking for 'mariadb-check' as: mariadb-check
'mariadb-check' --no-defaults --help 2>&1 > /dev/null 
This installation of MariaDB is already upgraded to 10.6.12-MariaDB.
There is no need to run mysql_upgrade again for 10.6.12-MariaDB.
You can use --force if you still want to run mysql_upgrade

```


## Test verbose of mysql client
- More options - [table like structure](https://mariadb.com/kb/en/mysql-command-line-client/)

```bash
$ echo "show variables like 'datadir'" | sudo mysql -uroot
Variable_name	Value
datadir	/var/lib/mysql/


$ echo "show variables like 'datadir'" | sudo mysql -uroot -v
--------------
show variables like 'datadir'
--------------

Variable_name	Value
datadir	/var/lib/mysql/

$ echo "show variables like 'datadir'" | sudo mysql -uroot -vv
--------------
show variables like 'datadir'
--------------

Variable_name	Value
datadir	/var/lib/mysql/
1 row in set

Bye

$ echo "show variables like 'datadir'" | sudo mysql -uroot -vvv
--------------
show variables like 'datadir'
--------------

+---------------+-----------------+
| Variable_name | Value           |
+---------------+-----------------+
| datadir       | /var/lib/mysql/ |
+---------------+-----------------+
1 row in set (0.001 sec)

Bye

```


## Perform upgrade on old datadir

```bash
$ sudo systemctl stop mariadb
# -----------------------
# Create 10.4 binaries
# Create 10.4 datadir
$ ./scripts/mysql_install_db --srcdir=../../src/10.4 --datadir=../../datadir/10.4
# Copy to /tmp
$ cp -r 10.4/ /tmp/
# -----------------------
# MY EXCERSISE - error generated
# Start mariadb-10.4 (using non-existing socket)
# $ ./sql/mysqld --datadir=/tmp/10.4 --socket=/tmp/mysql.sock
# signal 6 - #SIGABRT man signal.7
2023-03-07 13:39:57 0 [ERROR] mysqld: Can't create/write to file '/run/mysqld/mysqld.pid' (Errcode: 13 "Permission denied")
2023-03-07 13:39:57 0 [ERROR] Can't start server: can't create PID file: Permission denied
mysqld: /home/anel/GitHub/mariadb/server/src/10.4/storage/innobase/sync/sync0debug.cc:1506: CreateTracker::~CreateTracker(): Assertion `m_files.empty()' failed.
# -----------------------
# While with `sudo` works: 
# $ sudo ./sql/mysqld --datadir=/tmp/10.4 --socket=/tmp/mysql.sock -uroot
# -----------------------
# While this doesn't work
$ sudo ./sql/mysqld --defaults-file=~/.my104.cnf
Could not open required defaults file: /root/.my104.cnf
Fatal error in defaults handling. Program aborted
# -----------------------
# While this works (using config file) < proceed with this! This will create socket
sudo ./sql/mysqld --defaults-file=/home/anel/.my104.cnf -uroot
# Create some table
$ sudo ./client/mysql -uroot -S /tmp/mysql.sock
# Check info file
$ cat /tmp/10.4/mysql_upgrade_info 
10.4.29-MariaDB

# ----------------------------------------------------------------------------------
# Start 10.11 on 10.4 datadirectory
# Stop 10.4 server, and start 10.11
$ sudo ./sql/mysqld --datadir=/tmp/10.4 -uroot
# ----------------------------------------------------------------------------------
# Perform update
$ sudo ./client/mariadb-upgrade -uroot
Major version upgrade detected from 10.4.29-MariaDB to 10.11.2-MariaDB. Check required!
Phase 1/7: Checking and upgrading mysql database
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
Phase 2/7: Installing used storage engines... Skipped
Phase 3/7: Fixing views
mysql.user                                         OK
Phase 4/7: Running 'mysql_fix_privilege_tables'
Phase 5/7: Fixing table and database names
Phase 6/7: Checking and upgrading tables
Processing databases
information_schema
performance_schema
sys
sys.sys_config                                     OK
test
test.t                                             OK
Phase 7/7: Running 'FLUSH PRIVILEGES'
OK
# ----------------------------------------------------------------------------------
# Start 10.11 major upgrade from 10.4 (using the socket) with running 10.4 server
$ sudo ./client/mysql_upgrade -uroot -S /tmp/mysql.sock
Major version upgrade detected from 10.4.29-MariaDB to 10.11.2-MariaDB. Check required!
Error: Server version (10.4.29-MariaDB-debug) does not match with the version of
the server (10.11.2-MariaDB) with which this program was built/distributed. You can
use --skip-version-check to skip this check.
FATAL ERROR: Upgrade failed
```

- There was an idea to remove `--silent` if `--verbose` exist, but I got the error
```bash
+++ b/client/mysql_upgrade.c
@@ -640,7 +640,7 @@ static int run_query(const char *query, DYNAMIC_STRING *ds_res,
                 "--database=mysql",
                 "--batch", /* Turns off pager etc. */
                 force ? "--force": "--skip-force",
-                ds_res || opt_silent ? "--silent": "",
+                (ds_res || opt_silent) && (!opt_verbose) ? "--silent": "",
                 "<",

Looking for 'mariadb' as: /home/anel/GitHub/mariadb/server/build/10.11/client/mariadb
'/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb' --no-defaults --help 2>&1 > /dev/null 
[Detaching after vfork from child process 65298]
'/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb' --defaults-file=/tmp/mysql_upgrade-mOL6Lp --database=mysql --batch --skip-force  < /tmp/sqlrcYxop 2>&1 
[Detaching after vfork from child process 65300]
FATAL ERROR: Could not open or create the upgrade info file 'Value/mysql_upgrade_info' in the MariaDB Servers data directory, errno: 2 (No such file or directory)

```

- Error when downgrading
```bash
$ sudo ./client/mariadb-upgrade -vv -uroot
Looking for 'mysql' as: ./client/mysql
Looking for 'mysqlcheck' as: ./client/mysqlcheck
FATAL ERROR: Version mismatch (10.6.12-MariaDB -> 10.4.29-MariaDB): Trying to downgrade from a higher to lower version is not supported!

```

