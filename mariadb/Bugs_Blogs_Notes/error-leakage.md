[100%] Built target mariadb-client-test-embedded
[100%] Built target test-connect-t
[100%] Built target libmysqld
[100%] Built target symlink_libmysqld.so

When using free_list() instead of free_list_pair()


Logging: /home/anel/mariadb/server/src/10.11/mysql-test/mariadb-test-run.pl  replicate_rewrite_db
VS config:
vardir: /home/anel/mariadb/server/build/10.11/mysql-test/var
Checking leftover processes...
 - found old pid 60315 in 'mysqld.1.pid', killing it...
   process did not exist!
Removing old var directory...
Creating var directory '/home/anel/mariadb/server/build/10.11/mysql-test/var'...
Checking supported features...
MariaDB Version 10.11.0-MariaDB-debug
 - SSL connections supported
 - binaries are debug compiled
 - binaries built with wsrep patch
Collecting tests...
Installing system database...

==============================================================================

TEST                                      RESULT   TIME (ms) or COMMENT
--------------------------------------------------------------------------

worker[1] Using MTR_BUILD_THREAD 300, with reserved ports 16000..16019
sys_vars.replicate_rewrite_db            [ pass ]     13
***Warnings generated in error logs during shutdown after running tests: sys_vars.replicate_rewrite_db

Warning: Memory not freed: 752
Warning:   32 bytes lost at 0x7fe500187c10, allocated by T@0 at sql/rpl_filter.cc:574, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe500187d50, allocated by T@0 at sql/rpl_filter.cc:554, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe5001919d0, allocated by T@0 at sql/rpl_filter.cc:574, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   40 bytes lost at 0x7fe50020b340, allocated by T@0 at sql/rpl_filter.cc:554, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe50000acd0, allocated by T@0 at sql/rpl_filter.cc:574, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe500013cb0, allocated by T@0 at sql/rpl_filter.cc:554, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe500040f30, allocated by T@0 at sql/rpl_filter.cc:574, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe50015d8d0, allocated by T@0 at sql/rpl_filter.cc:554, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe50010b1d0, allocated by T@0 at sql/rpl_filter.cc:574, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe500171770, allocated by T@0 at sql/rpl_filter.cc:554, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe500173940, allocated by T@0 at sql/rpl_filter.cc:574, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe500176b40, allocated by T@0 at sql/rpl_filter.cc:554, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe500215770, allocated by T@0 at sql/rpl_filter.cc:574, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe5002156d0, allocated by T@0 at sql/rpl_filter.cc:554, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe500008690, allocated by T@0 at sql/rpl_filter.cc:574, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe5001093b0, allocated by T@0 at sql/rpl_filter.cc:554, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x7fe500109450, allocated by T@0 at sql/rpl_filter.cc:554, sql/rpl_filter.cc:611, sql/rpl_filter.cc:313, sql/rpl_filter.cc:636, sql/sys_vars.cc:5421, sql/sys_vars.cc:5403, sql/set_var.cc:207, sql/set_var.cc:863
Warning:   32 bytes lost at 0x5596b5612910, allocated by T@0 at sql/rpl_filter.cc:574, sql/rpl_filter.cc:611, sql/mysqld.cc:8072, mysys/my_getopt.c:655, sql/mysqld.cc:8453, sql/mysqld.cc:4024, sql/mysqld.cc:5685, sql/main.cc:34
Warning:   32 bytes lost at 0x5596b5612870, allocated by T@0 at sql/rpl_filter.cc:554, sql/rpl_filter.cc:611, sql/mysqld.cc:8072, mysys/my_getopt.c:655, sql/mysqld.cc:8453, sql/mysqld.cc:4024, sql/mysqld.cc:5685, sql/main.cc:34
