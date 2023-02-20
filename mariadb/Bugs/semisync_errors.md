### breakpoints
b register_slave
b show_slave_hosts
b report_reply_binlog
b show_slave_hosts_callback

### BLANK state:

```
$ ./mysql-test/mtr rpl_semi_sync_slave_report
Logging: /home/anel/GitHub/mariadb/server/src/10.9/mysql-test/mariadb-test-run.pl  rpl_semi_sync_slave_report
VS config:
vardir: /home/anel/GitHub/mariadb/server/build/10.9/mysql-test/var
Checking leftover processes...
Removing old var directory...
Creating var directory '/home/anel/GitHub/mariadb/server/build/10.9/mysql-test/var'...
Checking supported features...
MariaDB Version 10.9.5-MariaDB-debug
 - SSL connections supported
 - binaries are debug compiled
 - binaries built with wsrep patch
Collecting tests...
Installing system database...

==============================================================================

TEST                                      RESULT   TIME (ms) or COMMENT
--------------------------------------------------------------------------

worker[1]  - 'localhost:16000' was not free
worker[1] Using MTR_BUILD_THREAD 301, with reserved ports 16020..16039
include/master-slave.inc
[connection master]
#
# MDEV-21322: report slave progress to the master
#
# ***** TEST A: repl_semisync_wait_point is default (AFTER_COMMIT) and check what happens *****
SET @start_global_value = @@global.rpl_semi_sync_master_wait_point;
# ----- TEST 1: Check if valid wait point is set
set global rpl_semi_sync_master_wait_point= "AFTER_COMMIT";
select @@rpl_semi_sync_master_wait_point;
@@rpl_semi_sync_master_wait_point
AFTER_COMMIT
# ----- TEST 2: No semi-sync and GTID on master
connection master;
SHOW REPLICA HOSTS;
Server_id       Host    Port    Master_id
2       127.0.0.1       16021   1
# ----- TEST 3: Yes semi-sync and no GTID on master
set global rpl_semi_sync_master_enabled = 1;
show variables like 'rpl_semi_sync_master_enabled';
Variable_name   Value
rpl_semi_sync_master_enabled    ON
show status like 'Rpl_semi_sync_master_status';
Variable_name   Value
Rpl_semi_sync_master_status     ON
SHOW REPLICA HOSTS;
Server_id       Host    Port    Master_id
2       127.0.0.1       16021   1
reset master;
SHOW REPLICA HOSTS;
Server_id       Host    Port    Master_id
2       127.0.0.1       16021   1
# ----- TEST 4: No semi-sync on replica - empty result
connection slave;
SHOW REPLICA HOSTS;
Server_id       Host    Port    Master_id
# ----- TEST 5: Enable semi-sync on replica - empty result
set global rpl_semi_sync_slave_enabled = 1;
show variables like 'rpl_semi_sync_slave_enabled';
Variable_name   Value
rpl_semi_sync_slave_enabled     ON
SHOW REPLICA HOSTS;
Server_id       Host    Port    Master_id
connection master;
show variables like 'rpl_semi_sync_master_enabled';
Variable_name   Value
rpl_semi_sync_master_enabled    ON
**** ERROR: failed while waiting for '' 'Rpl_semi_sync_master_clients' = '1' ****
Note: the following output may have changed since the failure was detected
**** Showing STATUS, PROCESSLIST ****
SHOW  STATUS LIKE 'Rpl_semi_sync_master_clients';
Variable_name   Value
Rpl_semi_sync_master_clients    0
SHOW PROCESSLIST;
Id      User    Host    db      Command Time    State   Info    Progress
5       root    localhost       test    Sleep   60              NULL    0.000
6       root    localhost:34040 test    Sleep   60              NULL    0.000
7       root    localhost:34050 test    Sleep   61              NULL    0.000
8       root    localhost:34066 NULL    Binlog Dump     61      Master has sent all binlog to slave; waiting for more updates   NULL    0.000
9       root    localhost:34078 test    Query   0       starting        SHOW PROCESSLIST        0.000
10      root    localhost:34090 test    Sleep   60              NULL    0.000
rpl.rpl_semi_sync_slave_report 'mix'     [ fail ]
        Test ended at 2022-12-12 11:09:46

CURRENT_TEST: rpl.rpl_semi_sync_slave_report
mysqltest: In included file "./include/wait_for_status_var.inc":
included from /home/anel/GitHub/mariadb/server/src/10.9/mysql-test/suite/rpl/include/rpl_semi_sync_report.inc at line 33:
included from /home/anel/GitHub/mariadb/server/src/10.9/mysql-test/suite/rpl/t/rpl_semi_sync_slave_report.test at line 15:
At line 88: Explicit --die command executed

 - saving '/home/anel/GitHub/mariadb/server/build/10.9/mysql-test/var/log/rpl.rpl_semi_sync_slave_report-mix/' to '/home/anel/GitHub/mariadb/server/build/10.9/mysql-test/var/log/rpl.rpl_semi_sync_slave_report-mix/'
--------------------------------------------------------------------------
The servers were restarted 0 times
Spent 0.000 of 65 seconds executing testcases

Failure: Failed 1/1 tests, 0.00% were successful.

Failing test(s): rpl.rpl_semi_sync_slave_report

The log files in var/log may give you some hint of what went wrong.

If you want to report this error, please read first the documentation
at http://dev.mysql.com/doc/mysql/en/mysql-test-suite.html

mysql-test-run: *** ERROR: there were failing test cases
```

