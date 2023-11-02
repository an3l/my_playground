# MDEV-32484 Handlersocket Memory Leak in 10.11

See [MariaDB page](https://mariadb.com/kb/en/compile-and-using-mariadb-with-sanitizers-asan-ubsan-tsan-msan/#how-to-compile-mariadb-with-sanitizers)
- Enable ASAN
1. compile WITH_ASAN
2. compile handlersocket as static  -DPLUGIN_HANDLERSOCKET=STATIC
3. export ASAN_OPTIONS=abort_on_error=1:log_path=/tmp/asan:fast_unwind_on_malloc=0 mtr handlersocket


export ASAN_OPTIONS=fast_unwind_on_malloc=0
export CFLAGS="-fsanitize=address"
export CXXFLAGS="-fsanitize=address"
cmake -DWITH_SAFEMALLOC=OFF -DWITH_ASAN=ON
make
The ASAN_OPTIONS may be needed at runtime, not required at compilation time (but should not matter either). WITH_ASAN=ON should automatically add -fsanitize=address to the compilation and possibly linker flags. The initial value of CMAKE_C_FLAGS and CMAKE_CXX_FLAGS is copied from those 2 environment variables.

Any executable that is built with AddressSanitizer should link with some ASAN library (you can check it with ldd) or should produce additional output when you execute it as

ASAN_OPTIONS=help=1 name_of_executable

1. It doesn'f failed in MTR
- handlersocket.opt
```
--plugin-maturity=beta
--loose_handlersocket_port = 9998
--loose_handlersocket_port_wr = 9999
--loose_handlersocket_threads = 16
--loose_handlersocket_threads_wr = 1
--open_files_limit = 65535
```
- handleroscket.test
```
--echo #
--echo # MDEV-32484: Handlersocket Memory Leak in 10.11
--echo # 
CREATE DATABASE testdb;
CREATE TABLE testdb.table1 (k int key, v char(20));
INSERT INTO testdb.table1 values (234,'foo'),(678,'bar');

DROP DATABASE testdb;
```
- Execution at runtime
```
$ ASAN_OPTIONS="abort_on_error=1:fast_unwind_on_malloc=0" ./mysql-test/mtr handlersocket
worker[01] mysql-test-run: WARNING: Process [mysqld.1 - pid: 100225, winpid: 100225] died after mysql-test-run waited 0.3 seconds for /home/anel/GitHub/mariadb/server/build/10.4/mysql-test/var/run/mysqld.1.pid to be created.
main.handlersocket                       [ fail ]
        Test ended at 2023-10-19 10:17:51

CURRENT_TEST: main.handlersocket


Failed to start mysqld.1
mysqltest failed but provided no outpu
```
- By changing the `handlersocket.opt` no errors (only `plugin-maturity`)

2. Manually
- Check `ulimit`
```
$ ulimit -c
unlimited
# This will generate an error when starting mysqld
2023-10-19 11:10:29 0 [Warning] setrlimit could not change the size of core files to 'infinity';  We may not be able to generate a core file on signals

# Based on this https://stackoverflow.com/questions/2762879/linux-core-dumps-are-too-large change it
#  cat /etc/security/limits.conf 
$ ulimit -c 5000000
```
- `.my104.cnf`
```
$ cat ~/.my104-hs.cnf
[mariadb]
datadir=/tmp/10.4
lc_messages_dir=/home/anel/GitHub/mariadb/server/build/10.4/sql/share
# Plugin is compiled statically
plugin_maturity=beta
loose_handlersocket_port = 9998
loose_handlersocket_port_wr = 9999
loose_handlersocket_threads = 16
loose_handlersocket_threads_wr = 1
open_files_limit = 65535
plugin_dir="/home/anel/GitHub/mariadb/server/build/10.4/plugin/handler_socket"
core_file
log_error
```
Check options with `my_print_defaults`
```
$ ./extra/my_print_defaults --mysqld --defaults-file=~/.my104-hs.cnf
--datadir=/tmp/10.4
--lc_messages_dir=/home/anel/GitHub/mariadb/server/build/10.4/sql/share
--plugin_maturity=beta
--loose_handlersocket_port=9998
--loose_handlersocket_port_wr=9999
--loose_handlersocket_threads=16
--loose_handlersocket_threads_wr=1
--open_files_limit=65535

$ ./extra/my_print_defaults --mysqld
--port=3305
--socket=/run/mysqld/mysqld.sock
--pid-file=/run/mysqld/mysqld.pid
--basedir=/usr
--bind-address=127.0.0.1
--expire_logs_days=10
--character-set-server=utf8mb4
--collation-server=utf8mb4_general_ci
```
- Compile statically and with asan
```
$ cmake -LAH . |grep -E "HANDLERSOCKET|WITH_ASAN"
// How to build plugin HANDLERSOCKET. Options are: NO STATIC DYNAMIC YES AUTO.
PLUGIN_HANDLERSOCKET:STRING=STATIC
WITH_ASAN:BOOL=ON
WITH_ASAN_SCOPE:BOOL=OFF
WSREP_LIB_WITH_ASAN:BOOL=OFF
```
- Seems static linking is not working (no symbol found)
```
# NOt produced handlersocket.a
$ nm -C plugin/handler_socket/handlersocket.so  # list of symbols like daemon_handlersocket_status_variables or daemon_handlersocket_init
$ nm sql/mariadbd |grep daemon_handlersocket_init 
```

- Make sure binary is compiled with `WITH_ASAN` and check library 
```
$ ldd ./sql/mariadbd|grep asan
	libasan.so.5 => /lib/x86_64-linux-gnu/libasan.so.5 (0x00007fbf6472d000)
# or
# $ ASAN_OPTIONS=help=1 ./sql/mariadbd|less

```
- Install system tables and start the server
```
$ rm -rf /tmp/10.4 && ./scripts/mariadb-install-db --srcdir=../../src/10.4 --defaults-file=~/.my104-hs.cnf
Installing MariaDB/MySQL system tables in '/tmp/10.4' ...
OK
```
  - When installing without `loose_`
```
# this fails
$ rm -rf /tmp/10.4 && ./scripts/mariadb-install-db --srcdir=../../src/10.4 --defaults-file=~/.my104-hs.cnf
$ cat /tmp/10.4/anel.err 
2023-10-19 12:12:17 0 [ERROR] ./sql/mysqld: unknown variable 'handlersocket_port=9998'
2023-10-19 12:12:17 0 [ERROR] Aborting
```
- Start the server
```
$ ASAN_OPTIONS="abort_on_error=1:fast_unwind_on_malloc=0" ./sql/mariadbd --defaults-file=~/.my104-hs.cnf
2023-10-19 10:24:56 0 [Note] Starting MariaDB 10.4.32-MariaDB-debug source revision 699cfee595b917ab05a99426bc6e9adbaa342e71 as process 102040
2023-10-19 10:24:56 0 [Note] InnoDB: !!!!!!!! UNIV_DEBUG switched on !!!!!!!!!
2023-10-19 10:24:56 0 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
2023-10-19 10:24:56 0 [Note] InnoDB: Uses event mutexes
2023-10-19 10:24:56 0 [Note] InnoDB: Compressed tables use zlib 1.2.11
2023-10-19 10:24:56 0 [Note] InnoDB: Number of pools: 1
2023-10-19 10:24:56 0 [Note] InnoDB: Using SSE2 crc32 instructions
2023-10-19 10:24:56 0 [Note] InnoDB: Initializing buffer pool, total size = 128M, instances = 1, chunk size = 128M
2023-10-19 10:24:56 0 [Note] InnoDB: Completed initialization of buffer pool
2023-10-19 10:24:56 0 [Note] InnoDB: If the mysqld execution user is authorized, page cleaner thread priority can be changed. See the man page of setpriority().
2023-10-19 10:24:57 0 [Note] InnoDB: 128 out of 128 rollback segments are active.
2023-10-19 10:24:57 0 [Note] InnoDB: Creating shared tablespace for temporary tables
2023-10-19 10:24:57 0 [Note] InnoDB: Setting file './ibtmp1' size to 12 MB. Physically writing the file full; Please wait ...
2023-10-19 10:24:57 0 [Note] InnoDB: File './ibtmp1' size is now 12 MB.
2023-10-19 10:24:57 0 [Note] InnoDB: Waiting for purge to start
2023-10-19 10:24:57 0 [Note] InnoDB: 10.4.32 started; log sequence number 61544; transaction id 20
2023-10-19 10:24:57 0 [Note] InnoDB: Loading buffer pool(s) from /tmp/10.4/ib_buffer_pool
2023-10-19 10:24:57 0 [Note] Plugin 'FEEDBACK' is disabled.
2023-10-19 10:24:57 0 [Note] InnoDB: Buffer pool(s) load completed at 231019 10:24:57
2023-10-19 10:24:57 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_port=9998'
2023-10-19 10:24:57 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_port_wr=9999'
2023-10-19 10:24:57 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_threads=16'
2023-10-19 10:24:57 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_threads_wr=1'
2023-10-19 10:24:57 0 [Note] Server socket created on IP: '::'.
2023-10-19 10:24:57 0 [Note] Reading of all Master_info entries succeeded
2023-10-19 10:24:57 0 [Note] Added new Master_info '' to hash table
2023-10-19 10:24:57 0 [Note] ./sql/mariadbd: ready for connections.
Version: '10.4.32-MariaDB-debug'  socket: '/tmp/mysql.sock'  port: 3306  Source distribution

```

- Client
```
$ ./client/mysql -S /tmp/mysql.sock

MariaDB [(none)]> select @@plugin_dir; # plugin_dir is read-only
+--------------------------------------------------------------------+
| @@plugin_dir                                                       |
+--------------------------------------------------------------------+
| /home/anel/GitHub/mariadb/server/build/10.4/plugin/handler_socket/ |
+--------------------------------------------------------------------+
1 row in set (0.003 sec)

MariaDB [(none)]> install plugin handlersocket soname 'handlersocket.so';
Query OK, 0 rows affected (0.031 sec)

MariaDB [(none)]> select * from mysql.plugin;
+---------------+------------------+
| name          | dl               |
+---------------+------------------+
| handlersocket | handlersocket.so |
+---------------+------------------+
1 row in set (0.006 sec)


MariaDB [(none)]> CREATE DATABASE testdb;
MariaDB [(none)]> CREATE TABLE testdb.table1 (k int key, v char(20));
MariaDB [(none)]> INSERT INTO testdb.table1 values (234,'foo'),(678,'bar');
MariaDB [test]> SHOW GLOBAL VARIABLES LIKE 'core_file';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| core_file     | ON    |
+---------------+-------+
1 row in set (0.003 sec)

```

- Confirmed in`Debug` build it works
- Confirmed in `Release` build it works
```
2023-10-19 11:54:51 0 [Warning] setrlimit could not change the size of core files to 'infinity';  We may not be able to generate a core file on signals
2023-10-19 11:54:51 0 [Note] Starting MariaDB 10.4.32-MariaDB source revision 699cfee595b917ab05a99426bc6e9adbaa342e71 as process 151741
2023-10-19 11:54:51 0 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
2023-10-19 11:54:51 0 [Note] InnoDB: Uses event mutexes
2023-10-19 11:54:51 0 [Note] InnoDB: Compressed tables use zlib 1.2.11
2023-10-19 11:54:51 0 [Note] InnoDB: Number of pools: 1
2023-10-19 11:54:51 0 [Note] InnoDB: Using SSE2 crc32 instructions
2023-10-19 11:54:51 0 [Note] InnoDB: Initializing buffer pool, total size = 128M, instances = 1, chunk size = 128M
2023-10-19 11:54:52 0 [Note] InnoDB: Completed initialization of buffer pool
2023-10-19 11:54:52 0 [Note] InnoDB: If the mysqld execution user is authorized, page cleaner thread priority can be changed. See the man page of setpriority().
2023-10-19 11:54:52 0 [Note] InnoDB: 128 out of 128 rollback segments are active.
2023-10-19 11:54:52 0 [Note] InnoDB: Creating shared tablespace for temporary tables
2023-10-19 11:54:52 0 [Note] InnoDB: Setting file './ibtmp1' size to 12 MB. Physically writing the file full; Please wait ...
2023-10-19 11:54:52 0 [Note] InnoDB: File './ibtmp1' size is now 12 MB.
2023-10-19 11:54:52 0 [Note] InnoDB: 10.4.32 started; log sequence number 77108; transaction id 74
2023-10-19 11:54:52 0 [Note] InnoDB: Loading buffer pool(s) from /tmp/10.4/ib_buffer_pool
2023-10-19 11:54:52 0 [Note] Plugin 'FEEDBACK' is disabled.
2023-10-19 11:54:52 0 [Note] InnoDB: Buffer pool(s) load completed at 231019 11:54:52
2023-10-19 11:54:52 0 [ERROR] mariadbd: Can't open shared library '/home/anel/GitHub/mariadb/server/build/10.4/plugin/handler_socket/handlersocket.so' (errno: 0, undefined symbol: _db_my_assert)
2023-10-19 11:54:52 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_port=9998'
2023-10-19 11:54:52 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_port_wr=9999'
2023-10-19 11:54:52 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_threads=16'
2023-10-19 11:54:52 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_threads_wr=1'
2023-10-19 11:54:52 0 [Note] Server socket created on IP: '::'.
2023-10-19 11:54:52 0 [Note] Reading of all Master_info entries succeeded
2023-10-19 11:54:52 0 [Note] Added new Master_info '' to hash table
2023-10-19 11:54:52 0 [Note] ./sql/mariadbd: ready for connections.ls 
Version: '10.4.32-MariaDB'  socket: '/tmp/mysql.sock'  port: 3306  Source distribution
^\2023-10-19 11:49:15 0 [Note] ./sql/mariadbd (initiated by: unknown): Normal shutdown
2023-10-19 11:49:15 0 [Note] Event Scheduler: Purging the queue. 0 events
2023-10-19 11:49:15 0 [Note] InnoDB: FTS optimize thread exiting.
2023-10-19 11:49:15 0 [Note] InnoDB: Starting shutdown...
2023-10-19 11:49:15 0 [Note] InnoDB: Dumping buffer pool(s) to /tmp/10.4/ib_buffer_pool
2023-10-19 11:49:15 0 [Note] InnoDB: Buffer pool(s) dump completed at 231019 11:49:15
2023-10-19 11:49:16 0 [Note] InnoDB: Removed temporary tablespace data file: "ibtmp1"
2023-10-19 11:49:16 0 [Note] InnoDB: Shutdown completed; log sequence number 77108; transaction id 73
2023-10-19 11:49:16 0 [Note] ./sql/mariadbd: Shutdown complete

```

 
- Build library as dynamic(default)
```
$ cmake . -LAH|grep HANDLER

// How to build plugin HANDLERSOCKET. Options are: NO STATIC DYNAMIC YES AUTO.
PLUGIN_HANDLERSOCKET:STRING=DYNAMIC

```


# 10.11
## Installed plugin
```
kill -3 `pgrep -x mariadb`

MariaDB [(none)]> install plugin handlersocket soname 'handlersocket.so';
Query OK, 0 rows affected (0.046 sec)

MariaDB [(none)]> Aborted

=================================================================
==13978==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 75 byte(s) in 3 object(s) allocated from:
    #0 0x7f7e6ada7808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f7e6ac83eac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f7e6ac78c61  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1ec61)
    #3 0x7f7e6ac79ba7 in rl_message (/lib/x86_64-linux-gnu/libreadline.so.5+0x1fba7)
    #4 0x7f7e6ac77aeb  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1daeb)
    #5 0x7f7e6ac784f0 in _rl_isearch_dispatch (/lib/x86_64-linux-gnu/libreadline.so.5+0x1e4f0)
    #6 0x7f7e6ac7881a  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1e81a)
    #7 0x7f7e6ac6c455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #8 0x7f7e6ac6c7c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #9 0x7f7e6ac6cdc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #10 0x556b428053d0 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2230
    #11 0x556b428031c3 in main /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:1373
    #12 0x7f7e6a335082 in __libc_start_main ../csu/libc-start.c:308
    #13 0x556b4280134d in _start (/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb+0xef34d)

Direct leak of 23 byte(s) in 1 object(s) allocated from:
    #0 0x7f7e6ada7808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f7e6ac83eac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f7e6ac78c61  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1ec61)
    #3 0x7f7e6ac79ba7 in rl_message (/lib/x86_64-linux-gnu/libreadline.so.5+0x1fba7)
    #4 0x7f7e6ac77aeb  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1daeb)
    #5 0x7f7e6ac787f8  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1e7f8)
    #6 0x7f7e6ac6c455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #7 0x7f7e6ac6c7c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #8 0x7f7e6ac6cdc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #9 0x556b428053d0 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2230
    #10 0x556b428031c3 in main /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:1373
    #11 0x7f7e6a335082 in __libc_start_main ../csu/libc-start.c:308
    #12 0x556b4280134d in _start (/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb+0xef34d)

SUMMARY: AddressSanitizer: 98 byte(s) leaked in 4 allocation(s).
Aborted (core dumped)

```
- Got leak after quiting client library `kill -3 `pgrep -x mariadb``, after the server is quit normally - not the same leak as reported

```
MariaDB [(none)]> Aborted

=================================================================
==90164==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x7f3d0d865808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f3d0d741eac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f3d0d73c902 in rl_add_undo (/lib/x86_64-linux-gnu/libreadline.so.5+0x24902)
    #3 0x7f3d0d73f0ec in rl_insert_text (/lib/x86_64-linux-gnu/libreadline.so.5+0x270ec)
    #4 0x7f3d0d740079 in _rl_insert_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x28079)
    #5 0x7f3d0d72a455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #6 0x7f3d0d72a7c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #7 0x7f3d0d72adc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #8 0x55b6aea9c3d0 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2230
    #9 0x55b6aea9a1c3 in main /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:1373
    #10 0x7f3d0cdf3082 in __libc_start_main ../csu/libc-start.c:308
    #11 0x55b6aea9834d in _start (/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb+0xef34d)

SUMMARY: AddressSanitizer: 32 byte(s) leaked in 1 allocation(s).
Aborted (core dumped)

```

## Uninstalled plugin
```
MariaDB [(none)]> uninstall plugin handlersocket;
ERROR 2013 (HY000): Lost connection to server during query

$ ./sql/mariadbd --defaults-file=~/.my1011-hs.cnf
2023-10-20 13:52:44 0 [Note] Starting MariaDB 10.11.6-MariaDB-debug source revision 22c869f65f143bbd0bb3811b4113fdb0f483eef0 as process 13744
2023-10-20 13:52:44 0 [Note] InnoDB: !!!!!!!! UNIV_DEBUG switched on !!!!!!!!!
2023-10-20 13:52:44 0 [Note] InnoDB: Compressed tables use zlib 1.2.11
2023-10-20 13:52:44 0 [Note] InnoDB: Number of transaction pools: 1
2023-10-20 13:52:44 0 [Note] InnoDB: Using crc32 + pclmulqdq instructions
2023-10-20 13:52:44 0 [Note] InnoDB: Using Linux native AIO
2023-10-20 13:52:44 0 [Note] InnoDB: Initializing buffer pool, total size = 128.000MiB, chunk size = 2.000MiB
2023-10-20 13:52:44 0 [Note] InnoDB: Completed initialization of buffer pool
2023-10-20 13:52:44 0 [Note] InnoDB: File system buffers for log disabled (block size=512 bytes)
2023-10-20 13:52:44 0 [Note] InnoDB: End of log at LSN=55942
2023-10-20 13:52:44 0 [Note] InnoDB: 128 rollback segments are active.
2023-10-20 13:52:44 0 [Note] InnoDB: Setting file './ibtmp1' size to 12.000MiB. Physically writing the file full; Please wait ...
2023-10-20 13:52:44 0 [Note] InnoDB: File './ibtmp1' size is now 12.000MiB.
2023-10-20 13:52:44 0 [Note] InnoDB: log sequence number 55942; transaction id 14
2023-10-20 13:52:44 0 [Note] InnoDB: Loading buffer pool(s) from /tmp/10.11/ib_buffer_pool
2023-10-20 13:52:44 0 [Note] Plugin 'FEEDBACK' is disabled.
2023-10-20 13:52:45 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_port=9998'
2023-10-20 13:52:45 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_port_wr=9999'
2023-10-20 13:52:45 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_threads=16'
2023-10-20 13:52:45 0 [Warning] ./sql/mariadbd: unknown variable 'loose_handlersocket_threads_wr=1'
2023-10-20 13:52:45 0 [Note] InnoDB: Buffer pool(s) load completed at 231020 13:52:45
2023-10-20 13:52:45 0 [Note] Server socket created on IP: '0.0.0.0'.
2023-10-20 13:52:45 0 [Note] Server socket created on IP: '::'.
2023-10-20 13:52:45 0 [Note] ./sql/mariadbd: ready for connections.
Version: '10.11.6-MariaDB-debug'  socket: '/tmp/mysql.sock'  port: 3306  Source distribution
2023-10-20 13:53:29 4 [Warning] Plugin 'handlersocket' is of maturity level beta while the server is stable
handlersocket: initialized
CONFIG: num_threads=16
CONFIG: nonblocking=1(default)
CONFIG: use_epoll=1
CONFIG: readsize=0
CONFIG: conn_per_thread=1024(default)
CONFIG: for_write=0(default)
CONFIG: plain_secret=(default)
CONFIG: timeout=300
CONFIG: listen_backlog=32768
CONFIG: host=(default)
CONFIG: port=9998
CONFIG: sndbuf=0
CONFIG: rcvbuf=0
CONFIG: stack_size=1048576(default)
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
CONFIG: num_threads=1
CONFIG: nonblocking=1(default)
CONFIG: use_epoll=1
CONFIG: readsize=0
CONFIG: conn_per_thread=1024(default)
CONFIG: for_write=1
CONFIG: plain_secret=
CONFIG: timeout=300
CONFIG: listen_backlog=32768
CONFIG: host=(default)
CONFIG: port=9999
CONFIG: sndbuf=0
CONFIG: rcvbuf=0
CONFIG: stack_size=1048576(default)
CONFIG: wrlock_timeout=12
CONFIG: accept_balance=0
handlersocket: terminated
mariadbd: /home/anel/GitHub/mariadb/server/src/10.11/sql/sql_list.h:705: void ilink::assert_not_linked(): Assertion `prev == 0 && next == 0' failed.
231020 13:55:23 [ERROR] mysqld got signal 6 ;
This could be because you hit a bug. It is also possible that this binary
or one of the libraries it was linked against is corrupt, improperly built,
or misconfigured. This error can also be caused by malfunctioning hardware.

To report this bug, see https://mariadb.com/kb/en/reporting-bugs

We will try our best to scrape up some info that will hopefully help
diagnose the problem, but since we have already crashed, 
something is definitely wrong and this may fail.

Server version: 10.11.6-MariaDB-debug source revision: 22c869f65f143bbd0bb3811b4113fdb0f483eef0
key_buffer_size=134217728
read_buffer_size=131072
max_used_connections=1
max_threads=153
thread_count=18
It is possible that mysqld could use up to 
key_buffer_size + (read_buffer_size + sort_buffer_size)*max_threads = 468162 K  bytes of memory
Hope that's ok; if not, decrease some variables in the equation.

Thread pointer: 0x0
Attempting backtrace. You can use the following information to find out
where mysqld died. If you see no messages after this, something went
terribly wrong...
stack_bottom = 0x0 thread_stack 0x100000
sanitizer_common/sanitizer_common_interceptors.inc:4022(__interceptor_backtrace.part.0)[0x7fcda6078d40]
addr2line: './sql/mariadbd': No such file
Printing to addr2line failed
./sql/mariadbd(my_print_stacktrace+0xec)[0x55f017611d89]
./sql/mariadbd(handle_fatal_signal+0xa29)[0x55f0161d5788]
sigaction.c:0(__restore_rt)[0x7fcda5b98420]
addr2line: DWARF error: section .debug_info is larger than its filesize! (0x93ef57 vs 0x530ea0)
/lib/x86_64-linux-gnu/libc.so.6(gsignal+0xcb)[0x7fcda568100b]
/lib/x86_64-linux-gnu/libc.so.6(abort+0x12b)[0x7fcda5660859]
/lib/x86_64-linux-gnu/libc.so.6(+0x22729)[0x7fcda5660729]
/lib/x86_64-linux-gnu/libc.so.6(+0x33fd6)[0x7fcda5671fd6]
addr2line: './sql/mariadbd': No such file
./sql/mariadbd(_ZN5ilink17assert_not_linkedEv+0x140)[0x55f01564df42]
./sql/mariadbd(_ZN3THDD1Ev+0x28c)[0x55f01578f094]
./sql/mariadbd(_ZN3THDD0Ev+0x1c)[0x55f01578fd40]
handlersocket/database.cpp:341(dena::dbcontext::term_thread())[0x7fcd81daec4c]
handlersocket/hstcpsvr_worker.cpp:318(dena::(anonymous namespace)::thr_init::~thr_init())[0x7fcd81ddb5ce]
handlersocket/hstcpsvr_worker.cpp:347(dena::hstcpsvr_worker::run())[0x7fcd81ddba43]
handlersocket/hstcpsvr.cpp:31(dena::worker_throbj::operator()())[0x7fcd81df3b86]
libhsclient/thread.hpp:72(dena::thread<dena::worker_throbj>::thread_main(void*))[0x7fcd81df7073]
nptl/pthread_create.c:478(start_thread)[0x7fcda5b8c609]
addr2line: DWARF error: section .debug_info is larger than its filesize! (0x93ef57 vs 0x530ea0)
/lib/x86_64-linux-gnu/libc.so.6(clone+0x43)[0x7fcda575d133]
The manual page at https://mariadb.com/kb/en/how-to-produce-a-full-stack-trace-for-mysqld/ contains
information that should help you find out what is causing the crash.
Writing a core file...
Working directory at /tmp/10.11
Resource Limits:
Limit                     Soft Limit           Hard Limit           Units     
Max cpu time              unlimited            unlimited            seconds   
Max file size             unlimited            unlimited            bytes     
Max data size             unlimited            unlimited            bytes     
Max stack size            8388608              unlimited            bytes     
Max core file size        0                    0                    bytes     
Max resident set          unlimited            unlimited            bytes     
Max processes             127651               127651               processes 
Max open files            65535                65535                files     
Max locked memory         67108864             67108864             bytes     
Max address space         unlimited            unlimited            bytes     
Max file locks            unlimited            unlimited            locks     
Max pending signals       127651               127651               signals   
Max msgqueue size         819200               819200               bytes     
Max nice priority         0                    0                    
Max realtime priority     0                    0                    
Max realtime timeout      unlimited            unlimited            us        
Core pattern: |/usr/share/apport/apport -p%p -s%s -c%c -d%d -P%P -u%u -g%g -- %E

Kernel version: Linux version 5.15.0-87-generic (buildd@bos03-amd64-016) (gcc (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0, GNU ld (GNU Binutils for Ubuntu) 2.34) #97~20.04.1-Ubuntu SMP Thu Oct 5 08:25:28 UTC 2023

Aborted (core dumped)
```

- Client errors
```
MariaDB [(none)]> uninstall plugin handlersocket;
ERROR 2013 (HY000): Lost connection to server during query
MariaDB [(none)]> select * from mysql.plugin;
ERROR 2006 (HY000): Server has gone away
No connection. Trying to reconnect...
ERROR 2002 (HY000): Can't connect to local server through socket '/tmp/mysql.sock' (111)
ERROR: Can't connect to the server

unknown [(none)]> select * from mysql.plugin;
No connection. Trying to reconnect...
ERROR 2002 (HY000): Can't connect to local server through socket '/tmp/mysql.sock' (111)
ERROR: Can't connect to the server

unknown [(none)]> exit5
    -> Ctrl-C -- exit!
Aborted

=================================================================
==15349==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 128 byte(s) in 1 object(s) allocated from:
    #0 0x7f02d656fa06 in __interceptor_calloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:153
    #1 0x55691435fd2c in mysql_init /home/anel/GitHub/mariadb/server/src/10.11/libmariadb/libmariadb/mariadb_lib.c:1282
    #2 0x556914349be3 in sql_real_connect /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:4856
    #3 0x55691434a1b8 in sql_connect /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:4941
    #4 0x556914347ce1 in com_connect /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:4520
    #5 0x55691434025a in reconnect /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:3100
    #6 0x556914340434 in mysql_real_query_for_lazy(char const*, unsigned long) /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:3148
    #7 0x556914342013 in com_go /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:3421
    #8 0x55691433d5ee in add_line /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2574
    #9 0x55691433b6db in read_and_execute /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2269
    #10 0x5569143391c3 in main /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:1373
    #11 0x7f02d5afd082 in __libc_start_main ../csu/libc-start.c:308
    #12 0x55691433734d in _start (/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb+0xef34d)

Direct leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x7f02d656f808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f02d644beac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f02d6446902 in rl_add_undo (/lib/x86_64-linux-gnu/libreadline.so.5+0x24902)
    #3 0x7f02d64491f0 in rl_delete_text (/lib/x86_64-linux-gnu/libreadline.so.5+0x271f0)
    #4 0x7f02d644a937 in _rl_rubout_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x28937)
    #5 0x7f02d6434455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #6 0x7f02d64347c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #7 0x7f02d6434dc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #8 0x55691433b3d0 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2230
    #9 0x5569143391c3 in main /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:1373
    #10 0x7f02d5afd082 in __libc_start_main ../csu/libc-start.c:308
    #11 0x55691433734d in _start (/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb+0xef34d)

Direct leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x7f02d656fa06 in __interceptor_calloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:153
    #1 0x55691435fcd4 in mysql_init /home/anel/GitHub/mariadb/server/src/10.11/libmariadb/libmariadb/mariadb_lib.c:1280
    #2 0x556914349be3 in sql_real_connect /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:4856
    #3 0x55691434a1b8 in sql_connect /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:4941
    #4 0x556914347ce1 in com_connect /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:4520
    #5 0x55691434025a in reconnect /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:3100
    #6 0x556914340434 in mysql_real_query_for_lazy(char const*, unsigned long) /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:3148
    #7 0x556914342013 in com_go /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:3421
    #8 0x55691433d5ee in add_line /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2574
    #9 0x55691433b6db in read_and_execute /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2269
    #10 0x5569143391c3 in main /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:1373
    #11 0x7f02d5afd082 in __libc_start_main ../csu/libc-start.c:308
    #12 0x55691433734d in _start (/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb+0xef34d)

Indirect leak of 96 byte(s) in 3 object(s) allocated from:
    #0 0x7f02d656f808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f02d644beac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f02d6446902 in rl_add_undo (/lib/x86_64-linux-gnu/libreadline.so.5+0x24902)
    #3 0x7f02d64491f0 in rl_delete_text (/lib/x86_64-linux-gnu/libreadline.so.5+0x271f0)
    #4 0x7f02d644a937 in _rl_rubout_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x28937)
    #5 0x7f02d6434455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #6 0x7f02d64347c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #7 0x7f02d6434dc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #8 0x55691433b3d0 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2230
    #9 0x5569143391c3 in main /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:1373
    #10 0x7f02d5afd082 in __libc_start_main ../csu/libc-start.c:308
    #11 0x55691433734d in _start (/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb+0xef34d)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x7f02d656f808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f02d644beac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f02d6446902 in rl_add_undo (/lib/x86_64-linux-gnu/libreadline.so.5+0x24902)
    #3 0x7f02d64490ec in rl_insert_text (/lib/x86_64-linux-gnu/libreadline.so.5+0x270ec)
    #4 0x7f02d644a079 in _rl_insert_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x28079)
    #5 0x7f02d6434455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #6 0x7f02d64347c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #7 0x7f02d6434dc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #8 0x55691433b3d0 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2230
    #9 0x5569143391c3 in main /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:1373
    #10 0x7f02d5afd082 in __libc_start_main ../csu/libc-start.c:308
    #11 0x55691433734d in _start (/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb+0xef34d)

Indirect leak of 8 byte(s) in 4 object(s) allocated from:
    #0 0x7f02d656f808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f02d644beac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f02d64458c5 in rl_copy_text (/lib/x86_64-linux-gnu/libreadline.so.5+0x238c5)
    #3 0x7f02d6449199 in rl_delete_text (/lib/x86_64-linux-gnu/libreadline.so.5+0x27199)
    #4 0x7f02d644a937 in _rl_rubout_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x28937)
    #5 0x7f02d6434455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #6 0x7f02d64347c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #7 0x7f02d6434dc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #8 0x55691433b3d0 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2230
    #9 0x5569143391c3 in main /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:1373
    #10 0x7f02d5afd082 in __libc_start_main ../csu/libc-start.c:308
    #11 0x55691433734d in _start (/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb+0xef34d)

SUMMARY: AddressSanitizer: 320 byte(s) leaked in 11 allocation(s).
Aborted (core dumped)
```

## Start server with loaded plugin
- Insert queries
```
MariaDB [(none)]> # Added queries
MariaDB [(none)]> DROP DATABASE IF EXISTS testdb; CREATE DATABASE testdb; CREATE TABLE testdb.table1 (k int key, v char(20)); INSERT INTO testdb.table1 values (234,'foo'),(678,'bar');

```
- Quit the server
```
$ kill -3 `pgrep -x mariadbd`
bash: kill: (1269) - Operation not permitted

2023-10-20 14:02:32 0 [Note] ./sql/mariadbd: ready for connections.
Version: '10.11.6-MariaDB-debug'  socket: '/tmp/mysql.sock'  port: 3306  Source distribution
2023-10-20 14:03:44 0 [Note] ./sql/mariadbd (initiated by: unknown): Normal shutdown
mariadbd: /home/anel/GitHub/mariadb/server/src/10.11/sql/sql_list.h:705: void ilink::assert_not_linked(): Assertion `prev == 0 && next == 0' failed.
mariadbd: /home/anel/GitHub/mariadb/server/src/10.11/sql/sql_list.h:705: void ilink::assert_not_linked(): Assertion `prev == 0 && next == 0' failed.
231020 14:03:44 [ERROR] mysqld got signal 6 ;
This could be because you hit a bug. It is also possible that this binary
or one of the libraries it was linked against is corrupt, improperly built,
or misconfigured. This error can also be caused by malfunctioning hardware.

To report this bug, see https://mariadb.com/kb/en/reporting-bugs

We will try our best to scrape up some info that will hopefully help
diagnose the problem, but since we have already crashed, 
something is definitely wrong and this may fail.

Server version: 10.11.6-MariaDB-debug source revision: 22c869f65f143bbd0bb3811b4113fdb0f483eef0
key_buffer_size=134217728
read_buffer_size=131072
max_used_connections=1
max_threads=153
thread_count=17
It is possible that mysqld could use up to 
key_buffer_size + (read_buffer_size + sort_buffer_size)*max_threads = 468162 K  bytes of memory
Hope that's ok; if not, decrease some variables in the equation.

Thread pointer: 0x0
Attempting backtrace. You can use the following information to find out
where mysqld died. If you see no messages after this, something went
terribly wrong...
Aborted (core dumped)

```
- Quit the client
```
MariaDB [(none)]> Aborted

=================================================================
==16516==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 421 byte(s) in 17 object(s) allocated from:
    #0 0x7f61a79af808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f61a788beac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f61a7880c61  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1ec61)
    #3 0x7f61a7881ba7 in rl_message (/lib/x86_64-linux-gnu/libreadline.so.5+0x1fba7)
    #4 0x7f61a787faeb  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1daeb)
    #5 0x7f61a78804f0 in _rl_isearch_dispatch (/lib/x86_64-linux-gnu/libreadline.so.5+0x1e4f0)
    #6 0x7f61a788081a  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1e81a)
    #7 0x7f61a7874455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #8 0x7f61a78747c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #9 0x7f61a7874dc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #10 0x5595d4b7d3d0 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2230
    #11 0x5595d4b7b1c3 in main /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:1373
    #12 0x7f61a6f3d082 in __libc_start_main ../csu/libc-start.c:308
    #13 0x5595d4b7934d in _start (/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb+0xef34d)

Direct leak of 23 byte(s) in 1 object(s) allocated from:
    #0 0x7f61a79af808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f61a788beac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f61a7880c61  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1ec61)
    #3 0x7f61a7881ba7 in rl_message (/lib/x86_64-linux-gnu/libreadline.so.5+0x1fba7)
    #4 0x7f61a787faeb  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1daeb)
    #5 0x7f61a78807f8  (/lib/x86_64-linux-gnu/libreadline.so.5+0x1e7f8)
    #6 0x7f61a7874455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #7 0x7f61a78747c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #8 0x7f61a7874dc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #9 0x5595d4b7d3d0 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:2230
    #10 0x5595d4b7b1c3 in main /home/anel/GitHub/mariadb/server/src/10.11/client/mysql.cc:1373
    #11 0x7f61a6f3d082 in __libc_start_main ../csu/libc-start.c:308
    #12 0x5595d4b7934d in _start (/home/anel/GitHub/mariadb/server/build/10.11/client/mariadb+0xef34d)

SUMMARY: AddressSanitizer: 444 byte(s) leaked in 18 allocation(s).
Aborted (core dumped)
```
