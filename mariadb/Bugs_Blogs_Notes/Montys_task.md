# Refactor MYSQL_BIN_LOG
Based on 
https://github.com/MariaDB/server/tree/bb-11.4-MDEV-31404


Failure in bb, not reported as failure:
https://buildbot.mariadb.org/#/builders/369/builds/15699/steps/7/logs/stdio

#  MYSQL_BIN_LOG

- It is inherited from `public TC_LOG, private Event_log`
  - Event log is inherited from `MYSQL_LOG`, that has methods like `is_open`
- Public constructor and members.
- ALl methods and members are private
- There is single private constructor with (uint *)
  - Point is that user cannot create objects but creates named constructor idiom https://isocpp.org/wiki/faq/ctors#named-ctor-idiom
    - There are `static` classes that can create/return instances of classes. - didin't understand this
  - Or prevent inheritance https://isocpp.org/wiki/faq/strange-inheritance#final-classes
    - We want to have inheritance
  - Instantiated with singleton (https://www.geeksforgeeks.org/singleton-design-pattern/)
    https://www.geeksforgeeks.org/can-constructor-private-cpp/
    
- `extern MYSQL_PLUGIN_IMPORT MYSQL_BIN_LOG mysql_bin_log;`
- There is singleton `log.cc`
```
MYSQL_BIN_LOG mysql_bin_log(&sync_binlog_period);
# uint sync_binlog_period= 0; assigned in mysqld.cc
```

## BINLOG:

### HOw binary logs are now creted?
COM_BINLOG_DUMP -> mysql_binlog_send -> init_binlog_sender -> open_binlog -> send_one_binlog_file -> mysql_bin_log.find_next_log
                                            ->
### What does !is_relay_log?

cleanup -> stop_background_thread()
        -> rpl_global_gtid_binlog_state.free();

open    -> binlog_state_recover_done (NO) -> do_binlog_recovery  -> start_binlog_background_thread()
        -> check init_and_set_log_file_name() -> fail error.
        -> checksum assign alg to binlog_checksum_options
        -> write_event() [output a Gtid_list_log_event at start]
        -> reset_binlog_end_pos
        -> binlog_xid_count_list iteration [Adding new xid_list_entry ]
        -> update_binlog_end_pos()

reset_logs ->  reset_master_pending [mark that is in progress]
           -> mark_xids_active && do_checkpoint_request [force a commit checkpoint first]
           -> rpl_global_gtid_binlog_state.load or rpl_global_gtid_binlog_state.reset
           -> reset_binlog_space_total [on error]


can_purge_log -> DBUG_ASSERT(),
              -> counter (binlog_xid_count_list)
              -> keep old binlolg open

count_binlog_space -> check if is_relay_log
new_file_impl -> create Rotate_log_event
              -> create algorithm
              -> 


write() -> DBUG_ASSERT() on error

close() -> get checksum_alg
        -> if binlog and write_state_to_file()


## RELAYLOG:

### How relay logs are now creted?
- Relay_log_info public member `MYSQL_BIN_LOG relay_log;` 
  -> how is instantated?


### What does is_relay_log?
write_description_event -> Format_description_log_event.set_relay_log_event()

open() -> checksum check BINLOG_CHECKSUM_ALG_UNDEF and assign algo
       -> signal_relay_log_update [Notify IO T ]

new_file_impl -> create Rotate_log_event  < +++ This function creates log files itslef
              -> create algorithm
              


Used in :
find_log_pos ->   normalize_binlog_name()
find_next_log ->  normalize_binlog_name()

`log.h`
write_description_event
signal_relay_log_update
update_binlog_end_pos
purge_logs_by_size


`log.cc`
Intact: 
1) `MYSQL_BIN_LOG::cleanup()`
2) `longlong Event_log::write_description_event(`
3) `MYSQL_BIN_LOG::open`

# Tests
- Using [base commit](https://github.com/MariaDB/server/commit/d51086a9f1b1b6a66c7ba8eb6a6876b433fa118f#diff-8954f28af66c39bc531d55364c372dce3068e0e9896e08747e993e8c7ebcd60e)

```
./mysql-test/mtr --parallel=auto --mem --force --max-test-fail=0 binlog.max_binlog_total_size perfschema.show_sanity sys_vars.max_binlog_total_size_basic
./mysql-test/mtr --parallel=auto --mem --force --max-test-fail=0 --suite=rpl
./mysql-test/mtr --parallel=auto --mem --force --max-test-fail=0 --suite=binlog
```
# Example of refactoring
`Refactor rpl_binlog_state into a base and a derived class`
https://github.com/MariaDB/server/commit/eae59ae2dc3efe8c4e08dbc074b9c458811b7ad4

# Other C++ questions
- When to use `inline`


# Other things

1. d43c15b0dee8 rfemove comment need_lock

new_file() used in ./sql/slave.cc
log.cc
new_file() is only used for rotation
new_file() is called, calls open(old_max_size), then before open() starts

2. Using keyword `using`
```
  using MYSQL_LOG::generate_name; -> not virtual in MYSQL_LOG
  using MYSQL_LOG::is_open;
```
MYSQL_LOG inherited from Event

3. virtual f `generate_new_name`
`generate_new_name` virtual in 
- MYSQL_BIN_LOG & 
- MYSQL_LOG (has virtual ~MYSQL_LOG() = default;) and `virtual` keyword for that < maybe doesn't make sense to have in MYSQL_BIN_LOG keyword (virtual - by default)

- 
# Testing
- After task 2
```
The servers were restarted 579 times
Spent 3064.010 of 484 seconds executing testcases

Completed: All 1179 tests were successful.

53 tests were skipped, 43 by the test itself.

```

# Virtual class can_purge_log
- `virtual` needs to use pointer or reference to achieve polymorphism
  - base class (MYSQL_BIN_LOG) may point to derived class and binds at runtime (late binding)
    - Early binding (compiletime) binding done on the type of pointer
  - if there is virtual class, child needs to write one ,otherwise, linker error `undefined reference to `MYSQL_BIN_LOG::can_purge_log(char const*)'`
- If virtual function of base class is not defined before is defined overriden version of child class - `unknown reference` will be called in linking time(see Solution 1)
  - https://cplusplus.com/forum/general/74973/
- New error: `undefined reference to `vtable for MYSQL_BINARY_LOG`
  - Seems virtual destructor for [pure] virtual needed, howerve handlng of ~MYSQL_BINARY_LOG is done on `mysql.exit()`
    - Virtual destrcutor allows that any pointer of base class that points to object of derived class, when deleted will delete also the object of child class, otherwise,
      there is UB (undefined behavior).

- `can_purge_log` 
Used in
1.  `log.cc`
```
purge_logs
purge_logs_before_date
real_purge_logs_by_size
```
2. `./sql/sys_vars.cc`
```
    /* Inform can_purge_log() that it should do a recheck of log_in_use() */
    sending_new_binlog_file++;
```
3. `./sql/sql_repl.cc`
```
  /* Counter used by can_purge_log() */
  sending_new_binlog_file++;
```

## Problems
### Solution 1 
- call implemented virtual method as overriden in child class
```C
   bool can_purge_log(const char *log_file_name) override
   {
      return MYSQL_BIN_LOG::can_purge_log(log_file_name);
   }
```
Result linker error (with ^ function being defined in the header), 
```
/usr/bin/ld: libmariadbd.a(log.cc.o): in function `MYSQL_BINARY_LOG::can_purge_log(char const*)':
/home/anel/GitHub/mariadb/server/src/11.4/sql/log.h:1178: undefined reference to `MYSQL_BIN_LOG::can_purge_log(char const*)'
/usr/bin/ld: libmariadbd.a(log.cc.o): in function `MYSQL_RELAY_LOG::can_purge_log(char const*)':
/home/anel/GitHub/mariadb/server/src/11.4/sql/log.h:1191: undefined reference to `MYSQL_BIN_LOG::can_purge_log(char const*)'
/usr/bin/ld: libmariadbd.a(log.cc.o):(.data.rel.ro._ZTV13MYSQL_BIN_LOG[_ZTV13MYSQL_BIN_LOG]+0x58): undefined reference to `MYSQL_BIN_LOG::can_purge_log(char const*)'

```

Result linker error in cpp file before/after implementation of `MYSQL_BIN_LOG::can_purge_log(log_file_name)`
```
[100%] Built target mariadb-backup
/usr/bin/ld: ../libmariadbd.a(log.cc.o): in function `MYSQL_BINARY_LOG::MYSQL_BINARY_LOG(unsigned int*, bool)':
/home/anel/GitHub/mariadb/server/src/11.4/sql/log.h:1175: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: /home/anel/GitHub/mariadb/server/src/11.4/sql/log.h:1175: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: ../libmariadbd.a(log.cc.o): in function `MYSQL_RELAY_LOG::MYSQL_RELAY_LOG(unsigned int*, bool)':
/home/anel/GitHub/mariadb/server/src/11.4/sql/log.h:1185: undefined reference to `vtable for MYSQL_RELAY_LOG'
/usr/bin/ld: /home/anel/GitHub/mariadb/server/src/11.4/sql/log.h:1185: undefined reference to `vtable for MYSQL_RELAY_LOG'
/usr/bin/ld: ../libmariadbd.a(log.cc.o):(.data.rel.ro._ZTV13MYSQL_BIN_LOG[_ZTV13MYSQL_BIN_LOG]+0x58): undefined reference to `MYSQL_BIN_LOG::can_purge_log(char const*)'
/usr/bin/ld: ../libmariadbd.a(log.cc.o): in function `MYSQL_BINARY_LOG::~MYSQL_BINARY_LOG()':
/home/anel/GitHub/mariadb/server/src/11.4/sql/log.h:1171: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: /home/anel/GitHub/mariadb/server/src/11.4/sql/log.h:1171: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: ../libmariadbd.a(log.cc.o): in function `MYSQL_RELAY_LOG::~MYSQL_RELAY_LOG()':
/home/anel/GitHub/mariadb/server/src/11.4/sql/log.h:1181: undefined reference to `vtable for MYSQL_RELAY_LOG'
/usr/bin/ld: /home/anel/GitHub/mariadb/server/src/11.4/sql/log.h:1181: undefined reference to `vtable for MYSQL_RELAY_LOG'
collect2: error: ld returned 1 exit status
```

## All functions

- is_relay_log part of code:
signal_relay_log_update -R

signal_bin_log_update - B

update_binlog_end_pos - BR

purge_logs_by_size -BR

MYSQL_BIN_LOG::cleanup()
MYSQL_BIN_LOG::open()
MYSQL_BIN_LOG::close()
MYSQL_BIN_LOG::find_log_pos   -> normalize_binlog_name
MYSQL_BIN_LOG::find_next_log  -> normalize_binlog_name
MYSQL_BIN_LOG::reset_logs
MYSQL_BIN_LOG::count_binlog_space() - B
MYSQL_BIN_LOG::new_file_impl()
MYSQL_BIN_LOG::write

- is_relay_log parameter
Event_log::write_description_event():: Event_log::MYSQL_LOG # Note MYSQL_BIN_LOG::Event_log (private)
normalize_binlog_name () -  inline function


This may be part of classess - depends on is_relay_log
enum_binlog_checksum_alg checksum_alg

We could create friend class to access private members (like MYSQL_LOG::name from write_commit function MYSQL_BINARY) or move the members
Used in `set_status_variables` if we move below members, that function in MYSQL-BIN_LOG will not konw about them
num_commits
num_group_commits
group_commit_trigger_count
group_commit_trigger_timeout
group_commit_trigger_lock_wait
IF we move them , `#define TC_LOG_BINLOG MYSQL_BINARY_LOG` -> ` MYSQL_BINARY_LOG::open(const char*)` etc


```
/home/anel/GitHub/mariadb/server/src/11.4/sql/rpl_mi.cc:1481:23: error: ‘class MYSQL_RELAY_LOG’ has no member named ‘reset_logs’
 1481 |     mi->rli.relay_log.reset_logs(current_thd, 0, (rpl_gtid*) 0, 0, 0);
      |                       ^~~~~~~~~~
[ 90%] Building CXX object sql/CMakeFiles/sql.dir/transaction.cc.o
/home/anel/GitHub/mariadb/server/src/11.4/sql/rpl_rli.cc: In destructor ‘virtual Relay_log_info::~Relay_log_info()’:
/home/anel/GitHub/mariadb/server/src/11.4/sql/rpl_rli.cc:117:21: error: ‘void Event_log::cleanup()’ is inaccessible within this context
  117 |   relay_log.cleanup();

```

- Problems with `open()`
https://stackoverflow.com/questions/6727087/c-virtual-function-being-hidden

- https://en.wikipedia.org/wiki/Curiously_recurring_template_pattern


# Potential fixes
## Encapsulation
~~- Move binlog_background_thread_started to private and make public getter~~ it is stsatic member

# MOnty cmoments
1. Failed compile
https://buildbot.mariadb.org/#/builders/353/builds/13640
```bash
/usr/bin/ld: libmariadbd.a(log.cc.o): in function `MYSQL_BINARY_LOG::MYSQL_BINARY_LOG(unsigned int*)':
/home/buildbot/aarch64-centos-stream9-rpm-autobake/build/padding_for_CPACK_RPM_BUILD_SOURCE_DIRS_PREFIX/sql/log.h:883: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: /home/buildbot/aarch64-centos-stream9-rpm-autobake/build/padding_for_CPACK_RPM_BUILD_SOURCE_DIRS_PREFIX/sql/log.h:883: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: ../../libmysqld/libmariadbd.a(log.cc.o): in function `MYSQL_BINARY_LOG::MYSQL_BINARY_LOG(unsigned int*)':
/home/buildbot/aarch64-centos-stream9-rpm-autobake/build/padding_for_CPACK_RPM_BUILD_SOURCE_DIRS_PREFIX/sql/log.h:883: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: /home/buildbot/aarch64-centos-stream9-rpm-autobake/build/padding_for_CPACK_RPM_BUILD_SOURCE_DIRS_PREFIX/sql/log.h:883: undefined reference to `vtable for MYSQL_BINARY_LOG'
collect2: error: ld returned 1 exit status
make[2]: *** [libmysqld/CMakeFiles/libmysqld.dir/build.make:103: libmysqld/libmariadbd.so.19] Error 1
make[1]: *** [CMakeFiles/Makefile2:16319: libmysqld/CMakeFiles/libmysqld.dir/all] Error 2
make[1]: *** Waiting for unfinished jobs....
collect2: error: ld returned 1 exit status
make[2]: *** [unittest/embedded/CMakeFiles/test-connect-t.dir/build.make:103: unittest/embedded/test-connect-t] Error 1
make[1]: *** [CMakeFiles/Makefile2:16453: unittest/embedded/CMakeFiles/test-connect-t.dir/all] Error 2
/usr/bin/ld: ../libmariadbd.a(log.cc.o): in function `MYSQL_BINARY_LOG::MYSQL_BINARY_LOG(unsigned int*)':
/home/buildbot/aarch64-centos-stream9-rpm-autobake/build/padding_for_CPACK_RPM_BUILD_SOURCE_DIRS_PREFIX/sql/log.h:883: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: /home/buildbot/aarch64-centos-stream9-rpm-autobake/build/padding_for_CPACK_RPM_BUILD_SOURCE_DIRS_PREFIX/sql/log.h:883: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: ../libmariadbd.a(log.cc.o): in function `MYSQL_BINARY_LOG::MYSQL_BINARY_LOG(unsigned int*)':
/home/buildbot/aarch64-centos-stream9-rpm-autobake/build/padding_for_CPACK_RPM_BUILD_SOURCE_DIRS_PREFIX/sql/log.h:883: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: /home/buildbot/aarch64-centos-stream9-rpm-autobake/build/padding_for_CPACK_RPM_BUILD_SOURCE_DIRS_PREFIX/sql/log.h:883: undefined reference to `vtable for MYSQL_BINARY_LOG'
```

https://buildbot.mariadb.org/#/builders/44/builds/25482
```
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=None -DCMAKE_INSTALL_SYSCONFDIR=/etc -DCMAKE_INSTALL_LOCALSTATEDIR=/var -DCMAKE_EXPORT_NO_PACKAGE_REGISTRY=ON -DCMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY=ON "-GUnix Makefiles" -DCMAKE_VERBOSE_MAKEFILE=ON -DCMAKE_INSTALL_LIBDIR=lib/aarch64-linux-gnu -DCMAKE_BUILD_TYPE=RelWithDebInfo "-DCOMPILATION_COMMENT=mariadb.org binary distribution" -DMYSQL_SERVER_SUFFIX=-1:11.4.0\+maria\~deb10 -DSYSTEM_TYPE=debian-linux-gnu -DCMAKE_SYSTEM_PROCESSOR=arm64 -DBUILD_CONFIG=mysql_release -DCONC_DEFAULT_CHARSET=utf8mb4 -DPLUGIN_AWS_KEY_MANAGEMENT=NO -DPLUGIN_COLUMNSTORE=NO -DDEB=Debian ..

/usr/bin/ld: ../libmariadbd.a(log.cc.o): in function `MYSQL_BINARY_LOG::~MYSQL_BINARY_LOG()':
./builddir/libmysqld/./sql/log.h:804: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: ./builddir/libmysqld/./sql/log.h:804: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: ../libmariadbd.a(log.cc.o): in function `non-virtual thunk to MYSQL_BINARY_LOG::~MYSQL_BINARY_LOG()':
./builddir/libmysqld/./sql/log.h:804: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: ./builddir/libmysqld/./sql/log.h:804: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: ../libmariadbd.a(log.cc.o): in function `MYSQL_BINARY_LOG::~MYSQL_BINARY_LOG()':
./builddir/libmysqld/./sql/log.h:804: undefined reference to `vtable for MYSQL_BINARY_LOG'
/usr/bin/ld: ../libmariadbd.a(log.cc.o):./builddir/libmysqld/./sql/log.h:804: more undefined references to `vtable for MYSQL_BINARY_LOG' follow
collect2: error: ld returned 1 exit status
make[4]: *** [libmysqld/examples/CMakeFiles/mariadb-test-embedded.dir/build.make:93: libmysqld/examples/mariadb-test-embedded] Error 1
make[3]: *** [CMakeFiles/Makefile2:15001: libmysqld/examples/CMakeFiles/mariadb-test-embedded.dir/all] Error 2
```
2. 


