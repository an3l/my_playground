### MDEV-15530: Variable replicate_rewrite_db 
Cosmetic commit
#git checkout HEAD^ -- mysql-test/suite/rpl/t/rpl_rewrt_db-slave.opt
#git checkout HEAD^ -- mysql-test/suite/binlog/t/binlog_row_mysqlbinlog_options.test

Failed tests:

rpl.rpl_lcase_tblnames_rewrite_db

+
rpl.rpl_set_null_myisam
```
rpl.rpl_set_null_myisam 'stmt'           w1 [ skipped ]  Neither MIXED nor ROW binlog format
***Warnings generated in error logs during shutdown after running tests: rpl.rpl_lcase_tblnames_rewrite_db

Error: Freeing overrun buffer 0x55d2991553e0 at mysys/safemalloc.c:200, mysys/my_malloc.c:212, sql/rpl_filter.cc:749, sql/rpl_filter.cc:39, sql/keycaches.cc:230, sql/keycaches.cc:99, sql/keycaches.cc:236, sql/slave.cc:1335
Error: Freeing overrun buffer 0x55d29991e170 at mysys/safemalloc.c:200, mysys/my_malloc.c:212, sql/rpl_filter.cc:749, sql/rpl_filter.cc:39, sql/mysqld.cc:2020, sql/mysqld.cc:5945, sql/main.cc:34, ??:0
Error: Safemalloc overrun buffer 0x55d29991e170 at mysys/safemalloc.c:370, mysys/safemalloc.c:395, mysys/safemalloc.c:418, ??:0, ??:0, sql/mysqld.cc:1946, sql/mysqld.cc:5958, sql/main.cc:34
Error: Safemalloc overrun buffer 0x55d2991553e0 at mysys/safemalloc.c:370, mysys/safemalloc.c:395, mysys/safemalloc.c:418, ??:0, ??:0, sql/mysqld.cc:1946, sql/mysqld.cc:5958, sql/main.cc:34
Warning:   32 bytes lost at 0x55d29991e170, allocated by T@0 at sql/rpl_filter.cc:566, sql/rpl_filter.cc:604, sql/rpl_filter.cc:313, sql/rpl_filter.cc:629, sql/rpl_mi.cc:977, sql/mysqld.cc:5856, sql/main.cc:34, ??:0
Warning:   32 bytes lost at 0x55d2991553e0, allocated by T@0 at sql/rpl_filter.cc:566, sql/rpl_filter.cc:604, sql/mysqld.cc:8072, mysys/my_getopt.c:655, sql/mysqld.cc:8453, sql/mysqld.cc:4024, sql/mysqld.cc:5685, sql/main.cc:34
```

+ 
rpl.rpl_extra_col_master_myisam
```
rpl.rpl_extra_col_master_myisam 'row'    w3 [ pass ]   1700
***Warnings generated in error logs during shutdown after running tests: rpl.rpl_lcase_tblnames_rewrite_db

Error: Freeing overrun buffer 0x55bcb45ae3e0 at mysys/safemalloc.c:200, mysys/my_malloc.c:212, sql/rpl_filter.cc:749, sql/rpl_filter.cc:39, sql/keycaches.cc:230, sql/keycaches.cc:99, sql/keycaches.cc:236, sql/slave.cc:1335
Error: Freeing overrun buffer 0x55bcb4d2c310 at mysys/safemalloc.c:200, mysys/my_malloc.c:212, sql/rpl_filter.cc:749, sql/rpl_filter.cc:39, sql/mysqld.cc:2020, sql/mysqld.cc:5945, sql/main.cc:34, ??:0
Error: Safemalloc overrun buffer 0x55bcb4d2c310 at mysys/safemalloc.c:370, mysys/safemalloc.c:395, mysys/safemalloc.c:418, ??:0, ??:0, sql/mysqld.cc:1946, sql/mysqld.cc:5958, sql/main.cc:34
Error: Safemalloc overrun buffer 0x55bcb45ae3e0 at mysys/safemalloc.c:370, mysys/safemalloc.c:395, mysys/safemalloc.c:418, ??:0, ??:0, sql/mysqld.cc:1946, sql/mysqld.cc:5958, sql/main.cc:34
Warning:   32 bytes lost at 0x55bcb4d2c310, allocated by T@0 at sql/rpl_filter.cc:566, sql/rpl_filter.cc:604, sql/rpl_filter.cc:313, sql/rpl_filter.cc:629, sql/rpl_mi.cc:977, sql/mysqld.cc:5856, sql/main.cc:34, ??:0
Warning:   32 bytes lost at 0x55bcb45ae3e0, allocated by T@0 at sql/rpl_filter.cc:566, sql/rpl_filter.cc:604, sql/mysqld.cc:8072, mysys/my_getopt.c:655, sql/mysqld.cc:8453, sql/mysqld.cc:4024, sql/mysqld.cc:5685, sql/main.cc:34
```

+
rpl.rpl_relayspace
```
rpl.rpl_relayspace 'mix'                 w8 [ pass ]   1253
***Warnings generated in error logs during shutdown after running tests: rpl.rpl_lcase_tblnames_rewrite_db

Error: Freeing overrun buffer 0x55f6abc7f3e0 at mysys/safemalloc.c:200, mysys/my_malloc.c:212, sql/rpl_filter.cc:749, sql/rpl_filter.cc:39, sql/keycaches.cc:230, sql/keycaches.cc:99, sql/keycaches.cc:236, sql/slave.cc:1335
Error: Freeing overrun buffer 0x55f6ac4a44f0 at mysys/safemalloc.c:200, mysys/my_malloc.c:212, sql/rpl_filter.cc:749, sql/rpl_filter.cc:39, sql/mysqld.cc:2020, sql/mysqld.cc:5945, sql/main.cc:34, ??:0
Error: Safemalloc overrun buffer 0x55f6ac4a44f0 at mysys/safemalloc.c:370, mysys/safemalloc.c:395, mysys/safemalloc.c:418, ??:0, ??:0, sql/mysqld.cc:1946, sql/mysqld.cc:5958, sql/main.cc:34
Error: Safemalloc overrun buffer 0x55f6abc7f3e0 at mysys/safemalloc.c:370, mysys/safemalloc.c:395, mysys/safemalloc.c:418, ??:0, ??:0, sql/mysqld.cc:1946, sql/mysqld.cc:5958, sql/main.cc:34
Warning:   32 bytes lost at 0x55f6ac4a44f0, allocated by T@0 at sql/rpl_filter.cc:566, sql/rpl_filter.cc:604, sql/rpl_filter.cc:313, sql/rpl_filter.cc:629, sql/rpl_mi.cc:977, sql/mysqld.cc:5856, sql/main.cc:34, ??:0
Warning:   32 bytes lost at 0x55f6abc7f3e0, allocated by T@0 at sql/rpl_filter.cc:566, sql/rpl_filter.cc:604, sql/mysqld.cc:8072, mysys/my_getopt.c:655, sql/mysqld.cc:8453, sql/mysqld.cc:4024, sql/mysqld.cc:5685, sql/main.cc:34

```
