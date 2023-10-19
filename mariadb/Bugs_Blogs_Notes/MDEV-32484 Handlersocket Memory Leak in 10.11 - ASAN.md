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

