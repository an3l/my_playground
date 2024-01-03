# MDEV-30432 - Remove cpprestsdk from ConnectSE
https://jira.mariadb.org/browse/MDEV-30432

## Older conversation:
- I have tried before [test](https://mariadb.zulipchat.com/#narrow/stream/118758-MariaDB-Foundation-Staff/topic/Connect.20SE.20-.20REST.20API)
- https://mariadb.zulipchat.com/#narrow/stream/118758-MariaDB-Foundation-Staff/topic/Debian.20packaging/near/322227565

Following https://jira.mariadb.org/browse/MDEV-24357
-> Rest library (enabled with `CONNECT_WITH_REST`) -> `GetRest.so` dynamically linked (can be removed)?
-> Statically linked ha_connect.so with libcpprest.a
'''

Allowing to compile a version of Connect statically linked to cpprestsdk was actually a temporary tool allowing to test REST on early versions of connect having no other mean to do it and should have been already removed.

Indeed, an engine module, such as Connect, must be loadable by all means and therefore, never be dependent on an external product. This was already true for Java and JBDC and must be also true for REST.

to use REST the way it is described in appendix 2 and see if you have any trouble when compiling the external GetRest.so lib on Ubuntu.
'''


# Connect REST

## Old document
- About cpprestsdk  and old version of MaraiDB (doesn't support REST)
https://mariadb.com/kb/en/connect-adding-the-rest-feature-as-a-library-called-by-an-oem-table/
- Files
tabrest.cpp, 
restget.cpp,  extern (uses `cpprest/` header) restGetFile, REST_SOURCE, RESTColumns, GetRestFunction
tabrest.h and 
mini-global.h 
+ headers



https://mariadb.com/kb/en/connect-making-the-getrest-library/

### CMake variables
`REST_SOURCE` < dodao u CMakeLists -DREST_SOURCE - koristi u 
`CONNECT_WITH_REST` < dodao cpp

## New document
https://mariadb.com/kb/en/connect-files-retrieved-using-rest-queries/

# Current rest
Works fine, without having linkage
```
l$ ldd ./storage/connect/ha_connect.so 
	linux-vdso.so.1 (0x00007ffcac4f4000)
	libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f3aef387000)
	libxml2.so.2 => /lib/x86_64-linux-gnu/libxml2.so.2 (0x00007f3aef1cd000)
	libodbc.so.2 => /lib/x86_64-linux-gnu/libodbc.so.2 (0x00007f3aef15b000)
	libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f3aeef79000)
	libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f3aeee2a000)
	libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f3aeee0f000)
	libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f3aeedea000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f3aeebf8000)
	libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f3aeebf2000)
	libicuuc.so.66 => /lib/x86_64-linux-gnu/libicuuc.so.66 (0x00007f3aeea0c000)
	liblzma.so.5 => /lib/x86_64-linux-gnu/liblzma.so.5 (0x00007f3aee9e3000)
	libltdl.so.7 => /lib/x86_64-linux-gnu/libltdl.so.7 (0x00007f3aee9d8000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f3aef609000)
	libicudata.so.66 => /lib/x86_64-linux-gnu/libicudata.so.66 (0x00007f3aecf15000)

```
Seems he used my patch 02bb11709d7b to record the test case, although it does work even without this.
There is installed curl (3 packages)
```
$ dpkg --get-selections |grep curl
curl						install
libcurl3-gnutls:amd64				install
libcurl4:amd64					install
libcurl4-openssl-dev:amd64			install


$ dpkg -L libcurl4
/.
/usr
/usr/lib
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/libcurl.so.4.6.0
/usr/share
/usr/share/doc
/usr/share/doc/libcurl4
/usr/share/doc/libcurl4/NEWS.Debian.gz
/usr/share/doc/libcurl4/changelog.Debian.gz
/usr/share/doc/libcurl4/copyright
/usr/lib/x86_64-linux-gnu/libcurl.so.4

$ dpkg -L libcurl4-openssl-dev 
/.
/usr
/usr/bin
/usr/bin/curl-config
/usr/include
/usr/include/x86_64-linux-gnu
/usr/include/x86_64-linux-gnu/curl
/usr/include/x86_64-linux-gnu/curl/curl.h
/usr/include/x86_64-linux-gnu/curl/curlver.h
/usr/include/x86_64-linux-gnu/curl/easy.h
/usr/include/x86_64-linux-gnu/curl/mprintf.h
/usr/include/x86_64-linux-gnu/curl/multi.h
/usr/include/x86_64-linux-gnu/curl/stdcheaders.h
/usr/include/x86_64-linux-gnu/curl/system.h
/usr/include/x86_64-linux-gnu/curl/typecheck-gcc.h
/usr/include/x86_64-linux-gnu/curl/urlapi.h
/usr/lib
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/libcurl.a
/usr/lib/x86_64-linux-gnu/libcurl.la
/usr/lib/x86_64-linux-gnu/pkgconfig
/usr/lib/x86_64-linux-gnu/pkgconfig/libcurl.pc
/usr/share
/usr/share/aclocal
/usr/share/aclocal/libcurl.m4
/usr/share/doc
/usr/share/doc/libcurl4-openssl-dev
/usr/share/doc/libcurl4-openssl-dev/copyright
/usr/share/man
/usr/share/man/man1
/usr/share/man/man1/curl-config.1.gz
/usr/lib/x86_64-linux-gnu/libcurl.so
/usr/share/doc/libcurl4-openssl-dev/NEWS.Debian.gz
/usr/share/doc/libcurl4-openssl-dev/changelog.Debian.gz


$ dpkg -L libcurl3-gnutls
/.
/usr
/usr/lib
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/libcurl-gnutls.so.4.6.0
/usr/share
/usr/share/doc
/usr/share/doc/libcurl3-gnutls
/usr/share/doc/libcurl3-gnutls/NEWS.Debian.gz
/usr/share/doc/libcurl3-gnutls/changelog.Debian.gz
/usr/share/doc/libcurl3-gnutls/copyright
/usr/share/lintian
/usr/share/lintian/overrides
/usr/share/lintian/overrides/libcurl3-gnutls
/usr/lib/x86_64-linux-gnu/libcurl-gnutls.so.3
/usr/lib/x86_64-linux-gnu/libcurl-gnutls.so.4


$ dpkg -L curl
/.
/usr
/usr/bin
/usr/bin/curl

```

- Remove curl
```
sudo apt remove curl
```
- Error (tabrest.cpp)
```
#
# Testing REST query
#
CREATE TABLE t1
ENGINE=CONNECT DATA_CHARSET=utf8 TABLE_TYPE=JSON FILE_NAME='users.json'
HTTP='http://jsonplaceholder.typicode.com/users';
connect.anel                             [ fail ]
        Test ended at 2023-12-29 10:22:00

CURRENT_TEST: connect.anel
mysqltest: At line 4: query 'CREATE TABLE t1
ENGINE=CONNECT DATA_CHARSET=utf8 TABLE_TYPE=JSON FILE_NAME='users.json'
HTTP='http://jsonplaceholder.typicode.com/users'' failed: ER_UNKNOWN_ERROR (1105): Cannot access to curl nor casablanca

 - saving '/home/anel/GitHub/mariadb/server/build/11.4-connect-curl/mysql-test/var/log/connect.anel/' to '/home/anel/GitHub/mariadb/server/build/11.4-connect-curl/mysql-test/var/log/connect.anel/'
 
$ readelf -a storage/connect/ha_connect.so |grep curl
  2918: 00000000001cf2bc   919 FUNC    LOCAL  DEFAULT   14 _ZL5XcurlP7_globalPKcS2_S

```

- With patch
```
CREATE TABLE t1
ENGINE=CONNECT DATA_CHARSET=utf8 TABLE_TYPE=JSON FILE_NAME='users.json'
HTTP='http://jsonplaceholder.typicode.com/users';
connect.anel                             [ fail ]
        Test ended at 2023-12-29 10:43:44

CURRENT_TEST: connect.anel
mysqltest: At line 4: query 'CREATE TABLE t1
ENGINE=CONNECT DATA_CHARSET=utf8 TABLE_TYPE=JSON FILE_NAME='users.json'
HTTP='http://jsonplaceholder.typicode.com/users'' failed: ER_UNKNOWN_ERROR (1105): Cannot access to curl.

```

- Check how `curl` is used
```
$ grep -R "#include <curl/curl.h>" ./

```

- See:
  `./storage/columnstore/columnstore/dbcon/mysql/columnstore_dataload.cpp`
  `./plugin/hashicorp_key_management/hashicorp_key_management_plugin.cc`
  
### Mastering culr with Daniel Stenberg
Generic
https://www.youtube.com/watch?v=V5vZWHP-RqU
8.4.0
https://www.youtube.com/watch?v=-j-_nKmq2aE
https://www.youtube.com/watch?v=xZpyXA9_7qg

- Learn more about curl API
  - Libcurl under the hood < nauci
    https://www.youtube.com/watch?v=T7Pv5lQ1dAc
  - mastering libcurl
    https://www.youtube.com/watch?v=ZQXv5v9xocU



## REST update: Forking the new process 

Using vfork() : man vfork
How to see the version of glibc:
```
$ ldd --version
ldd (Ubuntu GLIBC 2.27-3ubuntu1.4) 2.27

$ /lib/x86_64-linux-gnu/libc.so.6 --version
GNU C Library (Ubuntu GLIBC 2.27-3ubuntu1.4) stable release version 2.27.
```

Simple work with curl:
```C
int main(int argc, char const *argv[])
{
  pid_t pid;
  //Testing the command: curl https://google.com -o "anel.txt" - doesn't work because of https - curl reported
  //Testing the commoand curl www.google.com -o "anel.txt"

  const char *filename="anel-curl.txt"; // it has to be enclosed with "  - why?
  char link[512]="www.google.com";
  // child process
  if (!(pid= vfork()))
  {
    printf("PID: %d, hi from child\n", pid);
    execl("/usr/bin/curl","--url", link, "-o", filename, NULL);
    printf("I_will_not_be_executed!");
  }
  else
  {
    // parent waiting to finish
    wait(NULL);
    printf("PID: %d, hi from parent\n", pid);
  }
  return 0;
}

```


Working with curl and dynamic linking

Used in s3:  /home/anel/mariadb/10.5/storage/maria/libmarias3
And mariabackup: extra/mariabackup/xbcloud.cc
WITH_CURL: libmariadb/CMakeLists.txt

Working with cmake

```
# libcurl3-gnutls  /usr/lib/x86_64-linux-gnu/libcurl-gnutls.so.3
# libcurl4             /usr/lib/x86_64-linux-gnu/libcurl.so
# libcurl4-openssl-dev  /usr/lib/x86_64-linux-gnu/libcurl.so.4

$ ls -la /usr/lib/x86_64-linux-gnu/ |grep libcurl
-rw-r--r--   1 root root  1058664 Dec  1 19:01 libcurl.a
lrwxrwxrwx   1 root root       19 Dec  1 19:01 libcurl-gnutls.so.3 -> libcurl-gnutls.so.4
lrwxrwxrwx   1 root root       23 Dec  1 19:01 libcurl-gnutls.so.4 -> libcurl-gnutls.so.4.5.0
-rw-r--r--   1 root root   510408 Dec  1 19:01 libcurl-gnutls.so.4.5.0
-rw-r--r--   1 root root      951 Dec  1 19:01 libcurl.la
lrwxrwxrwx   1 root root       16 Dec  1 19:01 libcurl.so -> libcurl.so.4.5.0
lrwxrwxrwx   1 root root       16 Dec  1 19:01 libcurl.so.4 -> libcurl.so.4.5.0
-rw-r--r--   1 root root   518600 Dec  1 19:01 libcurl.so.4.5.0
```

```

errno -l # install moreutils

EPERM 1 Operation not permitted
ENOENT 2 No such file or directory
ESRCH 3 No such process
..
```

# Remove libcurl
```
$ sudo apt remove libcurl4-openssl-dev
$ cmake --build . --target connect
[  0%] Built target uca-dump
[  8%] Built target mysqlservices
[  8%] Built target GenUnicodeDataSource
[ 58%] Built target mysys
[ 75%] Built target strings
[ 75%] Built target dbug
[ 75%] Built target comp_err
[ 75%] Built target GenError
make[3]: *** No rule to make target '/usr/lib/x86_64-linux-gnu/libcurl.so', needed by 'storage/connect/ha_connect.so'.  Stop.
make[3]: *** Waiting for unfinished jobs....
[ 75%] Building CXX object storage/connect/CMakeFiles/connect.dir/tabrest.cpp.o
/home/anel/GitHub/mariadb/server/src/connect-curl-11.4/storage/connect/tabrest.cpp:39:10: fatal error: curl/curl.h: No such file or directory
   39 | #include <curl/curl.h>
      |          ^~~~~~~~~~~~~
compilation terminated.

```


Testing package and docker image
```bash
$ docker run -it --rm --name maria-replication -v/home/anel/GitHub/mariadb/server/src/connect-curl-11.4:/code/ debian-11 bash


buildbot@0013f8b295b9:/$ dpkg --contents mariadb-plugin-connect_11.4.0+maria~deb11_amd64.deb
drwxr-xr-x root/root         0 2024-01-03 13:09 ./
drwxr-xr-x root/root         0 2024-01-03 13:09 ./etc/
drwxr-xr-x root/root         0 2024-01-03 13:09 ./etc/mysql/
drwxr-xr-x root/root         0 2024-01-03 13:09 ./etc/mysql/mariadb.conf.d/
-rw-r--r-- root/root        40 2024-01-03 13:09 ./etc/mysql/mariadb.conf.d/connect.cnf
drwxr-xr-x root/root         0 2024-01-03 13:09 ./usr/
drwxr-xr-x root/root         0 2024-01-03 13:09 ./usr/lib/
drwxr-xr-x root/root         0 2024-01-03 13:09 ./usr/lib/mysql/
drwxr-xr-x root/root         0 2024-01-03 13:09 ./usr/lib/mysql/plugin/
-rw-r--r-- root/root   1917600 2024-01-03 13:09 ./usr/lib/mysql/plugin/ha_connect.so
drwxr-xr-x root/root         0 2024-01-03 13:09 ./usr/share/
drwxr-xr-x root/root         0 2024-01-03 13:09 ./usr/share/doc/
drwxr-xr-x root/root         0 2024-01-03 13:09 ./usr/share/doc/mariadb-plugin-connect/
-rw-r--r-- root/root       253 2024-01-03 13:09 ./usr/share/doc/mariadb-plugin-connect/changelog.gz
-rw-r--r-- root/root      2493 2023-12-29 08:01 ./usr/share/doc/mariadb-plugin-connect/copyright


$ dpkg --info mariadb-plugin-connect_11.4.0+maria~deb11_amd64.deb
 new Debian package, version 2.0.
 size 559616 bytes: control archive=908 bytes.
      38 bytes,     1 lines      conffiles            
    1178 bytes,    19 lines      control              
     234 bytes,     3 lines      md5sums              
 Package: mariadb-plugin-connect
 Source: mariadb
 Version: 1:11.4.0+maria~deb11
 Architecture: amd64
 Maintainer: MariaDB Developers <developers@lists.mariadb.org>
 Installed-Size: 1891
 Depends: libxml2 (>= 2.7.4), mariadb-server (= 1:11.4.0+maria~deb11), unixodbc, libc6 (>= 2.29), libcurl4 (>= 7.16.2), libodbc1 (>= 2.3.1), libstdc++6 (>= 4.1.1), zlib1g (>= 1:1.2.3.4)
 
 $ dpkg-deb -I  mariadb-plugin-connect_11.4.0+maria~deb11_amd64.deb|grep Dep
 Depends: libxml2 (>= 2.7.4), mariadb-server (= 1:11.4.0+maria~deb11), unixodbc, libc6 (>= 2.29), libcurl4 (>= 7.16.2), libodbc1 (>= 2.3.1), libstdc++6 (>= 4.1.1), zlib1g (>= 1:1.2.3.4)


# Extract library and check curl dependency
$ sudo dpkg-deb -x mariadb-plugin-connect_11.4.0+maria~deb11_amd64.deb test-ha-connect
$ ldd test-ha-connect/usr/lib/mysql/plugin/ha_connect.so |grep curl
	libcurl.so.4 => /usr/lib/x86_64-linux-gnu/libcurl.so.4 (0x00007fd41c88d000)


# Install package
$ sudo dpkg -i mariadb-plugin-connect_11.4.0+maria~deb11_amd64.deb
Selecting previously unselected package mariadb-plugin-connect.
(Reading database ... 57799 files and directories currently installed.)
Preparing to unpack mariadb-plugin-connect_11.4.0+maria~deb11_amd64.deb ...
Unpacking mariadb-plugin-connect (1:11.4.0+maria~deb11) ...
dpkg: dependency problems prevent configuration of mariadb-plugin-connect:
 mariadb-plugin-connect depends on mariadb-server (= 1:11.4.0+maria~deb11); however:
  Package mariadb-server is not installed.
 mariadb-plugin-connect depends on unixodbc; however:
  Package unixodbc is not installed.

dpkg: error processing package mariadb-plugin-connect (--install):
 dependency problems - leaving unconfigured
Errors were encountered while processing:
 mariadb-plugin-connect


$ sudo apt install mariadb-server unixodbc
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
You might want to run 'apt --fix-broken install' to correct these.
The following packages have unmet dependencies:
 mariadb-plugin-connect : Depends: mariadb-server (= 1:11.4.0+maria~deb11) but 1:10.5.21-0+deb11u1 is to be installed
 mariadb-server : Depends: mariadb-server-10.5 (>= 1:10.5.21-0+deb11u1) but it is not going to be installed
E: Unmet dependencies. Try 'apt --fix-broken install' with no packages (or specify a solution).


# Install from .deb packages
# mariadb-server_11.4.0+maria~deb11_amd64.deb
dpkg -i mariadb-server_11.4.0+maria~deb11_amd64.deb
dpkg: error: requested operation requires superuser privilege
$ sudo dpkg -i mariadb-server_11.4.0+maria~deb11_amd64.deb
Selecting previously unselected package mariadb-server.
dpkg: regarding mariadb-server_11.4.0+maria~deb11_amd64.deb containing mariadb-server, pre-dependency problem:
 mariadb-server pre-depends on mariadb-common (>= 1:11.4.0+maria~deb11)
  mariadb-common is not installed.

# mariadb-common_11.4.0+maria~deb11_all.deb
$ sudo dpkg -i mariadb-common_11.4.0+maria~deb11_all.deb
Selecting previously unselected package mariadb-common.
(Reading database ... 57808 files and directories currently installed.)
Preparing to unpack mariadb-common_11.4.0+maria~deb11_all.deb ...
Unpacking mariadb-common (1:11.4.0+maria~deb11) ...
dpkg: dependency problems prevent configuration of mariadb-common:
 mariadb-common depends on mysql-common (>= 5.6.25); however:
  Package mysql-common is not installed.

# mysql-common_11.4.0+maria~deb11_all.deb
# 1)
$ sudo dpkg -i mysql-common_11.4.0+maria~deb11_all.deb
Selecting previously unselected package mysql-common.
(Reading database ... 57812 files and directories currently installed.)
Preparing to unpack mysql-common_11.4.0+maria~deb11_all.deb ...
Unpacking mysql-common (1:11.4.0+maria~deb11) ...
Setting up mysql-common (1:11.4.0+maria~deb11) ...

# Vrati se unazad
# 2) 
sudo dpkg -i mariadb-common_11.4.0+maria~deb11_all.deb
(Reading database ... 57817 files and directories currently installed.)
Preparing to unpack mariadb-common_11.4.0+maria~deb11_all.deb ...
Unpacking mariadb-common (1:11.4.0+maria~deb11) over (1:11.4.0+maria~deb11) ...
Setting up mariadb-common (1:11.4.0+maria~deb11) ...
update-alternatives: error: no alternatives for my.cnf
update-alternatives: using /etc/mysql/mariadb.cnf to provide /etc/mysql/my.cnf (my.cnf) in auto mod

# 3)
$ sudo dpkg -i mariadb-server_11.4.0+maria~deb11_amd64.deb
(Reading database ... 57817 files and directories currently installed.)
Preparing to unpack mariadb-server_11.4.0+maria~deb11_amd64.deb ...
debconf: unable to initialize frontend: Dialog
debconf: (No usable dialog-like program is installed, so the dialog based frontend cannot be used. at /usr/share/perl5/Debconf/FrontEnd/Dialog.pm line 78.)
debconf: falling back to frontend: Readline
Unpacking mariadb-server (1:11.4.0+maria~deb11) ...
dpkg: dependency problems prevent configuration of mariadb-server:
 mariadb-server depends on galera-4 (>= 26.4); however:
  Package galera-4 is not installed.
 mariadb-server depends on iproute2; however:
  Package iproute2 is not installed.
 mariadb-server depends on libdbi-perl; however:
  Package libdbi-perl is not installed.
 mariadb-server depends on lsof; however:
  Package lsof is not installed.
 mariadb-server depends on mariadb-client (>= 1:11.4.0+maria~deb11); however:
  Package mariadb-client is not installed.
 mariadb-server depends on mariadb-server-core (>= 1:11.4.0+maria~deb11); however:
  Package mariadb-server-core is not installed.
 mariadb-server depends on rsync; however:
  Package rsync is not installed.
 mariadb-server depends on socat; however:
  Package socat is not installed.
  
  
$ sudo apt-get install software-properties-common  
 mariadb-plugin-connect : Depends: unixodbc but it is not going to be installed
 mariadb-server : Depends: galera-4 (>= 26.4) but it is not going to be installed
                  Depends: iproute2 but it is not going to be installed
                  Depends: libdbi-perl but it is not going to be installed
                  Depends: lsof but it is not going to be installed
                  Depends: mariadb-client (>= 1:11.4.0+maria~deb11) but it is not going to be installed
                  Depends: mariadb-server-core (>= 1:11.4.0+maria~deb11) but it is not installable
                  Depends: rsync but it is not going to be installed
                  Depends: socat but it is not going to be installed
                  
# Pre 3)  -A)  mariadb-server-core_11.4.0+maria~deb11_amd64.deb
$ sudo dpkg -i mariadb-server-core_11.4.0+maria~deb11_amd64.deb
Selecting previously unselected package mariadb-server-core.
(Reading database ... 57917 files and directories currently installed.)
Preparing to unpack mariadb-server-core_11.4.0+maria~deb11_amd64.deb ...
Unpacking mariadb-server-core (1:11.4.0+maria~deb11) ...
Setting up mariadb-server-core (1:11.4.0+maria~deb11) ...
Processing triggers for man-db (2.9.4-2) ...


# Pre 3) - B)  mariadb-client_11.4.0+maria~deb11_amd64.deb
$ sudo dpkg -i mariadb-client_11.4.0+maria~deb11_amd64.deb
Selecting previously unselected package mariadb-client.
(Reading database ... 58021 files and directories currently installed.)
Preparing to unpack mariadb-client_11.4.0+maria~deb11_amd64.deb ...
Unpacking mariadb-client (1:11.4.0+maria~deb11) ...
dpkg: dependency problems prevent configuration of mariadb-client:
 mariadb-client depends on libconfig-inifiles-perl; however:
  Package libconfig-inifiles-perl is not installed.
 mariadb-client depends on mariadb-client-core (>= 1:11.4.0+maria~deb11); however:
  Package mariadb-client-core is not installed.

dpkg: error processing package mariadb-client (--install):
 dependency problems - leaving unconfigured
Processing triggers for man-db (2.9.4-2) ...
Errors were encountered while processing:
 mariadb-client


# Pre 3) - Pre B)  B.1 mariadb-client-core_11.4.0+maria~deb11_amd64.deb
$ sudo dpkg -i mariadb-client-core_11.4.0+maria~deb11_amd64.deb
Selecting previously unselected package mariadb-client-core.
(Reading database ... 58089 files and directories currently installed.)
Preparing to unpack mariadb-client-core_11.4.0+maria~deb11_amd64.deb ...
Unpacking mariadb-client-core (1:11.4.0+maria~deb11) ...
dpkg: dependency problems prevent configuration of mariadb-client-core:
 mariadb-client-core depends on libmariadb3 (>= 10.5.4); however:
  Package libmariadb3 is not installed.

dpkg: error processing package mariadb-client-core (--install):
 dependency problems - leaving unconfigured
Processing triggers for man-db (2.9.4-2) ...
Errors were encountered while processing:
 mariadb-client-core
 

# Pre 3) - Pre B)  B.2 libmariadb3_11.4.0+maria~deb11_amd64.deb
$ sudo dpkg -i libmariadb3_11.4.0+maria~deb11_amd64.deb
Selecting previously unselected package libmariadb3:amd64.
(Reading database ... 58098 files and directories currently installed.)
Preparing to unpack libmariadb3_11.4.0+maria~deb11_amd64.deb ...
Unpacking libmariadb3:amd64 (1:11.4.0+maria~deb11) ...
Setting up libmariadb3:amd64 (1:11.4.0+maria~deb11) ...
Processing triggers for libc-bin (2.31-13+deb11u7) ...
# Vrati se na B.1 -  radi
$ sudo dpkg -i mariadb-client-core_11.4.0+maria~deb11_amd64.deb
(Reading database ... 58109 files and directories currently installed.)
Preparing to unpack mariadb-client-core_11.4.0+maria~deb11_amd64.deb ...
Unpacking mariadb-client-core (1:11.4.0+maria~deb11) over (1:11.4.0+maria~deb11) ...
Setting up mariadb-client-core (1:11.4.0+maria~deb11) ...
Processing triggers for man-db (2.9.4-2) ...


# Before B.1
$ sudo apt --fix-broken install
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Correcting dependencies... Done
The following additional packages will be installed:
  galera-4 iproute2 libatm1 libbpf0 libconfig-inifiles-perl libdbi-perl libmnl0 libpopt0 libwrap0 libxtables12 lsof rsync socat unixodbc
Suggested packages:
  iproute2-doc libmldbm-perl libnet-daemon-perl libsql-statement-perl openssh-server
The following NEW packages will be installed:
  galera-4 iproute2 libatm1 libbpf0 libconfig-inifiles-perl libdbi-perl libmnl0 libpopt0 libwrap0 libxtables12 lsof rsync socat unixodbc

```

Final command
```bash
sudo apt install galera-4 iproute2 libatm1 libbpf0 libconfig-inifiles-perl libdbi-perl libmnl0 libpopt0 libwrap0 libxtables12 lsof rsync socat unixodbc &&
sudo dpkg -i mysql-common_11.4.0+maria~deb11_all.deb && 
sudo dpkg -i mariadb-common_11.4.0+maria~deb11_all.deb &&
sudo dpkg -i libmariadb3_11.4.0+maria~deb11_amd64.deb && 
sudo dpkg -i mariadb-client-core_11.4.0+maria~deb11_amd64.deb && 
sudo dpkg -i mariadb-client_11.4.0+maria~deb11_amd64.deb && 
sudo dpkg -i mariadb-server-core_11.4.0+maria~deb11_amd64.deb &&
sudo dpkg -i mariadb-server_11.4.0+maria~deb11_amd64.deb

$ dpkg -S mariadbd
mariadb-server: /usr/bin/mariadbd-multi
mariadb-server: /usr/bin/mariadbd-safe-helper
mariadb-server-core: /usr/share/man/man8/mariadbd.8.gz
mariadb-server: /usr/share/doc/mariadb-server/mariadbd.sym.gz
mariadb-server: /usr/bin/mariadbd-safe
mariadb-server: /usr/share/man/man1/mariadbd-multi.1.gz
mariadb-server-core: /usr/sbin/mariadbd
mariadb-server: /usr/share/man/man1/mariadbd-safe.1.gz
mariadb-server: /usr/share/man/man1/mariadbd-safe-helper.1.gz
mariadb-server: /etc/apparmor.d/usr.sbin.mariadbd

```
- Started as root fails
```
$ sudo ./usr/sbin/mariadbd --user root
2024-01-03 14:37:00 0 [Note] Starting MariaDB 11.4.0-MariaDB-1:11.4.0+maria~deb11 source revision  as process 188485
2024-01-03 14:37:01 0 [Note] CONNECT: Version 1.07.0002 March 22, 2021
2024-01-03 14:37:01 0 [Note] InnoDB: Compressed tables use zlib 1.2.11
2024-01-03 14:37:01 0 [Note] InnoDB: Number of transaction pools: 1
2024-01-03 14:37:01 0 [Note] InnoDB: Using crc32 + pclmulqdq instructions
2024-01-03 14:37:01 0 [Note] mariadbd: O_TMPFILE is not supported on /tmp (disabling future attempts)
2024-01-03 14:37:01 0 [Note] InnoDB: Initializing buffer pool, total size = 128.000MiB, chunk size = 2.000MiB
2024-01-03 14:37:01 0 [Note] InnoDB: Completed initialization of buffer pool
2024-01-03 14:37:01 0 [Note] InnoDB: Buffered log writes (block size=512 bytes)
2024-01-03 14:37:01 0 [Note] InnoDB: End of log at LSN=47763
2024-01-03 14:37:01 0 [Note] InnoDB: Opened 3 undo tablespaces
2024-01-03 14:37:01 0 [Note] InnoDB: 128 rollback segments in 3 undo tablespaces are active.
2024-01-03 14:37:01 0 [Note] InnoDB: Setting file './ibtmp1' size to 12.000MiB. Physically writing the file full; Please wait ...
2024-01-03 14:37:01 0 [Note] InnoDB: File './ibtmp1' size is now 12.000MiB.
2024-01-03 14:37:01 0 [Note] InnoDB: log sequence number 47763; transaction id 14
2024-01-03 14:37:01 0 [Note] InnoDB: Loading buffer pool(s) from /var/lib/mysql/ib_buffer_pool
2024-01-03 14:37:01 0 [Note] Plugin 'FEEDBACK' is disabled.
2024-01-03 14:37:01 0 [Note] Plugin 'wsrep-provider' is disabled.
2024-01-03 14:37:01 0 [Note] InnoDB: Buffer pool(s) load completed at 240103 14:37:01
2024-01-03 14:37:01 0 [Note] Server socket created on IP: '127.0.0.1'.
2024-01-03 14:37:01 0 [ERROR] Can't start server : Bind on unix socket: No such file or directory
2024-01-03 14:37:01 0 [ERROR] Do you already have another server running on socket: /run/mysqld/mysqld.sock ?
2024-01-03 14:37:01 0 [ERROR] Aborting
```


- Fix: `buildbot@0013f8b295b9:/$ sudo mkdir /run/mysqld`
- Works
```
buildbot@0013f8b295b9:/$ sudo ./usr/sbin/mariadbd --user root
2024-01-03 14:37:44 0 [Note] Starting MariaDB 11.4.0-MariaDB-1:11.4.0+maria~deb11 source revision  as process 188500
2024-01-03 14:37:44 0 [Note] CONNECT: Version 1.07.0002 March 22, 2021
2024-01-03 14:37:44 0 [Note] InnoDB: Compressed tables use zlib 1.2.11
2024-01-03 14:37:44 0 [Note] InnoDB: Number of transaction pools: 1
2024-01-03 14:37:44 0 [Note] InnoDB: Using crc32 + pclmulqdq instructions
2024-01-03 14:37:44 0 [Note] mariadbd: O_TMPFILE is not supported on /tmp (disabling future attempts)
2024-01-03 14:37:44 0 [Note] InnoDB: Initializing buffer pool, total size = 128.000MiB, chunk size = 2.000MiB
2024-01-03 14:37:44 0 [Note] InnoDB: Completed initialization of buffer pool
2024-01-03 14:37:44 0 [Note] InnoDB: Buffered log writes (block size=512 bytes)
2024-01-03 14:37:44 0 [Note] InnoDB: End of log at LSN=47763
2024-01-03 14:37:44 0 [Note] InnoDB: Opened 3 undo tablespaces
2024-01-03 14:37:44 0 [Note] InnoDB: 128 rollback segments in 3 undo tablespaces are active.
2024-01-03 14:37:44 0 [Note] InnoDB: Setting file './ibtmp1' size to 12.000MiB. Physically writing the file full; Please wait ...
2024-01-03 14:37:44 0 [Note] InnoDB: File './ibtmp1' size is now 12.000MiB.
2024-01-03 14:37:44 0 [Note] InnoDB: log sequence number 47763; transaction id 14
2024-01-03 14:37:44 0 [Note] Plugin 'FEEDBACK' is disabled.
2024-01-03 14:37:44 0 [Note] Plugin 'wsrep-provider' is disabled.
2024-01-03 14:37:44 0 [Note] InnoDB: Loading buffer pool(s) from /var/lib/mysql/ib_buffer_pool
2024-01-03 14:37:44 0 [Note] InnoDB: Buffer pool(s) load completed at 240103 14:37:44
2024-01-03 14:37:44 0 [Note] Server socket created on IP: '127.0.0.1'.
2024-01-03 14:37:44 0 [Note] mariadbd: Event Scheduler: Loaded 0 events
2024-01-03 14:37:44 0 [Note] ./usr/sbin/mariadbd: ready for connections.
Version: '11.4.0-MariaDB-1:11.4.0+maria~deb11'  socket: '/run/mysqld/mysqld.sock'  port: 3306  mariadb.org binary distribution
```

- Testing in container
```
buildbot@0013f8b295b9:/$ sudo mariadb --user root
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 5
Server version: 11.4.0-MariaDB-1:11.4.0+maria~deb11 mariadb.org binary distribution
MariaDB [test]> create table cusers3 engine=connect http='http://jsonplaceholder.typicode.com/users' table_type=json;
Query OK, 0 rows affected, 1 warning (0.179 sec)

MariaDB [test]> select * from cusers3;
+----+--------------------------+------------------+---------------------------+-------------------+---------------+----------------+-----------------+-----------------+-----------------+-----------------------+---------------+--------------------+------------------------------------------+--------------------------------------+
| id | name                     | username         | email                     | address_street    | address_suite | address_city   | address_zipcode | address_geo_lat | address_geo_lng | phone                 | website       | company_name       | company_catchPhrase                      | company_bs                           |
+----+--------------------------+------------------+---------------------------+-------------------+---------------+----------------+-----------------+-----------------+-----------------+-----------------------+---------------+--------------------+------------------------------------------+--------------------------------------+
|  1 | Leanne Graham            | Bret             | Sincere@april.biz         | Kulas Light       | Apt. 556      | Gwenborough    | 92998-3874      | -37.3159        | 81.1496         | 1-770-736-8031 x56442 | hildegard.org | Romaguera-Crona    | Multi-layered client-server neural-net   | harness real-time e-markets          |
|  2 | Ervin Howell             | Antonette        | Shanna@melissa.tv         | Victor Plains     | Suite 879     | Wisokyburgh    | 90566-7771      | -43.9509        | -34.4618        | 010-692-6593 x09125   | anastasia.net | Deckow-Crist       | Proactive didactic contingency           | synergize scalable supply-chains     |
|  3 | Clementine Bauch         | Samantha         | Nathan@yesenia.net        | Douglas Extension | Suite 847     | McKenziehaven  | 59590-4157      | -68.6102        | -47.0653        | 1-463-123-4447        | ramiro.info   | Romaguera-Jacobson | Face to face bifurcated interface        | e-enable strategic applications      |
|  4 | Patricia Lebsack         | Karianne         | Julianne.OConner@kory.org | Hoeger Mall       | Apt. 692      | South Elvis    | 53919-4257      | 29.4572         | -164.2990       | 493-170-9623 x156     | kale.biz      | Robel-Corkery      | Multi-tiered zero tolerance productivity | transition cutting-edge web services |
|  5 | Chelsey Dietrich         | Kamren           | Lucio_Hettinger@annie.ca  | Skiles Walks      | Suite 351     | Roscoeview     | 33263           | -31.8129        | 62.5342         | (254)954-1289         | demarco.info  | Keebler LLC        | User-centric fault-tolerant solution     | revolutionize end-to-end systems     |
|  6 | Mrs. Dennis Schulist     | Leopoldo_Corkery | Karley_Dach@jasper.info   | Norberto Crossing | Apt. 950      | South Christy  | 23505-1337      | -71.4197        | 71.7478         | 1-477-935-8478 x6430  | ola.org       | Considine-Lockman  | Synchronised bottom-line interface       | e-enable innovative applications     |
|  7 | Kurtis Weissnat          | Elwyn.Skiles     | Telly.Hoeger@billy.biz    | Rex Trail         | Suite 280     | Howemouth      | 58804-1099      | 24.8918         | 21.8984         | 210.067.6132          | elvis.io      | Johns Group        | Configurable multimedia task-force       | generate enterprise e-tailers        |
|  8 | Nicholas Runolfsdottir V | Maxime_Nienow    | Sherwood@rosamond.me      | Ellsworth Summit  | Suite 729     | Aliyaview      | 45169           | -14.3990        | -120.7677       | 586.493.6943 x140     | jacynthe.com  | Abernathy Group    | Implemented secondary concept            | e-enable extensible e-tailers        |
|  9 | Glenna Reichert          | Delphine         | Chaim_McDermott@dana.io   | Dayna Park        | Suite 449     | Bartholomebury | 76495-3109      | 24.6463         | -168.8889       | (775)976-6794 x41206  | conrad.com    | Yost and Sons      | Switchable contextually-based project    | aggregate real-time technologies     |
| 10 | Clementina DuBuque       | Moriah.Stanton   | Rey.Padberg@karina.biz    | Kattie Turnpike   | Suite 198     | Lebsackbury    | 31428-2261      | -38.2386        | 57.2232         | 024-648-3804          | ambrose.net   | Hoeger LLC         | Centralized empowering task-force        | target end-to-end models             |
+----+--------------------------+------------------+---------------------------+-------------------+---------------+----------------+-----------------+-----------------+-----------------+-----------------------+---------------+--------------------+------------------------------------------+--------------------------------------+
10 rows in set (0.126 sec)

```

Tested from different container
https://jira.mariadb.org/browse/MDEV-26727
```
$ docker exec -it connect-patch sudo mariadb -uroot -e "use test; create table cusers4 engine=connect http='http://jsonplaceholder.typicode.com/users' table_type=json; select * from cusers4;"
+----+--------------------------+------------------+---------------------------+-------------------+---------------+----------------+-----------------+-----------------+-----------------+-----------------------+---------------+--------------------+------------------------------------------+--------------------------------------+
| id | name                     | username         | email                     | address_street    | address_suite | address_city   | address_zipcode | address_geo_lat | address_geo_lng | phone                 | website       | company_name       | company_catchPhrase                      | company_bs                           |
+----+--------------------------+------------------+---------------------------+-------------------+---------------+----------------+-----------------+-----------------+-----------------+-----------------------+---------------+--------------------+------------------------------------------+--------------------------------------+
|  1 | Leanne Graham            | Bret             | Sincere@april.biz         | Kulas Light       | Apt. 556      | Gwenborough    | 92998-3874      | -37.3159        | 81.1496         | 1-770-736-8031 x56442 | hildegard.org | Romaguera-Crona    | Multi-layered client-server neural-net   | harness real-time e-markets          |
|  2 | Ervin Howell             | Antonette        | Shanna@melissa.tv         | Victor Plains     | Suite 879     | Wisokyburgh    | 90566-7771      | -43.9509        | -34.4618        | 010-692-6593 x09125   | anastasia.net | Deckow-Crist       | Proactive didactic contingency           | synergize scalable supply-chains     |
|  3 | Clementine Bauch         | Samantha         | Nathan@yesenia.net        | Douglas Extension | Suite 847     | McKenziehaven  | 59590-4157      | -68.6102        | -47.0653        | 1-463-123-4447        | ramiro.info   | Romaguera-Jacobson | Face to face bifurcated interface        | e-enable strategic applications      |
|  4 | Patricia Lebsack         | Karianne         | Julianne.OConner@kory.org | Hoeger Mall       | Apt. 692      | South Elvis    | 53919-4257      | 29.4572         | -164.2990       | 493-170-9623 x156     | kale.biz      | Robel-Corkery      | Multi-tiered zero tolerance productivity | transition cutting-edge web services |
|  5 | Chelsey Dietrich         | Kamren           | Lucio_Hettinger@annie.ca  | Skiles Walks      | Suite 351     | Roscoeview     | 33263           | -31.8129        | 62.5342         | (254)954-1289         | demarco.info  | Keebler LLC        | User-centric fault-tolerant solution     | revolutionize end-to-end systems     |
|  6 | Mrs. Dennis Schulist     | Leopoldo_Corkery | Karley_Dach@jasper.info   | Norberto Crossing | Apt. 950      | South Christy  | 23505-1337      | -71.4197        | 71.7478         | 1-477-935-8478 x6430  | ola.org       | Considine-Lockman  | Synchronised bottom-line interface       | e-enable innovative applications     |
|  7 | Kurtis Weissnat          | Elwyn.Skiles     | Telly.Hoeger@billy.biz    | Rex Trail         | Suite 280     | Howemouth      | 58804-1099      | 24.8918         | 21.8984         | 210.067.6132          | elvis.io      | Johns Group        | Configurable multimedia task-force       | generate enterprise e-tailers        |
|  8 | Nicholas Runolfsdottir V | Maxime_Nienow    | Sherwood@rosamond.me      | Ellsworth Summit  | Suite 729     | Aliyaview      | 45169           | -14.3990        | -120.7677       | 586.493.6943 x140     | jacynthe.com  | Abernathy Group    | Implemented secondary concept            | e-enable extensible e-tailers        |
|  9 | Glenna Reichert          | Delphine         | Chaim_McDermott@dana.io   | Dayna Park        | Suite 449     | Bartholomebury | 76495-3109      | 24.6463         | -168.8889       | (775)976-6794 x41206  | conrad.com    | Yost and Sons      | Switchable contextually-based project    | aggregate real-time technologies     |
| 10 | Clementina DuBuque       | Moriah.Stanton   | Rey.Padberg@karina.biz    | Kattie Turnpike   | Suite 198     | Lebsackbury    | 31428-2261      | -38.2386        | 57.2232         | 024-648-3804          | ambrose.net   | Hoeger LLC         | Centralized empowering task-force        | target end-to-end models             |
+----+--------------------------+------------------+---------------------------+-------------------+---------------+----------------+-----------------+-----------------+-----------------+-----------------------+---------------+--------------------+------------------------------------------+--------------------------------------+

```
