Failed tests for MDEV-32004

    binlog_encryption.rpl_parallel
    binlog_encryption.rpl_mixed_binlog_max_cache_size
    binlog_encryption.rpl_mixed_binlog_max_cache_size
    binlog_encryption.rpl_parallel
    binlog_encryption.encrypted_master_switch_to_unencrypted_coords
    binlog_encryption.encrypted_master_switch_to_unencrypted_gtid
    binlog_encryption.rpl_parallel
    binlog_encryption.rpl_parallel_ignored_errors
    binlog_encryption.rpl_parallel
    binlog_encryption.rpl_parallel
    binlog_encryption.rpl_parallel_ignored_errors
    binlog_encryption.encrypted_master_switch_to_unencrypted_coords
    binlog_encryption.rpl_parallel
    binlog_encryption.encrypted_master_switch_to_unencrypted_gtid
    multi_source.gtid_slave_pos
    multi_source.gtid_slave_pos
    rpl.rpl_incompatible_heartbeat rpl.rpl_innodb_mixed_dml rpl.rpl_innodb_mixed_ddl rpl.rpl_mixed_binlog_max_cache_size rpl.rpl_gtid_grouping
    rpl.mdev-31448_kill_ooo_finish_optimistic
    rpl.rpl_mixed_binlog_max_cache_size
    rpl.mdev-31448_kill_ooo_finish_optimistic
    rpl.rpl_domain_id_filter_io_crash
    rpl.rpl_cant_read_event_incident rpl.rpl_connection
    rpl.rpl_domain_id_filter_io_crash
    rpl.rpl_connection
    rpl.rpl_domain_id_filter_restart rpl.rpl_drop_db rpl.rpl_drop rpl.rpl_gtid_errorlog rpl.rpl_grant rpl.rpl_dump_request_retry_warning rpl.rpl_get_lock rpl.rpl_drop_view rpl.rpl_gtid_delete_domain rpl.rpl_function_defaults rpl.rpl_events
    rpl.rpl_gtid_errorlog
    rpl.rpl_domain_id_filter_io_crash
    rpl.rpl_parallel_kill
    rpl.rpl_domain_id_filter_io_crash
    rpl.rpl_foreign_key_innodb rpl.rpl_gtid_errorhandling
    rpl.rpl_parallel_kill
    rpl.rpl_gtid_strict rpl.rpl_mdev382 rpl.rpl_loaddata rpl.rpl_mdev_17614
    rpl.rpl_gtid_errorhandling
    rpl.rpl_mdev_17614
    rpl.rpl_gtid_reconnect rpl.rpl_gtid_startpos rpl.rpl_gtid_sort
    rpl.rpl_gtid_startpos
    rpl_sql_thd_start_errno_cleared
    
    
    
 Failed here even without the patch: rpl_sql_thd_start_errno_cleared
 
 
 --- /home/anel/GitHub/mariadb/server/src/10.4/mysql-test/suite/rpl/r/rpl_sql_thd_start_errno_cleared.result	2023-09-14 11:18:16.330977896 +0200
+++ /home/anel/GitHub/mariadb/server/src/10.4/mysql-test/suite/rpl/r/rpl_sql_thd_start_errno_cleared.reject	2023-09-14 13:12:20.607829159 +0200
@@ -29,6 +29,8 @@
 set @@global.debug_dbug= "+d,delay_sql_thread_after_release_run_lock";
 include/start_slave.inc
 set debug_sync= "now wait_for sql_thread_run_lock_released";
+Warnings:
+Warning	1639	debug sync point wait timed out
 # Validating that the SQL thread is running..


2023-09-14 13:07:20 16 [Warning] Slave: Lock wait timeout exceeded; try restarting transaction Error_code: 1205
clear


Look this for mtr:
multi_source.gtid_slave_pos rpl.rpl_incompatible_heartbeat rpl.rpl_innodb_mixed_dml  rpl.rpl_mixed_binlog_max_cache_size rpl.rpl_gtid_grouping rpl.mdev-31448_kill_ooo_finish_optimistic rpl.rpl_mixed_binlog_max_cache_size rpl.mdev-31448_kill_ooo_finish_optimistic rpl.rpl_cant_read_event_incident rpl.rpl_connection rpl.rpl_connection rpl.rpl_domain_id_filter_restart rpl.rpl_drop_db rpl.rpl_drop rpl.rpl_gtid_errorlog rpl.rpl_grant rpl.rpl_dump_request_retry_warning rpl.rpl_get_lock rpl.rpl_drop_view rpl.rpl_gtid_delete_domain rpl.rpl_function_defaults rpl.rpl_events rpl.rpl_parallel_kill rpl.rpl_domain_id_filter_io_crash rpl.rpl_foreign_key_innodb  rpl.rpl_gtid_strict rpl.rpl_mdev382 rpl.rpl_loaddata rpl.rpl_mdev_17614 rpl.rpl_gtid_errorhandling rpl.rpl_mdev_17614 rpl.rpl_gtid_reconnect rpl.rpl_gtid_startpos rpl.rpl_gtid_sort rpl_sql_thd_start_errno_cleared  binlog_encryption.encrypted_master_switch_to_unencrypted_coords binlog_encryption.encrypted_master_switch_to_unencrypted_gtid binlog_encryption.rpl_parallel_ignored_errors binlog_encryption.rpl_mixed_binlog_max_cache_size  binlog_encryption.rpl_parallel
    
    
    
 With patch
 ```
     rpl.rpl_mixed_binlog_max_cache_size rpl.rpl_incompatible_heartbeat rpl.rpl_gtid_grouping rpl.rpl_innodb_mixed_ddl rpl.rpl_innodb_mixed_dml
    rpl.rpl_domain_id_filter_io_crash
    rpl.rpl_cant_read_event_incident rpl.rpl_connection
    rpl.rpl_gtid_errorhandling
    rpl.semisync_future-7591 rpl.rpl_view_debug rpl.rpl_err_ignoredtable rpl.rpl_lcase_tblnames_rewrite_db rpl.rpl_free_items rpl.rpl_multi_update2 rpl.rpl_multi_delete2 rpl.rpl_view_multi rpl.rpl_server_id2
    rpl.rpl_gtid_startpos
    rpl.mdev-31448_kill_ooo_finish_optimistic
    rpl.rpl_grant rpl.rpl_get_lock rpl.rpl_function_defaults rpl.rpl_gtid_delete_domain rpl.rpl_drop_view rpl.rpl_drop rpl.rpl_domain_id_filter_restart rpl.rpl_dump_request_retry_warning rpl.rpl_drop_db rpl.rpl_events
    rpl.rpl_gtid_errorlog

 ```
 
 Missing
 ```
 rpl.rpl_mdev_17614
 rpl.rpl_gtid_delete_domain
 rpl.rpl_gtid_errorhandling
 rpl.rpl_parallel_kill
 rpl.rpl_gtid_startpos 
 rpl.rpl_gtid_errorlog
 rpl.mdev-31448_kill_ooo_finish_optimistic
 rpl.rpl_domain_id_filter_io_crash
 rpl.rpl_gtid_delete_domain 
 rpl.rpl_connection
 ```
 

 - Missing rpl.semisync_future-7591 rpl.rpl_parallel_retry
 ```
 rpl.rpl_parallel_kill
 rpl.rpl_semi_sync_master_shutdown (P)
 rpl.rpl_slave_status
 rpl.rpl_row_corruption
 rpl.rpl_ssl1
rpl.semisync_future-7591
 rpl.rpl_parallel_retry
 rpl.rpl_row_idempotency
 rpl.rpl_stm_start_stop_slave
 rpl.rpl_stm_stop_middle_group
 rpl.rpl_heartbeat_basic
 rpl.rpl_shutdown_wait_slaves
 ```
 
PROBLEM 1:  rpl.rpl_semi_sync_master_shutdown:
```
$ git diff mysql-test/suite/rpl/include/rpl_shutdown_wait_slaves.inc
diff --git a/mysql-test/suite/rpl/include/rpl_shutdown_wait_slaves.inc b/mysql-test/suite/rpl/include/rpl_shutdown_wait_slaves.inc
index 4726bbe1889..f71426cf9c8 100644
--- a/mysql-test/suite/rpl/include/rpl_shutdown_wait_slaves.inc
+++ b/mysql-test/suite/rpl/include/rpl_shutdown_wait_slaves.inc
@@ -77,15 +77,24 @@ DROP TABLE t1;
 
 --connection server_2
 --disable_warnings
+--let rpl_debug= 1
+--source include/stop_slave.inc
+CHANGE MASTER TO MASTER_USE_GTID=SLAVE_POS;
+--let $slave_io_errno=2003
+--source include/wait_for_slave_io_error.inc
 --source include/start_slave.inc
 --enable_warnings
 
 --connection server_3
 --disable_warnings
+--source include/stop_slave.inc
+CHANGE MASTER TO MASTER_USE_GTID=SLAVE_POS;
 --source include/start_slave.inc
 --enable_warnings
 
 --connection server_4
 --disable_warnings
+--source include/stop_slave.inc
+CHANGE MASTER TO MASTER_USE_GTID=SLAVE_POS;
 --source include/start_slave.inc
 --enable_warnings
```

Possible fix  ^^^ rpl_slave_status.test 
- accessdenied error 1045 (IO thread)
source include/wait_for_slave_sql_to_start.inc; -> 
  --source include/wait_for_slave_io_error.inc (1045) -> reset replication
    --source include/stop_slave_sql.inc ->
      CHANGE MASTER TO MASTER_USER = 'root', MASTER_PASSWORD = ''; -> (clear Slave_IO_error)
        --let $rpl_only_running_threads= 1
        --source include/rpl_reset.inc

```
# cleanup: slave io thread is stopped so we reset replication
--source include/stop_slave_sql.inc
CHANGE MASTER TO MASTER_USER = 'root', MASTER_PASSWORD = '';
# clear Slave_IO_Errno
--let $rpl_only_running_threads= 1
--source include/rpl_reset.inc
```

PROBLEM 2: `rpl.rpl.rpl_semi_sync_shutdown_await_ack`
```
diff --git a/mysql-test/suite/rpl/t/rpl_semi_sync_shutdown_await_ack.inc b/mysql-test/suite/rpl/t/rpl_semi_sync_shutdown_await_ack.inc
index a232f68540d..a9a7f9f6f14 100644
--- a/mysql-test/suite/rpl/t/rpl_semi_sync_shutdown_await_ack.inc
+++ b/mysql-test/suite/rpl/t/rpl_semi_sync_shutdown_await_ack.inc
@@ -116,6 +116,9 @@ show status like 'Rpl_semi_sync_master_no_tx';
 --connection server_2
 --eval SET @@GLOBAL.debug_dbug= "$sav_server_2_dbug"
 --eval SET @@GLOBAL.rpl_semi_sync_slave_enabled= 0
+--let $slave_io_errno=1595
+--source include/wait_for_slave_io_error.inc
+--let $rpl_only_running_threads= 1
 source include/stop_slave.inc;

```


