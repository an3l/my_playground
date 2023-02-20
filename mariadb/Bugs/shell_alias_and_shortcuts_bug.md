(gdb) f 4
+f 4
#4  0x00005555555b458f in read_and_execute (interactive=true) at /home/anel/GitHub/mariadb/server/src/10.3/clien
t/mysql.cc:2146


(gdb) f 3
+f 3
#3  0x00005555555b5393 in add_line (buffer=@0x5555559b9280: {<Sql_alloc> = {<No data fields>}, Ptr = 0x5555559f9
f98 "alias a='x'", str_length = 11, Alloced_length = 520, extra_alloc = 0, alloced = true, thread_specific = fal
se, str_charset = 0x555555805b80 <my_charset_bin>}, line=0x555555a3f4f0 "alias a='x';", line_length=12, in_strin
g=0x7fffffffda76 "", ml_comment=0x7fffffffda77, truncated=false) at /home/anel/GitHub/mariadb/server/src/10.3/cl
ient/mysql.cc:2448


(gdb) p buffer.c_ptr()
+p buffer.c_ptr()
$6 = 0x5555559f9f98 "alias a='x'"



Shortcuts:

(gdb) f 3
+f 3
#3  0x00005555555b4fed in add_line (buffer=@0x5555559b9280: {<Sql_alloc> = {<No data fields>}, Ptr = 0x5555559f9
f98 "alias a='x'", str_length = 0, Alloced_length = 520, extra_alloc = 0, alloced = true, thread_specific = fals
e, str_charset = 0x555555805b80 <my_charset_bin>}, line=0x555555a3efa0 "\\a b='y';", line_length=9, in_string=0x
7fffffffda76 "", ml_comment=0x7fffffffda77, truncated=false) at /home/anel/GitHub/mariadb/server/src/10.3/client
/mysql.cc:2378




### Invoke mysqlbinlog bug
# Start some test to obtain /build/10.3/mysql-test/var/my.cnf file
 // $ ./mysql-test/mtr binlog.binlog_base64_flag --manual-gdb
# Stop the test

# Start the server from build
$ ./sql/mysqld --defaults-file=~/.my103.cnf

# Start mysqlbinlog With mysql
./client/mysqlbinlog --defaults-file=/home/anel/GitHub/mariadb/server/build/10.3/mysql-test/var/my.cnf --local-load=/home/anel/GitHub/mariadb/server/build/10.3/mysql-test/var/tmp suite/binlog/std_data/bug32407.001 | /home/anel/GitHub/mariadb/server/build/10.3/client//mysql
 --defaults-file=/home/anel/GitHub/mariadb/server/build/10.3/mysql-test/var/my.cnf
 
# Start mysqlbinlog  without mysql
 ./client/mysqlbinlog --defaults-file=/home/anel/GitHub/mariadb/server/build/10.3/mysql-test/var/my.cnf --local-load=/home/anel/GitHub/mariadb/server/build/10.3/mysql-test/var/tmp /home/anel/GitHub/mariadb/server/src/10.3/mysql-test/suite/binlog/std_data/bug32407.001 
 
## Redirect to file
## Without mysql no patch
./client/mysqlbinlog --defaults-file=/home/anel/GitHub/mariadb/server/build/10.3/mysql-test/var/my.cnf --local-load=/home/anel/GitHub/mariadb/server/build/10.3/mysql-test/var/tmp /home/anel/GitHub/mariadb/server/src/10.3/mysql-test/suite/binlog/std_data/bug32407.001 > /tmp/mylog_no_patch.txt
 
## Without mysql with patch file
./client/mysqlbinlog --defaults-file=/home/anel/GitHub/mariadb/server/build/10.3/mysql-test/var/my.cnf --local-load=/home/anel/GitHub/mariadb/server/build/10.3/mysql-test/var/tmp /home/anel/GitHub/mariadb/server/src/10.3/mysql-test/suite/binlog/std_data/bug32407.001 > /tmp/mylog_with_patch.txt


### Insert using mysql
$ ./client/mysql --defaults-file=~/.my103.cnf < /tmp/mylog_with_patch.txt
ERROR 1227 (42000) at line 8: Access denied; you need (at least one of) the SUPER privilege(s) for this operation
### BUG
$ ./client/mysql --defaults-file=~/.my103.cnf -uroot < /tmp/mylog_with_patch.txt
ERROR at line 20: Usage: \C charset_name | charset charset_name

## Conclusion 
mysql binary generated with patch equally bad parses files from patch and also before patch

# Testing on gdb
## Use file to gdb
 gdb --args ./client/mysql
 r --defaults-file=~/.my103.cnf -uroot < /tmp/mylog_with_patch.txt< /tmp/mylog_with_patch.txt
 
 
* ss_comment becomes 0 instead of 1
* (gdb) p pos
+p pos
$72 = 0x5555559d9e14 " *//*!*/;" # last8 characters
* (gdb) p line
+p line
$71 = 0x5555559d9e08 "/*!\\C latin1 *//*!*/;"

* buffer is created from out-line, since they are not equal at the beginning
out =   "\\C latin1 *//*!*/;"
line="/*!\\C latin1 *//*!*/;"
(gdb) p buffer.c_ptr()
+p buffer.c_ptr()
$73 = 0x5555559f9d38 "/*!" 


### Bez patcha dogodi se call ovog parametra
(gdb) p pos-1
+p pos-1
$8 = 0x5555559d9e0b "\\C latin1 *//*!*/;"
 
