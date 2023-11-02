# MDEV-14448: Ctrl-C should not exit the client

Patch: https://github.com/MariaDB/server/commit/84c9cbc36b94bcf3f078c71953ce26535a0686f0

Windows should be: https://www.dpldocs.info/this-week-in-d/Blog.Posted_2019_11_25.html

# Test 1:Not long running query
1.1 Without the patch - client is aborted:
```
MariaDB [(none)]> Ctrl-C -- exit!
Aborted
```

1.2 With the patch - client is not aborted:
```
MariaDB [(none)]> ^C
MariaDB [(none)]> ^C
MariaDB [(none)]> ^C
MariaDB [(none)]> 
```

# Test 2: Slow running query
- Simulate long runnig query:
1. Add 1[s] delay to docker network using `tc`: 
```
$ tc qdisc show|grep docker
qdisc noqueue 0: dev docker0 root refcnt 2 
$ sudo tc qdisc add dev docker0 root netem delay 1000ms
$ tc qdisc show|grep docker
qdisc netem 8001: dev docker0 root refcnt 2 limit 1000 delay 1.0s
```
2. Start docker container and expose port
```
$ docker container run --rm -p=3307:3306 --name mariadb-server -e MYSQL_ROOT_PASSWORD=secret -d mariadb:latest
```
3. Start host client with exposed port
```
$ ./client/mysql -uroot -psecret -hlocalhost -P3307 --protocol=tcp

```
4. Check queries (takes about 1s)
```
MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (1.001 sec)
```

2.1 Without the patch:
For each case below run query and execute CTRL-C x n. Without the query it is the same as for case of normal query execution.
a) CTRL-C x 1 (+ any character after) (connection not lost on second query, for 3. query reconnected)
```
MariaDB [(none)]> show databases;
^CCtrl-C -- query killed. Continuing normally.
+--------------------+
| Database           |
+--------------------+
+--------------------+
4 rows in set (4.539 sec)

```
Note, if there are characters after CTRL-C they will apear in next prompt

b) CTRL-C x 2 (connection lost on second query)
```
# 1. query (note that time is 8s)
MariaDB [(none)]> show databases;
^C^CCtrl-C -- query killed. Continuing normally.
Ctrl-C -- query killed. Continuing normally.
+--------------------+
| Database           |
+--------------------+
+--------------------+
4 rows in set (8.716 sec)

# 2. query
MariaDB [(none)]> show databases;
ERROR 2013 (HY000): Lost connection to server during query

# 3. query (note that time is 4s to reconnect, any other query is 1s)
MariaDB [(none)]> show databases;
ERROR 2006 (HY000): Server has gone away
No connection. Trying to reconnect...
Connection id:    15
Current database: *** NONE ***

+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (4.002 sec)
```

Note: In case any new character added to CTRL-C x 2 it is showed in the prompt for 2. query

c) CTRL-C x 3 - same as b).

2.3 With the patch - the situation is the same as in 2.2 and is not part of fixing.
3. Special case with patch
a) Query -> CTRL-C x 1 ->  CTRL-C (no problem)
```
MariaDB [(none)]> show databases;
^CCtrl-C -- query killed. Continuing normally.
+--------------------+
| Database           |
+--------------------+
+--------------------+
4 rows in set (4.403 sec)

MariaDB [(none)]> ^C
MariaDB [(none)]> exit
Bye
```

b) Query -> CTRL-C x 2 (+optional chars)->  CTRL-C (it is aborted - connection killed - interrupted_query == 2 - > works as coded, but should it kill?)
```
MariaDB [(none)]> show databases;
^C^CCtrl-C -- query killed. Continuing normally.
Ctrl-C -- query killed. Continuing normally.
+--------------------+
| Database           |
+--------------------+
+--------------------+
4 rows in set (8.511 sec)

MariaDB [(none)]> Ctrl-C -- exit!
Aborted
```

c) Query -> CTRL-C x 2 -> Query->CTRL-C (it is not aborted aborted -normal)
```
MariaDB [(none)]> show databases;
^C^CCtrl-C -- query killed. Continuing normally.
Ctrl-C -- query killed. Continuing normally.
+--------------------+
| Database           |
+--------------------+
+--------------------+
4 rows in set (8.392 sec)

MariaDB [(none)]> show databases;
ERROR 2013 (HY000): Lost connection to MySQL server during query
MariaDB [(none)]> ^C
MariaDB [(none)]> exit
Bye
```

d) Query -> CTRL-C x 2 (+ chars) -> Query -> CTRL-C (asan bug)
```

```
=ASAN LEAK
```
MariaDB [(none)]> show databases;
^C^C aCtrl-C -- query killed. Continuing normally.
Ctrl-C -- query killed. Continuing normally.
+--------------------+
| Database           |
+--------------------+
+--------------------+
4 rows in set (8.438 sec)

MariaDB [(none)]> show databases;
ERROR 2013 (HY000): Lost connection to MySQL server during query
MariaDB [(none)]> ^C
MariaDB [(none)]> exit
Bye
```

- ASAN
```
==71534==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x7f9c94947808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f9c94823eac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f9c9481e902 in rl_add_undo (/lib/x86_64-linux-gnu/libreadline.so.5+0x24902)
    #3 0x7f9c948211f0 in rl_delete_text (/lib/x86_64-linux-gnu/libreadline.so.5+0x271f0)
    #4 0x7f9c94822937 in _rl_rubout_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x28937)
    #5 0x7f9c9480c455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #6 0x7f9c9480c7c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #7 0x7f9c9480cdc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #8 0x55a0b0725139 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.4/client/mysql.cc:2128
    #9 0x55a0b0722fda in main /home/anel/GitHub/mariadb/server/src/10.4/client/mysql.cc:1297
    #10 0x7f9c93ed5082 in __libc_start_main ../csu/libc-start.c:308
    #11 0x55a0b07211ad in _start (/home/anel/GitHub/mariadb/server/build/10.4/client/mysql+0xd51ad)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x7f9c94947808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f9c94823eac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f9c9481e902 in rl_add_undo (/lib/x86_64-linux-gnu/libreadline.so.5+0x24902)
    #3 0x7f9c948211f0 in rl_delete_text (/lib/x86_64-linux-gnu/libreadline.so.5+0x271f0)
    #4 0x7f9c94822937 in _rl_rubout_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x28937)
    #5 0x7f9c9480c455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #6 0x7f9c9480c7c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #7 0x7f9c9480cdc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #8 0x55a0b0725139 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.4/client/mysql.cc:2128
    #9 0x55a0b0722fda in main /home/anel/GitHub/mariadb/server/src/10.4/client/mysql.cc:1297
    #10 0x7f9c93ed5082 in __libc_start_main ../csu/libc-start.c:308
    #11 0x55a0b07211ad in _start (/home/anel/GitHub/mariadb/server/build/10.4/client/mysql+0xd51ad)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x7f9c94947808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f9c94823eac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f9c9481e902 in rl_add_undo (/lib/x86_64-linux-gnu/libreadline.so.5+0x24902)
    #3 0x7f9c948210ec in rl_insert_text (/lib/x86_64-linux-gnu/libreadline.so.5+0x270ec)
    #4 0x7f9c94822079 in _rl_insert_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x28079)
    #5 0x7f9c9480c455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #6 0x7f9c9480c7c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #7 0x7f9c9480cdc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #8 0x55a0b0725139 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.4/client/mysql.cc:2128
    #9 0x55a0b0722fda in main /home/anel/GitHub/mariadb/server/src/10.4/client/mysql.cc:1297
    #10 0x7f9c93ed5082 in __libc_start_main ../csu/libc-start.c:308
    #11 0x55a0b07211ad in _start (/home/anel/GitHub/mariadb/server/build/10.4/client/mysql+0xd51ad)

Indirect leak of 4 byte(s) in 2 object(s) allocated from:
    #0 0x7f9c94947808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f9c94823eac in xmalloc (/lib/x86_64-linux-gnu/libreadline.so.5+0x29eac)
    #2 0x7f9c9481d8c5 in rl_copy_text (/lib/x86_64-linux-gnu/libreadline.so.5+0x238c5)
    #3 0x7f9c94821199 in rl_delete_text (/lib/x86_64-linux-gnu/libreadline.so.5+0x27199)
    #4 0x7f9c94822937 in _rl_rubout_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x28937)
    #5 0x7f9c9480c455 in _rl_dispatch_subseq (/lib/x86_64-linux-gnu/libreadline.so.5+0x12455)
    #6 0x7f9c9480c7c0 in readline_internal_char (/lib/x86_64-linux-gnu/libreadline.so.5+0x127c0)
    #7 0x7f9c9480cdc4 in readline (/lib/x86_64-linux-gnu/libreadline.so.5+0x12dc4)
    #8 0x55a0b0725139 in read_and_execute /home/anel/GitHub/mariadb/server/src/10.4/client/mysql.cc:2128
    #9 0x55a0b0722fda in main /home/anel/GitHub/mariadb/server/src/10.4/client/mysql.cc:1297
    #10 0x7f9c93ed5082 in __libc_start_main ../csu/libc-start.c:308
    #11 0x55a0b07211ad in _start (/home/anel/GitHub/mariadb/server/build/10.4/client/mysql+0xd51ad)

SUMMARY: AddressSanitizer: 100 byte(s) leaked in 5 allocation(s).
Aborted (core dumped)

```


With new patch we have:
```
MariaDB [(none)]> show databases;
^C^C^C^CCtrl-C -- query killed. Continuing normally.
Ctrl-C -- connection killed. Abort. 
+--------------------+
| Database           |
+--------------------+
+--------------------+
4 rows in set (8.479 sec)

Bye

```



