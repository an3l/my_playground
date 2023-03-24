# Debug info in C
- [PR 2547](https://github.com/MariaDB/server/pull/2547)
- [MDEV-20738: my_addr_resolve passes invalid offsets to addr2line](https://jira.mariadb.org/browse/MDEV-20738)

## backtrace_symbols_fd
- It is function within program library `execinfo` with header `exec_info.h`, see `man 3 backtrace_symbols_fd`.
- We can find `execinfo.h`
```bash
$ sudo find /|grep execinfo.h
/usr/include/execinfo.h
```
So we can find (search) package with this file
```bash
$ dpkg -S /usr/include/execinfo.h 
libc6-dev:amd64: /usr/include/execinfo.h
```
We can list all files of package `libc6-dev` (how to find it's binary package?)
```bash
$ dpkg -L libc6-dev
# Here are static and dynamic libraries for libc
/usr/lib/x86_64-linux-gnu/libc.a
/usr/lib/x86_64-linux-gnu/libc.so
```

- [Differences between glibc and libc for Ubuntu](https://stackoverflow.com/questions/54053087/libc-or-glibc-in-ubuntu)
  - [glibc](https://packages.ubuntu.com/search?keywords=glibc&searchon=sourcenames&suite=all&section=all) is source package
  - [libc6](https://packages.ubuntu.com/search?keywords=libc6&searchon=names&suite=all&section=all) is installed binary package
  - `glibc-debuginfo` referenced by PR is [package on RPM not on Ubuntu](https://unix.stackexchange.com/questions/645907/glibc-debuginfo-ubuntu),
  - On ubuntu 22.04 or later there is `debuginfd`, but before it seems alternative is [debug-symbol](https://wiki.ubuntu.com/Debug%20Symbol%20Packages):
    - package `ubuntu-dbgsym-keyring`, `xserver-xorg-core-dbgsym`, `xserver-xorg-core-dbg` (not installed)
    - Ubuntu has `*-dbgsym.ddeb` packages

- However for debugging follow [full source code debugging of the C library on Ubuntu](https://stackoverflow.com/questions/48278881/gdb-complaining-about-missing-raise-c/48287761#48287761)
  Above says about:
  - `libc6-dbg` dependent on `gdb`
  - About debian devepoment tool `dpkg-dev` (needed to download and process the source files `deb-src`)
  - `$ apt-cache showpkg libc6 | more` find which distro libc6 came from and find out which deb-src you need
    Additionally we may find reverse depends packages
    ```bash
        Reverse Depends:
        libc6-dbg,libc6 2.31-0ubuntu9.7
        update-notifier,libc6 2.7
        mariadb-server-10.3,libc6 2.29
        mariadb-client-10.3,libc6 2.28
    ```
  - how to get dependecy of a package and which packages are dependent on this one (example below)
```bash
# Install libc6-dbg, it is a dependecy of `gdb`
# Check if installed
$ dpkg -l libc6-dbg
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name            Version         Architecture Description
+++-===============-===============-============-=========================================
ii  libc6-dbg:amd64 2.31-0ubuntu9.9 amd64        GNU C Library: detached debugging symbols
# Check files

# Check gdb package
$ dpkg -l gdb
# Check files
$ dpkg -L gdb

# Check that <gdb> depends on libc6-dbg <depends>
$ apt-cache depends gdb
gdb
  Depends: libbabeltrace1
  Depends: libc6
  Depends: libexpat1
  Depends: libgcc-s1
  Depends: liblzma5
  Depends: libmpfr6
  Depends: libncursesw6
  Depends: libpython3.8
  Depends: libreadline8
  Depends: libstdc++6
  Depends: libtinfo6
  Depends: zlib1g
  Conflicts: gdb
  Recommends: <libc-dbg>
    libc6-dbg
  Recommends: libcc1-0
  Recommends: gdbserver
  Suggests: gdb-doc
  Replaces: gdb
  Replaces: gdb-doc

# Check which package depends on gdb <rdepends>
$ apt-cache rdepends gdb 

```
## MariaDB usage

- In file `configure.cmake`, there is custom function
```cmake
# Searches function in libraries
# if function is found, sets output parameter result to the name of the library
# if function is found in libc, result will be empty 
FUNCTION(MY_SEARCH_LIBS func libs result)
```
- So example would be:
```cmake
  MY_SEARCH_LIBS(backtrace_symbols_fd execinfo LIBEXECINFO)
```
- Library name is `libexecinfo`

### Repeat procedure from MDEV-20738
- Repeat procedure from [MDEV-20738](https://jira.mariadb.org/browse/MDEV-20738)
```bash
$ sudo systemctl status mariadb
$ sudo kill -s 11 $(pidof mariadbd)
```
- Still works
```bash
# Error log generated, but empty
$ cat /var/log/mysql/error.log
$ ls /var/log/mysql # weird admin group "adm"
-rw-r-----  1 mysql adm       0 Mar 24 09:10 error.log
```
- Howerver there is an error in `journal`
```bash
$ sudo journalctl -u mariadb
....
Mar 24 14:08:01 anel mariadbd[18653]: 230324 14:08:01 [ERROR] mysqld got signal 11 ;
Mar 24 14:08:01 anel mariadbd[18653]: This could be because you hit a bug. It is also possible that this binary
Mar 24 14:08:01 anel mariadbd[18653]: or one of the libraries it was linked against is corrupt, improperly built,
Mar 24 14:08:01 anel mariadbd[18653]: or misconfigured. This error can also be caused by malfunctioning hardware.
Mar 24 14:08:01 anel mariadbd[18653]: To report this bug, see https://mariadb.com/kb/en/reporting-bugs
Mar 24 14:08:01 anel mariadbd[18653]: We will try our best to scrape up some info that will hopefully help
Mar 24 14:08:01 anel mariadbd[18653]: diagnose the problem, but since we have already crashed,
Mar 24 14:08:01 anel mariadbd[18653]: something is definitely wrong and this may fail.
Mar 24 14:08:01 anel mariadbd[18653]: Server version: 10.6.12-MariaDB-1:10.6.12+maria~ubu2004 source revision: 4c79e15cc3716f69c044d428>
Mar 24 14:08:01 anel mariadbd[18653]: key_buffer_size=134217728
Mar 24 14:08:01 anel mariadbd[18653]: read_buffer_size=131072
Mar 24 14:08:01 anel mariadbd[18653]: max_used_connections=1
Mar 24 14:08:01 anel mariadbd[18653]: max_threads=153
Mar 24 14:08:01 anel mariadbd[18653]: thread_count=0
Mar 24 14:08:01 anel mariadbd[18653]: It is possible that mysqld could use up to
Mar 24 14:08:01 anel mariadbd[18653]: key_buffer_size + (read_buffer_size + sort_buffer_size)*max_threads = 467967 K  bytes of memory
Mar 24 14:08:01 anel mariadbd[18653]: Hope that's ok; if not, decrease some variables in the equation.
Mar 24 14:08:01 anel mariadbd[18653]: Thread pointer: 0x0
Mar 24 14:08:01 anel mariadbd[18653]: Attempting backtrace. You can use the following information to find out
Mar 24 14:08:01 anel mariadbd[18653]: where mysqld died. If you see no messages after this, something went
Mar 24 14:08:01 anel mariadbd[18653]: terribly wrong...
Mar 24 14:08:01 anel mariadbd[18653]: stack_bottom = 0x0 thread_stack 0x49000
Mar 24 14:08:01 anel mariadbd[18653]: ??:0(my_print_stacktrace)[0x5613038340c2]
Mar 24 14:08:01 anel mariadbd[18653]: ??:0(handle_fatal_signal)[0x5613032fbc55]
Mar 24 14:08:01 anel mariadbd[18653]: sigaction.c:0(__restore_rt)[0x7f4ea65a7420]
Mar 24 14:08:01 anel mariadbd[19078]: addr2line: DWARF error: section .debug_info is larger than its filesize! (0x93ef57 vs 0x530ea0)
Mar 24 14:08:01 anel mariadbd[18653]: ??:0(__poll)[0x7f4ea617a99f]
Mar 24 14:08:01 anel mariadbd[18653]: ??:0(handle_connections_sockets())[0x561302fee35a]
Mar 24 14:08:01 anel mariadbd[18653]: ??:0(mysqld_main(int, char**))[0x561302feee96]
Mar 24 14:08:01 anel mariadbd[19080]: addr2line: DWARF error: section .debug_info is larger than its filesize! (0x93ef57 vs 0x530ea0)
Mar 24 14:08:01 anel mariadbd[18653]: ??:0(__libc_start_main)[0x7f4ea608c083]
Mar 24 14:08:01 anel mariadbd[18653]: ??:0(_start)[0x561302fe383e]
Mar 24 14:08:01 anel mariadbd[18653]: The manual page at https://mariadb.com/kb/en/how-to-produce-a-full-stack-trace-for-mysqld/ contai>
Mar 24 14:08:01 anel mariadbd[18653]: information that should help you find out what is causing the crash.
Mar 24 14:08:01 anel mariadbd[18653]: Writing a core file...
Mar 24 14:08:01 anel mariadbd[18653]: Working directory at /var/lib/mysql
Mar 24 14:08:01 anel mariadbd[18653]: Resource Limits:
Mar 24 14:08:01 anel mariadbd[18653]: Limit                     Soft Limit           Hard Limit           Units
Mar 24 14:08:01 anel mariadbd[18653]: Max cpu time              unlimited            unlimited            seconds
Mar 24 14:08:01 anel mariadbd[18653]: Max file size             unlimited            unlimited            bytes
Mar 24 14:08:01 anel mariadbd[18653]: Max data size             unlimited            unlimited            bytes
Mar 24 14:08:01 anel mariadbd[18653]: Max stack size            8388608              unlimited            bytes
Mar 24 14:08:01 anel mariadbd[18653]: Max core file size        0                    unlimited            bytes
Mar 24 14:08:01 anel mariadbd[18653]: Max resident set          unlimited            unlimited            bytes
Mar 24 14:08:01 anel mariadbd[18653]: Max processes             127694               127694               processes
Mar 24 14:08:01 anel mariadbd[18653]: Max open files            32768                32768                files
Mar 24 14:08:01 anel mariadbd[18653]: Max locked memory         65536                65536                bytes
Mar 24 14:08:01 anel mariadbd[18653]: Max address space         unlimited            unlimited            bytes
Mar 24 14:08:01 anel mariadbd[18653]: Max file locks            unlimited            unlimited            locks
Mar 24 14:08:01 anel mariadbd[18653]: Max pending signals       127694               127694               signals
Mar 24 14:08:01 anel mariadbd[18653]: Max msgqueue size         819200               819200               bytes
Mar 24 14:08:01 anel mariadbd[18653]: Max nice priority         0                    0
Mar 24 14:08:01 anel mariadbd[18653]: Max realtime priority     0                    0
Mar 24 14:08:01 anel mariadbd[18653]: Max realtime timeout      unlimited            unlimited            us
Mar 24 14:08:01 anel mariadbd[18653]: Core pattern: |/usr/share/apport/apport -p%p -s%s -c%c -d%d -P%P -u%u -g%g -- %E
Mar 24 14:08:01 anel mariadbd[18653]: Kernel version: Linux version 5.15.0-67-generic (buildd@lcy02-amd64-029) (gcc (Ubuntu 9.4.0-1ubun>
Mar 24 14:08:03 anel systemd[1]: mariadb.service: Main process exited, code=dumped, status=11/SEGV
Mar 24 14:08:03 anel systemd[1]: mariadb.service: Failed with result 'core-dump'.
```
#### Check options
```bash
$ which my_print_defaults 
/usr/bin/my_print_defaults
$ dpkg -S /usr/bin/my_print_defaults 
mariadb-client-core-10.6: /usr/bin/my_print_defaults
$ my_print_defaults --mysqld
--socket=/run/mysqld/mysqld.sock
--pid-file=/run/mysqld/mysqld.pid
--basedir=/usr
--bind-address=127.0.0.1
--expire_logs_days=10
--character-set-server=utf8mb4
--collation-server=utf8mb4_general_ci
```
### Enable core files


- Regarding [MDEV-20738](https://jira.mariadb.org/browse/MDEV-20738),
with binutils 2.34.6 (ubuntu 20.04)
```bash
$ ld -v
GNU ld (GNU Binutils for Ubuntu) 2.34
$ dpkg -l|grep binutils
ii  binutils                                     2.34-6ubuntu1.4                      amd64        GNU assembler, linker and binary utilities
ii  binutils-common:amd64                        2.34-6ubuntu1.4                      amd64        Common files for the GNU assembler, linker and binary utilities
ii  binutils-x86-64-linux-gnu                    2.34-6ubuntu1.4                      amd64        GNU binary utilities, for x86-64-linux-gnu target
ii  libbinutils:amd64                            2.34-6ubuntu1.4                      amd64        GNU binary utilities (private shared library)
```
based on [this](https://bugs.launchpad.net/ubuntu/+source/binutils/+bug/1977958) it should be temporary fix.
- However 22.04 fixes by increasing size 10x in `binutils 2.38`, but is not added backport.
### Test binutils 2.34.6


## Simple performance lock analysis tool (splat) for Linux IBM
From https://unix.stackexchange.com/questions/643117/thread-profiling-and-monitoring
https://developer.ibm.com/articles/introducing-linux-splat/
https://github.com/open-power-sdk/splat
[IBM articles](https://developer.ibm.com/technologies/linux/articles/)

