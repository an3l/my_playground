

===========
Prerequisits for system variables:

Master                          Slave                       Output
------------                  ----------------             ----------------
semi_sync enabled              semi_sync enabled             Patch output
x                                   x                         default

===========

Problem 1: how to get the slave semi_sync enabled status? 
It must be locked in order to use it or update packet for THD::register_slave() - not sure how packet is populated?
In that sense we could store information in Slave_info since is locked with LOCK_thd_data

===========
Problem 2: getting information about GTID, log_file, log_pos

Flow of execution: 
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
                                                        
   
