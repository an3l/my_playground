# MDEV-32942 my_print_defaults leaks memory with wrong configuration file
https://jira.mariadb.org/browse/MDEV-32942

## Memory corruption 
```
$ ./extra/my_print_defaults '--defaults-file=~/nofile.cnf' --mysqld mysql_install_db mariadb-install-db
Could not open required defaults file: /home/anel/nofile.cnf
Fatal error in defaults handling. Program aborted

=================================================================
==55684==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 120 byte(s) in 1 object(s) allocated from:
    #0 0x7f7bbb3c7808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x555c12901133 in my_malloc /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:101
    #2 0x555c128e28cb in main /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:174
    #3 0x7f7bbad59082 in __libc_start_main ../csu/libc-start.c:308
    #4 0x555c128e220d in _start (/home/anel/GitHub/mariadb/server/build/10.4/extra/my_print_defaults+0x7420d)

SUMMARY: AddressSanitizer: 120 byte(s) leaked in 1 allocation(s).
Aborted (core dumped)
```

Found by testing
```bash
$ bash -x ./scripts/mysql_install_db --defaults-file=~/nofile.cnf
+ basedir=
+ builddir=
+ ldata=./data
+ langdir=
+ srcdir=
+ log_error=
+ args=
+ defaults=
+ defaults_group_suffix=
+ mysqld_opt=
+ user=
+ group=
+ silent_startup=--silent-startup
+ force=0
+ in_rpm=0
+ ip_only=0
+ cross_bootstrap=0
+ auth_root_authentication_method=socket
+ auth_root_socket_user=
+ skip_test_db=0
++ dirname ./scripts/mysql_install_db
+ dirname0=./scripts
++ dirname ./scripts
+ dirname0=.
+ parse_arguments '--defaults-file=~/nofile.cnf'
+ pick_args=
+ test '--defaults-file=~/nofile.cnf' = PICK-ARGS-FROM-ARGV
+ for arg in "$@"
+ case "$arg" in
+ defaults='--defaults-file=~/nofile.cnf'
+ test -n ''
+ test -n ''
+ test -n ''
+ test -n . -a -x ././bin/my_print_defaults
+ test -x ./extra/my_print_defaults
+ srcdir=.
+ builddir=.
+ print_defaults=./extra/my_print_defaults
+ test '!' -x ./extra/my_print_defaults
++ ./extra/my_print_defaults '--defaults-file=~/nofile.cnf' --mysqld mysql_install_db mariadb-install-db
Could not open required defaults file: /home/anel/nofile.cnf
Fatal error in defaults handling. Program aborted

=================================================================
==55287==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 120 byte(s) in 1 object(s) allocated from:
    #0 0x7f476c508808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x55efcc453133 in my_malloc /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:101
    #2 0x55efcc4348cb in main /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:174
    #3 0x7f476be9a082 in __libc_start_main ../csu/libc-start.c:308
    #4 0x55efcc43420d in _start (/home/anel/GitHub/mariadb/server/build/10.4/extra/my_print_defaults+0x7420d)

SUMMARY: AddressSanitizer: 120 byte(s) leaked in 1 allocation(s).
+ parse_arguments
+ pick_args=

```

## Debug
```
gdb) r '--defaults-file=~/nofile.cnf' --mysqld mysql_install_db mariadb-install-db
+r '--defaults-file=~/nofile.cnf' --mysqld mysql_install_db mariadb-install-db
Starting program: /home/anel/GitHub/mariadb/server/build/10.4/extra/my_print_defaults '--defaults-file=~/nofile.cnf' --mysqld mysql_install_db mariadb-install-db
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Could not open required defaults file: /home/anel/nofile.cnf
Fatal error in defaults handling. Program aborted
==59572==LeakSanitizer has encountered a fatal error.
==59572==HINT: For debugging, try setting environment variable LSAN_OPTIONS=verbosity=1:log_threads=1
==59572==HINT: LeakSanitizer does not work under ptrace (strace, gdb, etc)

Program received signal SIGABRT, Aborted.
__GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
50	../sysdeps/unix/sysv/linux/raise.c: No such file or directory.
```

```
$ LSAN_OPTIONS=verbosity=1:log_threads=1 ./extra/my_print_defaults '--defaults-file=~/nofile.cnf' --mysqld mysql_install_db mariadb-install-db
==60009==AddressSanitizer: libc interceptors initialized
|| `[0x10007fff8000, 0x7fffffffffff]` || HighMem    ||
|| `[0x02008fff7000, 0x10007fff7fff]` || HighShadow ||
|| `[0x00008fff7000, 0x02008fff6fff]` || ShadowGap  ||
|| `[0x00007fff8000, 0x00008fff6fff]` || LowShadow  ||
|| `[0x000000000000, 0x00007fff7fff]` || LowMem     ||
MemToShadow(shadow): 0x00008fff7000 0x000091ff6dff 0x004091ff6e00 0x02008fff6fff
redzone=16
max_redzone=2048
quarantine_size_mb=256M
thread_local_quarantine_size_kb=1024K
malloc_context_size=30
SHADOW_SCALE: 3
SHADOW_GRANULARITY: 8
SHADOW_OFFSET: 0x7fff8000
==60009==Installed the sigaction for signal 11
==60009==Installed the sigaction for signal 7
==60009==Installed the sigaction for signal 8
==60009==T0: stack [0x7ffe1d2b7000,0x7ffe1dab7000) size 0x800000; local=0x7ffe1dab4534
==60009==AddressSanitizer Init done
Could not open required defaults file: /home/anel/nofile.cnf
Fatal error in defaults handling. Program aborted
==60010==Processing thread 60009.
==60010==Stack at 0x7ffe1d2b7000-0x7ffe1dab7000 (SP = 0x7ffe1dab4128).
==60010==TLS at 0x7f40721ecbc0-0x7f40721edc80.

=================================================================
==60009==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 120 byte(s) in 1 object(s) allocated from:
    #0 0x7f407288a808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x557a80bdc133 in my_malloc /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:101
    #2 0x557a80bbd8cb in main /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:174
    #3 0x7f407221c082 in __libc_start_main ../csu/libc-start.c:308
    #4 0x557a80bbd20d in _start (/home/anel/GitHub/mariadb/server/build/10.4/extra/my_print_defaults+0x7420d)

SUMMARY: AddressSanitizer: 120 byte(s) leaked in 1 allocation(s).
Aborted (core dumped)

```


### GDB
(gdb) p arguments
+p arguments
$3 = (char **) 0x7fffffffd8a0
(gdb) p *arguments
+p *arguments
$4 = 0x7fffffffde48 "/home/anel/GitHub/mariadb/server/build/10.4/extra/my_print_defaults"
(gdb) p arguments[0]
+p arguments[0]
$6 = 0x7fffffffde48 "/home/anel/GitHub/mariadb/server/build/10.4/extra/my_print_defaults"
(gdb) p arguments[1]
+p arguments[1]
$7 = 0x7fffffffde8c "--defaults-file=~/nofile.cnf"
(gdb) p arguments[2]
+p arguments[2]
$8 = 0x607000000041 "/lib/x86_64-linux-gnu/libasan.so.5"
(gdb) p arguments[3]

(gdb) p *options
+p *options
$18 = {
  name = 0x5555556cf300 "debug",
  id = 35,
  comment = 0x5555556cf340 "Output debug log",
  value = 0x5555558590e0 <default_dbug_option>,
  u_max_value = 0x5555558590e0 <default_dbug_option>,
  typelib = 0x0,
  var_type = 9,
  arg_type = OPT_ARG,
  def_value = 0,
  min_value = 0,
  max_value = 0,
  sub_size = 0,
  block_size = 0,
  app_type = 0x0
}

(gdb) p *options
+p *options
$25 = {
  name = 0x5555556cf380 "defaults-file",
  id = 99,
  comment = 0x5555556cf3c0 "Read this file only, do not read global or per-user config files; should be the first option",
  value = 0x5555558590a0 <config_file>,
  u_max_value = 0x5555558590a0 <config_file>,
  typelib = 0x0,
  var_type = 9,
  arg_type = REQUIRED_ARG,
  def_value = 0,
  min_value = 0,
  max_value = 0,
  sub_size = 0,
  block_size = 0,
  app_type = 0x0
}


(gdb) p *options
+p *options
$28 = {
  name = 0x5555556cf440 "defaults-extra-file",
  id = 101,
  comment = 0x5555556cf480 "Read this file after the global config file and before the config file in the users home directory; should be the first option",
  value = 0x555555a4d080 <my_defaults_extra_file>,
  u_max_value = 0x555555a4d080 <my_defaults_extra_file>,
  typelib = 0x0,
  var_type = 9,
  arg_type = REQUIRED_ARG,
  def_value = 0,
  min_value = 0,
  max_value = 0,
  sub_size = 0,
  block_size = 0,
  app_type = 0x0
}


# sets value
(gdb) f 0
+f 0
#0  setval (opts=0x5555558591f0 <my_long_options+112>, value=0x5555558590a0 <config_file>, argument=0x7fffffffde9c "~/nofile.cnf", set_maximum_value=0 '\000') at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_getopt.c:776

+p *load_default_groups@13
$56 =   {[0] = 0x5555556cf020 "mysqld",
  [1] = 0x5555556cf060 "server",
  [2] = 0x5555556cf0a0 "mysqld-10.4",
  [3] = 0x5555556cf0e0 "mariadb",
  [4] = 0x5555556cf120 "mariadb-10.4",
  [5] = 0x5555556cf160 "mariadbd",
  [6] = 0x5555556cf1a0 "mariadbd-10.4",
  [7] = 0x5555556cf1e0 "client-server",
  [8] = 0x5555556cf220 "galera",
  [9] = 0x7fffffffdeb2 "mysql_install_db",
  [10] = 0x7fffffffdec3 "mariadb-install-db",
  [11] = 0x0}
  [12] = 0xbebebebebebebebe <error: Cannot access memory at address 0xbebebebebebebebe>}


(gdb) f 0
#0  my_load_defaults (conf_file=0x7fffffffde9c "~/nofile.cnf", groups=0x60c000000048, argc=0x7fffffffd7e0, argv=0x7fffffffd800, default_directories=0x555555a4d540 <default_directories>) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_default.c:522
(gdb) p my_load_defaults 
+p my_load_defaults
$59 = {int (const char *, const char **, int *, char ***, const char ***)} 0x5555555cb2f0 <my_load_defaults>


(gdb) p alloc
+p alloc
$61 = {
  free = 0x7fffffffd760,
  used = 0x5555555e73ee <my_malloc+1077>,
  pre_alloc = 0x10,
  min_malloc = 112,
  block_size = 0,
  block_num = 72,
  first_block_usage = 24768,
  flags = 0,
  error_handler = 0x41b58ab3,
  name = 0x5555556d7860 "1 32 32 19 _db_stack_frame_:88"
}

(gdb) bt
+bt
#0  alloc_root (mem_root=0x7fffffffd680, length=72) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_alloc.c:255
#1  0x00005555555cfb2c in init_default_directories (alloc=0x7fffffffd680) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_default.c:1193
#2  0x00005555555cb4a7 in my_load_defaults (conf_file=0x7fffffffde9c "~/nofile.cnf", groups=0x60c000000048, argc=0x7fffffffd7e0, argv=0x7fffffffd800, default_directories=0x555555a4d540 <default_directories>) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_default.c:52
3
#3  0x00005555555cb2ee in load_defaults (conf_file=0x7fffffffde9c "~/nofile.cnf", groups=0x60c000000048, argc=0x7fffffffd7e0, argv=0x7fffffffd800) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_default.c:467
#4  0x00005555555c8a4f in main (argc=2, argv=0x7fffffffda30) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:183
(gdb) 

```

### my_malloc calls
```
1.
(gdb) bt
+bt
#0  my_malloc (size=106858786324544, my_flags=140737353941306) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:86
#1  0x00005555556067a0 in my_multi_malloc (myFlags=24) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/mulalloc.c:51
#2  0x00005555555ed144 in safe_mutex_lazy_init_deadlock_detection (mp=0x555555a573e0 <THR_LOCK_threads>) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:159
#3  0x00005555555eddcc in safe_mutex_lock (mp=0x555555a573e0 <THR_LOCK_threads>, my_flags=0, file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", line=307) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:319
#4  0x00005555555eaf93 in inline_mysql_mutex_lock (that=0x555555a573e0 <THR_LOCK_threads>, src_file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", src_line=307) at /home/anel/GitHub/mariadb/server/src/10.4/include/mysql/psi/mysql_thread.h:71
7
#5  0x00005555555ec474 in my_thread_init () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:307
#6  0x00005555555ebef8 in my_thread_global_init () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:190
#7  0x00005555555e4a95 in my_init () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_init.c:105
#8  0x00005555555c872b in main (argc=5, argv=0x7fffffffda28) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:151

(gdb) f 8
+f 8
#8  0x00005555555c872b in main (argc=5, argv=0x7fffffffda28) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:151


2. 
Breakpoint 1, my_malloc (size=3816988362448284928, my_flags=140737488343392) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:86
(gdb) bt
+bt
#0  my_malloc (size=3816988362448284928, my_flags=140737488343392) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:86
#1  0x00005555555f46f2 in init_dynamic_array2 (array=0x611000000070, element_size=16, init_buffer=0x0, init_alloc=128, alloc_increment=64, my_flags=0) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/array.c:70
#2  0x00005555555fe54b in my_hash_init2 (hash=0x611000000048, growth_size=64, charset=0x55555586d4e0 <my_charset_bin>, size=128, key_offset=40, key_length=8, get_key=0x0, hash_function=0x0, free_element=0x0, flags=1) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/hash.c
:98
#3  0x00005555555ed28c in safe_mutex_lazy_init_deadlock_detection (mp=0x555555a573e0 <THR_LOCK_threads>) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:172
#4  0x00005555555eddcc in safe_mutex_lock (mp=0x555555a573e0 <THR_LOCK_threads>, my_flags=0, file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", line=307) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:319
#5  0x00005555555eaf93 in inline_mysql_mutex_lock (that=0x555555a573e0 <THR_LOCK_threads>, src_file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", src_line=307) at /home/anel/GitHub/mariadb/server/src/10.4/include/mysql/psi/mysql_thread.h:71
7
#6  0x00005555555ec474 in my_thread_init () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:307
#7  0x00005555555ebef8 in my_thread_global_init () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:190
#8  0x00005555555e4a95 in my_init () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_init.c:105
#9  0x00005555555c872b in main (argc=5, argv=0x7fffffffda28) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:151


3. OVO je nase load_default_groups
Breakpoint 1, my_malloc (size=2048, my_flags=0) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:86
(gdb) bt
+bt
#0  my_malloc (size=2048, my_flags=0) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:86
#1  0x00005555555f46f2 in init_dynamic_array2 (array=0x6110000000d8, element_size=16, init_buffer=0x0, init_alloc=128, alloc_increment=64, my_flags=0) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/array.c:70
#2  0x00005555555fe54b in my_hash_init2 (hash=0x6110000000b0, growth_size=64, charset=0x55555586d4e0 <my_charset_bin>, size=128, key_offset=120, key_length=8, get_key=0x0, hash_function=0x0, free_element=0x0, flags=1) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/hash.
c:98
#3  0x00005555555ed2ef in safe_mutex_lazy_init_deadlock_detection (mp=0x555555a573e0 <THR_LOCK_threads>) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:177
#4  0x00005555555eddcc in safe_mutex_lock (mp=0x555555a573e0 <THR_LOCK_threads>, my_flags=0, file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", line=307) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:319
#5  0x00005555555eaf93 in inline_mysql_mutex_lock (that=0x555555a573e0 <THR_LOCK_threads>, src_file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", src_line=307) at /home/anel/GitHub/mariadb/server/src/10.4/include/mysql/psi/mysql_thread.h:71
7
#6  0x00005555555ec474 in my_thread_init () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:307
#7  0x00005555555ebef8 in my_thread_global_init () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:190
#8  0x00005555555e4a95 in my_init () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_init.c:105
#9  0x00005555555c872b in main (argc=5, argv=0x7fffffffda28) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:151


4.  Ovo je load_defaults
(gdb) bt
+bt
#0  my_malloc (size=3816988362448284928, my_flags=140737488343728) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:86
#1  0x00005555555d4f5a in alloc_root (mem_root=0x7fffffffd680, length=72) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_alloc.c:246
#2  0x00005555555cfb2c in init_default_directories (alloc=0x7fffffffd680) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_default.c:1193
#3  0x00005555555cb4a7 in my_load_defaults (conf_file=0x7fffffffde9c "~/nofile.cnf", groups=0x60c000000048, argc=0x7fffffffd7e0, argv=0x7fffffffd800, default_directories=0x555555a4d540 <default_directories>) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_default.c:52
3
#4  0x00005555555cb2ee in load_defaults (conf_file=0x7fffffffde9c "~/nofile.cnf", groups=0x60c000000048, argc=0x7fffffffd7e0, argv=0x7fffffffd800) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_default.c:467
#5  0x00005555555c8a4f in main (argc=2, argv=0x7fffffffda30) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:183

5.
(gdb) bt
+bt
#0  my_malloc (size=472, my_flags=64) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:86
#1  0x00005555555f46f2 in init_dynamic_array2 (array=0x7fffffffd5c0, element_size=8, init_buffer=0x0, init_alloc=128, alloc_increment=64, my_flags=0) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/array.c:70
#2  0x00005555555cbb06 in my_load_defaults (conf_file=0x7fffffffde9c "~/nofile.cnf", groups=0x60c0000000a0, argc=0x7fffffffd7e0, argv=0x7fffffffd800, default_directories=0x555555a4d540 <default_directories>) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_default.c:56
8
#3  0x00005555555cb2ee in load_defaults (conf_file=0x7fffffffde9c "~/nofile.cnf", groups=0x60c000000048, argc=0x7fffffffd7e0, argv=0x7fffffffd800) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_default.c:467
#4  0x00005555555c8a4f in main (argc=2, argv=0x7fffffffda30) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:183


(gdb) f 1
+f 1
#1  0x00005555555c88cc in main (argc=2, argv=0x7fffffffda30) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:174

```


### my_free calls
1.
- On first call we get the error (function load_defaults)
- FUnction of interest: my_load_defaults, my_search_option_files

```
(gdb) c 
+c
Continuing.
Could not open required defaults file: /home/anel/nofile.cnf
Fatal error in defaults handling. Program aborted

Breakpoint 2, my_free (ptr=0x5555556d0280) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:206
(gdb) bt
+bt
#0  my_free (ptr=0x5555556d0280) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:206
#1  0x00005555555f5d85 in delete_dynamic (array=0x7fffffffd5c0) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/array.c:303
#2  0x00005555555cbc0a in my_load_defaults (conf_file=0x7fffffffde9c "~/nofile.cnf", groups=0x60c0000000a0, argc=0x7fffffffd7e0, argv=0x7fffffffd800, default_directories=0x555555a4d540 <default_directories>) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_default.c:57
9
#3  0x00005555555cb2ee in load_defaults (conf_file=0x7fffffffde9c "~/nofile.cnf", groups=0x60c000000048, argc=0x7fffffffd7e0, argv=0x7fffffffd800) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_default.c:467
#4  0x00005555555c8a4f in main (argc=2, argv=0x7fffffffda30) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:183

```

2. my_end(0)
```
Breakpoint 2, my_free (ptr=0x100000190) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:206
(gdb) bt
+bt
#0  my_free (ptr=0x100000190) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:206
#1  0x00005555555f5d85 in delete_dynamic (array=0x6110000000d8) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/array.c:303
#2  0x00005555555fe8f9 in my_hash_free (hash=0x6110000000b0) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/hash.c:158
#3  0x00005555555f0366 in safe_mutex_free_deadlock_data (mp=0x555555a573e0 <THR_LOCK_threads>) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:665
#4  0x00005555555f009e in safe_mutex_destroy (mp=0x555555a573e0 <THR_LOCK_threads>, file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", line=102) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:604
#5  0x00005555555ead43 in inline_mysql_mutex_destroy (that=0x555555a573e0 <THR_LOCK_threads>, src_file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", src_line=102) at /home/anel/GitHub/mariadb/server/src/10.4/include/mysql/psi/mysql_thread.h
:676
#6  0x00005555555ebba0 in my_thread_destroy_internal_mutex () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:102
#7  0x00005555555ec1bd in my_thread_global_end () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:243
#8  0x00005555555e560a in my_end (infoflag=0) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_init.c:233
#9  0x00005555555c8a6c in main (argc=2, argv=0x7fffffffda30) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:186

```
3.
```
gdb) bt
+bt
#0  my_free (ptr=0x61d000000a88) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:206
#1  0x00005555555f5d85 in delete_dynamic (array=0x611000000070) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/array.c:303
#2  0x00005555555fe8f9 in my_hash_free (hash=0x611000000048) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/hash.c:158
#3  0x00005555555f03a0 in safe_mutex_free_deadlock_data (mp=0x555555a573e0 <THR_LOCK_threads>) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:666
#4  0x00005555555f009e in safe_mutex_destroy (mp=0x555555a573e0 <THR_LOCK_threads>, file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", line=102) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:604
#5  0x00005555555ead43 in inline_mysql_mutex_destroy (that=0x555555a573e0 <THR_LOCK_threads>, src_file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", src_line=102) at /home/anel/GitHub/mariadb/server/src/10.4/include/mysql/psi/mysql_thread.h
:676
#6  0x00005555555ebba0 in my_thread_destroy_internal_mutex () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:102
#7  0x00005555555ec1bd in my_thread_global_end () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:243
#8  0x00005555555e560a in my_end (infoflag=0) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_init.c:233
#9  0x00005555555c8a6c in main (argc=2, argv=0x7fffffffda30) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:186
```
4.
```
(gdb) bt
+bt
#0  my_free (ptr=0xffffffffa1a) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_malloc.c:206
#1  0x00005555555f03da in safe_mutex_free_deadlock_data (mp=0x555555a573e0 <THR_LOCK_threads>) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:667
#2  0x00005555555f009e in safe_mutex_destroy (mp=0x555555a573e0 <THR_LOCK_threads>, file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", line=102) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/thr_mutex.c:604
#3  0x00005555555ead43 in inline_mysql_mutex_destroy (that=0x555555a573e0 <THR_LOCK_threads>, src_file=0x5555556d8fc0 "/home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c", src_line=102) at /home/anel/GitHub/mariadb/server/src/10.4/include/mysql/psi/mysql_thread.h
:676
#4  0x00005555555ebba0 in my_thread_destroy_internal_mutex () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:102
#5  0x00005555555ec1bd in my_thread_global_end () at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_thr_init.c:243
#6  0x00005555555e560a in my_end (infoflag=0) at /home/anel/GitHub/mariadb/server/src/10.4/mysys/my_init.c:233
#7  0x00005555555c8a6c in main (argc=2, argv=0x7fffffffda30) at /home/anel/GitHub/mariadb/server/src/10.4/extra/my_print_defaults.c:186


Program received signal SIGABRT, Aborted.
__GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
../sysdeps/unix/sysv/linux/raise.c: No such file or directory.
(gdb) bt
+bt
#0  __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
#1  0x00007ffff700b859 in __GI_abort () at abort.c:79
#2  0x00007ffff76992e2 in __sanitizer::Abort () at ../../../../src/libsanitizer/sanitizer_common/sanitizer_posix_libcdep.cc:155
#3  0x00007ffff76a3e8c in __sanitizer::Die () at ../../../../src/libsanitizer/sanitizer_common/sanitizer_termination.cc:57
#4  0x00007ffff76a8fbf in __lsan::CheckForLeaks () at ../../../../src/libsanitizer/lsan/lsan_common.cc:585
#5  0x00007ffff76a8ff9 in __lsan::DoLeakCheck () at ../../../../src/libsanitizer/lsan/lsan_common.cc:616
#6  __lsan::DoLeakCheck () at ../../../../src/libsanitizer/lsan/lsan_common.cc:611
#7  0x00007ffff702ffde in __cxa_finalize (d=0x7ffff76f64a0) at cxa_finalize.c:83
#8  0x00007ffff7590be7 in __do_global_dtors_aux () at ../../../../src/libsanitizer/sanitizer_common/sanitizer_internal_defs.h:382
#9  0x00007fffffffd8d0 in ?? ()
#10 0x00007ffff7fe0f6b in _dl_fini () at dl-fini.c:138
Backtrace stopped: frame did not save the PC

```

