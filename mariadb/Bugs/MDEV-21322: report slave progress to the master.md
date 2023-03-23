
See this
https://mariadb.com/resources/blog/build-your-own-command-line-replica-with-gtid-aware-mariadb-binlog-part-1/

# How replicaiton works
Replication flow:
1. Replica sends request for replication with current GTID - > primary
2. Primary sends back data stream (GTID: domainid-server_id-sequence_no) -> replica IO_thread
3. IO_thread filters desired events ->  relay log 
   - Here binlog_dump command will be executed - dump thread created - request to start replication (see below)
   - Here Master info will be created (see below)

4. Relay log-> SQL_thread that executed changes to storage engine.


# How semi-sync works
With fully semisync there is additional
Before 3. or 5. (I'm not sure where) step
- send ACK that event is executed (that must be 5. step).
based on https://mariadb.com/kb/en/semisynchronous-replication/

- During IO_thread we check if semi_sync is enabled and if ACK on event is neede;
than `slave_reply()` is called see (`slave.cc`)

- There is `Repl_semi_sync_master::dump_start` (`semisync_master.cc) to start binlog_dump to slave (this happens from `mysql_binlog_send` (sql_repl.cc) on master).
- At the end of binlog dump thread (slave) function `report_reply_binlog` is called (when it receives slaves information).
- This function is also called during `report_reply_packet` (`semisync_master.cc`) when master_ack++.
- `report_reply_packet` and `report_reply_packet` is called during `ack` thread (on replica) (`semisync_master_ack_receiver.cc`).
  where ack thread is listening for active sockets and for each slave is calling this function and report back to master.
  

# Flow of execution IO_thread
Flow of execution `IO_thread`
(slave IO thread entry point)
`handle_slave_io`(`slave.cc`)->
  `request_dump` (`slave.cc`) ->
    `request_transmit(mi)`(`semisync_slave.cc`) (see below)
       (after) command `COM_BINLOG_DUMP` (`sql_parse.cc`):
       creates request(file/pos/slave_id and sends to master `mysql_binlog_dump`).
       Binlog dump thread is considered as a thread that returns non-null slave_info structure (`repl_safe.cc`) `is_binlog_dump_thread` function.
  
## request_transmit (slave)
- In `semisync_slave.cc: request_transmit(Master_info *mi)`
  semisync thread is setting user variable `rpl_semi_sync_slave` in  (here `mi->mysql` is used to execeute client on master)
to tell master dump thread that we want to do semi-sync replication.

## COM_BINLOG_DUMP (slave)
- It sets
 1. binlog file
 2. binlog flag
 3. binlog pos
 4. `thd->variables.server_id` to `slave_server_id` obtained from packet.
 5. calls mysql_binlog_send with above parameters - this is executed on master (so it sends last data that it knows).

`is_binlog_dump_thread` non-null slave_info - this function used in `mysqld.cc` to shutingdown the slaves.

## mysql_binlog_send (master)
- Master dump thread called in `mysql_binlog_send` in `sql_repl.cc` where it sets variable `thd->semi_sync_slave` by calling the 
function `is_semi_sync_slave()` that checks user variable `rpl_semi_sync_slave` value on master.
`mysql_binlog_send`->
  `send_one_binlog_file`->
    `send_events`->
      `send_event_to_slave` (at the end we are populating `gtid_state_sent`)

## About masterinfo

- Check `rpl_mi.h` class `Master_info`
- Description
 Replication IO Thread

  Master_info contains:
    - information about how to connect to a master
    - current master log name
    - current master log offset
    - misc control variables

  Master_info is initialized once from the master.info file if such
  exists. Otherwise, data members corresponding to master.info fields
  are initialized with defaults specified by master-* options. The
  initialization is done through init_master_info() call.

  The format of master.info file:

  log_name
  log_pos
  master_host
  master_user
  master_pass
  master_port
  master_connect_retry

  To write out the contents of master.info file to disk ( needed every
  time we read and queue data from the master ), a call to
  flush_master_info() is required.

  To clean up, call end_master_info()

- It has `semi_ack` variable:
```text
  /*
    semi_ack is used to identify if the current binlog event needs an
    ACK from slave, or if delay_master is enabled.
  */
  int semi_ack;
```
This variable is used during `slave_read_sync_header` in IO_thread (see `SEMI_SYNC_NEED_ACK` constant)

## Flow of execution
See semisync_how_works.md

Master thread:               Slave 1,2,..N (dump) thread        Ack receiver thread              
-------------                  -----------------------      ---------------------
create table 
write to binlog 
                    *binlog
                     thread
                                    get binlog info
                                sends status (packet) to ->              
                                                           <-   report_reply_binlog
report_reply_binlog
                                                                  sends ACK
recieves ACK
get ACK
BINLOG_GTID_POS
                        
                        
# Description of PR
+ We are trying to extend the command `SHOW REPLICA HOSTS` that is
executed on master, with columns `GTID_state_sent` and `GTID_state_ack`.
In order to achieve that we have to extend `thd->slave_info` struct with
2 new entries of type `Trans_binlog_info` that contain name of a file and position of file (GTID). 
This struct is replica structure whcih needs to be populated and
must be accessable to primary.

+ The first column `GTID_state_sent`:
  - It is populated by the last event that primary has sent to replica
    (only for semi-sync slave connection, but without need to know
    that replica actually obtained request,
    like it is case in asynchronous replication).
  - Primary executes `mysql_binlog` that first starts the `binlog_dump` thread.
    That thread starts `ack_receiver` thread, that returns second column
    of interest (in first iteration we don't care about).
    After `binlog_dump` thread creating, file is sent with
    `send_one_binlog_file()` function.
    This function is sending event with `send_events()` function,
    during which `send_event_to_slave()` function is executed.
    On that place we are creating the `thd->slave_info->gtid_state_sent` struct.

+ The second column `GTID_state_ack`:
  - It is populated by the `reply_packet_binlog` (a.k.a. `ack`) that is called,
    only for semi-sync replication. It is called on 2 places:
    a) during `binlog_dump` creation, after thread is added to
    `ack_reciver` and after thread is added as semi-sync slave. This
    should be first ack received from replica to primary.
    b) constantly in running phase of `ack_receiver` thread `run()`.
  - A the end of function `reply_packet_binlog` we are creating the
  struct `GTID_state_ack`
  
  
  
# Race condition in MDEV
* This is not race condition, but randomness of events

- Sometimes empty/simetimes give value

1. gives result
 #              but since we are iterating through slave_info, this slave is not found,why?In previous test slave_info is found.
 SHOW REPLICA HOSTS;
 Server_id	Host	Port	Master_id	Gtid_State_Sent	Gtid_State_Ack
+2	localhost	SLAVE_PORT	1	0-1-5	0-1-4
 connection slave;
 SET @@GLOBAL.debug_dbug= "";
 # cleanup
 # -------------------------------------------
 connection master;

2. doesn't give result
--- /home/anel/GitHub/mariadb/server/src/10.11/mysql-test/suite/rpl/r/rpl_show_slave_hosts.result	2023-03-14 15:42:26.155423792 +0100
+++ /home/anel/GitHub/mariadb/server/src/10.11/mysql-test/suite/rpl/r/rpl_show_slave_hosts.reject	2023-03-14 15:47:45.790195438 +0100
@@ -155,12 +155,19 @@
 # -------------------------------------------
 connection master;
 drop table t;
+drop table t2;
 connection slave;

## Problem
For test 5:
Had to manually stop io/sql threads instead of 
```
# End of tests
--source include/rpl_end.inc
```
Works, but test 6 is hanging.

