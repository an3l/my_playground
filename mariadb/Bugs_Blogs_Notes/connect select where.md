GDB from main

(gdb) info b
+info b
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x00005555561fbd60 in STRING::GetStr() at /home/anel/mariadb/server/src/10.3/storage/connect/xobject.h:131
	breakpoint already hit 1 time
2       breakpoint     keep y   0x0000555555c8dfd2 in mysql_parse(THD*, char*, unsigned int, Parser_state*, bool, bool) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:7790
	breakpoint already hit 6 times


Thread 6 "mysqld" hit Breakpoint 1, STRING::GetStr (this=0x0) at /home/anel/mariadb/server/src/10.3/storage/connect/xobject.h:131
131		inline PSZ    GetStr(void) {return Strp;}
(gdb) bt
+bt
#0  STRING::GetStr (this=0x0) at /home/anel/mariadb/server/src/10.3/storage/connect/xobject.h:131
#1  0x000055555622bc86 in TDBMYSQL::OpenDB (this=0x7fffd7fff3d0, g=0x7fffe0030970) at /home/anel/mariadb/server/src/10.3/storage/connect/tabmysql.cpp:921
#2  0x00005555561e3f19 in CntOpenTable (g=0x7fffe0030970, tdbp=0x7fffd7fff3d0, mode=MODE_READ, c1=0x7fffd7fff570 "id", c2=0x0, del=false) at /home/anel/mariadb/server/src/10.3/storage/connect/connect.cc:348
#3  0x00005555561d1524 in ha_connect::OpenTable (this=0x7fffe002ee90, g=0x7fffe0030970, del=false) at /home/anel/mariadb/server/src/10.3/storage/connect/ha_connect.cc:2101
#4  0x00005555561d834f in ha_connect::rnd_init (this=0x7fffe002ee90, scan=true) at /home/anel/mariadb/server/src/10.3/storage/connect/ha_connect.cc:4154
#5  0x0000555555c39581 in handler::ha_rnd_init (this=0x7fffe002ee90, scan=true) at /home/anel/mariadb/server/src/10.3/sql/handler.h:3059
#6  0x0000555555fb77ab in handler::ha_rnd_init_with_error (this=0x7fffe002ee90, scan=true) at /home/anel/mariadb/server/src/10.3/sql/handler.cc:3073
#7  0x0000555556153f9d in init_read_record (info=0x7fffe0015ba8, thd=0x7fffe0000d28, table=0x7fffe002e108, select=0x7fffe0016780, filesort=0x0, use_record_cache=1, print_error=true, disable_rr_cache=false) at /home/anel/mariadb/server/src/10.3/sql/records.cc:294
#8  0x0000555555cfef9f in join_init_read_record (tab=0x7fffe0015ae0) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:20871
#9  0x0000555555cfca7f in sub_select (join=0x7fffe00146f8, join_tab=0x7fffe0015ae0, end_of_records=false) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:19929
#10 0x0000555555cfbf38 in do_select (join=0x7fffe00146f8, procedure=0x0) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:19470
#11 0x0000555555cd2853 in JOIN::exec_inner (this=0x7fffe00146f8) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:4171
#12 0x0000555555cd1c12 in JOIN::exec (this=0x7fffe00146f8) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:3965
#13 0x0000555555cd2f5a in mysql_select (thd=0x7fffe0000d28, tables=0x7fffe0013f88, wild_num=1, fields=@0x7fffe0005498: {<base_list> = {<Sql_alloc> = {<No data fields>}, first = 0x7fffe0013f40, last = 0x7fffe0014ec8, elements = 2}, <No data fields>}, conds=0x0, og_num=0, order=0x0, group=0x0, having=0x0, proc_param=0x0, select_options=2147748608, result=0x7fffe00146d0, unit=0x7fffe0004bd8, select_lex=0x7fffe0005370) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:4374
#14 0x0000555555cc411c in handle_select (thd=0x7fffe0000d28, lex=0x7fffe0004b18, result=0x7fffe00146d0, setup_tables_done_option=0) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:372
#15 0x0000555555c89ef1 in execute_sqlcom_select (thd=0x7fffe0000d28, all_tables=0x7fffe0013f88) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:6340
#16 0x0000555555c808c5 in mysql_execute_command (thd=0x7fffe0000d28) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:3871
#17 0x0000555555c8e292 in mysql_parse (thd=0x7fffe0000d28, rawbuf=0x7fffe0013da0 "SELECT * FROM t2", length=16, parser_state=0x7ffff161c5b0, is_com_multi=false, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:7871
#18 0x0000555555c7a953 in dispatch_command (command=COM_QUERY, thd=0x7fffe0000d28, packet=0x7fffe00088a9 "", packet_length=16, is_com_multi=false, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:1852
#19 0x0000555555c792f3 in do_command (thd=0x7fffe0000d28) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:1398
#20 0x0000555555dfb812 in do_handle_one_connection (connect=0x555557f7ce18) at /home/anel/mariadb/server/src/10.3/sql/sql_connect.cc:1403
#21 0x0000555555dfb56e in handle_one_connection (arg=0x555557f7ce18) at /home/anel/mariadb/server/src/10.3/sql/sql_connect.cc:1308
#22 0x00005555568ce9df in pfs_spawn_thread (arg=0x555558035ed8) at /home/anel/mariadb/server/src/10.3/storage/perfschema/pfs.cc:1869
#23 0x00007ffff7839609 in start_thread (arg=<optimized out>) at pthread_create.c:477
#24 0x00007ffff775e133 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:95


c

Thread 7 "mysqld" hit Breakpoint 2, mysql_parse (thd=0x555555c4c770 <Lex_input_stream::init(THD*, char*, unsigned long)+204>, rawbuf=0x7ffff15d1400 "0\024]\361\377\177", length=32767, parser_state=0x7fffd0010bf0, is_com_multi=176, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:7790
7790	{
(gdb) bt
+bt
#0  mysql_parse (thd=0x555555c4c770 <Lex_input_stream::init(THD*, char*, unsigned long)+204>, rawbuf=0x7ffff15d1400 "0\024]\361\377\177", length=32767, parser_state=0x7fffd0010bf0, is_com_multi=176, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:7790
#1  0x0000555555c7a953 in dispatch_command (command=COM_QUERY, thd=0x7fffd0000d58, packet=0x7fffd00088d9 "SELECT `id`, `spaced col` FROM `t1`", packet_length=35, is_com_multi=false, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:1852
#2  0x0000555555c792f3 in do_command (thd=0x7fffd0000d58) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:1398
#3  0x0000555555dfb812 in do_handle_one_connection (connect=0x555558000248) at /home/anel/mariadb/server/src/10.3/sql/sql_connect.cc:1403
#4  0x0000555555dfb56e in handle_one_connection (arg=0x555558000248) at /home/anel/mariadb/server/src/10.3/sql/sql_connect.cc:1308
#5  0x00005555568ce9df in pfs_spawn_thread (arg=0x5555580362d8) at /home/anel/mariadb/server/src/10.3/storage/perfschema/pfs.cc:1869
#6  0x00007ffff7839609 in start_thread (arg=<optimized out>) at pthread_create.c:477
#7  0x00007ffff775e133 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:95


Thread 6 "mysqld" hit Breakpoint 2, mysql_parse (thd=0x555555c4c770 <Lex_input_stream::init(THD*, char*, unsigned long)+204>, rawbuf=0x7ffff161c400 "0\304a\361\377\177", length=32767, parser_state=0x7fffe0013da0, is_com_multi=176, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:7790
7790	{
(gdb) bt
+bt
#0  mysql_parse (thd=0x555555c4c770 <Lex_input_stream::init(THD*, char*, unsigned long)+204>, rawbuf=0x7ffff161c400 "0\304a\361\377\177", length=32767, parser_state=0x7fffe0013da0, is_com_multi=176, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:7790
#1  0x0000555555c7a953 in dispatch_command (command=COM_QUERY, thd=0x7fffe0000d28, packet=0x7fffe00088a9 "SELECT `id` FROM t2 WHERE t2.`spaced col` = 'C-003'", packet_length=51, is_com_multi=false, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:1852
#2  0x0000555555c792f3 in do_command (thd=0x7fffe0000d28) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:1398
#3  0x0000555555dfb812 in do_handle_one_connection (connect=0x555557f7ce18) at /home/anel/mariadb/server/src/10.3/sql/sql_connect.cc:1403
#4  0x0000555555dfb56e in handle_one_connection (arg=0x555557f7ce18) at /home/anel/mariadb/server/src/10.3/sql/sql_connect.cc:1308
#5  0x00005555568ce9df in pfs_spawn_thread (arg=0x555558035ed8) at /home/anel/mariadb/server/src/10.3/storage/perfschema/pfs.cc:1869
#6  0x00007ffff7839609 in start_thread (arg=<optimized out>) at pthread_create.c:477
#7  0x00007ffff775e133 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:95


(gdb) bt
+bt
#0  STRING::GetStr (this=0x0) at /home/anel/mariadb/server/src/10.3/storage/connect/xobject.h:131
#1  0x000055555622bc86 in TDBMYSQL::OpenDB (this=0x7fffd7fff400, g=0x7fffe0030970) at /home/anel/mariadb/server/src/10.3/storage/connect/tabmysql.cpp:921
#2  0x00005555561e3f19 in CntOpenTable (g=0x7fffe0030970, tdbp=0x7fffd7fff400, mode=MODE_READ, c1=0x7fffd7fff5f8 "id", c2=0x0, del=false) at /home/anel/mariadb/server/src/10.3/storage/connect/connect.cc:348
#3  0x00005555561d1524 in ha_connect::OpenTable (this=0x7fffe002ee90, g=0x7fffe0030970, del=false) at /home/anel/mariadb/server/src/10.3/storage/connect/ha_connect.cc:2101
#4  0x00005555561d834f in ha_connect::rnd_init (this=0x7fffe002ee90, scan=true) at /home/anel/mariadb/server/src/10.3/storage/connect/ha_connect.cc:4154
#5  0x0000555555c39581 in handler::ha_rnd_init (this=0x7fffe002ee90, scan=true) at /home/anel/mariadb/server/src/10.3/sql/handler.h:3059
#6  0x0000555555fb77ab in handler::ha_rnd_init_with_error (this=0x7fffe002ee90, scan=true) at /home/anel/mariadb/server/src/10.3/sql/handler.cc:3073
#7  0x0000555556153f9d in init_read_record (info=0x7fffe0016730, thd=0x7fffe0000d28, table=0x7fffe002e108, select=0x7fffe0017480, filesort=0x0, use_record_cache=1, print_error=true, disable_rr_cache=false) at /home/anel/mariadb/server/src/10.3/sql/records.cc:294
#8  0x0000555555cfef9f in join_init_read_record (tab=0x7fffe0016668) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:20871
#9  0x0000555555cfca7f in sub_select (join=0x7fffe0014aa0, join_tab=0x7fffe0016668, end_of_records=false) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:19929
#10 0x0000555555cfbf38 in do_select (join=0x7fffe0014aa0, procedure=0x0) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:19470
#11 0x0000555555cd2853 in JOIN::exec_inner (this=0x7fffe0014aa0) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:4171
#12 0x0000555555cd1c12 in JOIN::exec (this=0x7fffe0014aa0) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:3965
#13 0x0000555555cd2f5a in mysql_select (thd=0x7fffe0000d28, tables=0x7fffe0013fe0, wild_num=0, fields=@0x7fffe0005498: {<base_list> = {<Sql_alloc> = {<No data fields>}, first = 0x7fffe0013f98, last = 0x7fffe0013f98, elements = 1}, <No data fields>}, conds=0x7fffe0014840, og_num=0, order=0x0, group=0x0, having=0x0, proc_param=0x0, select_options=2147748608, result=0x7fffe0014a78, unit=0x7fffe0004bd8, select_lex=0x7fffe0005370) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:4374
#14 0x0000555555cc411c in handle_select (thd=0x7fffe0000d28, lex=0x7fffe0004b18, result=0x7fffe0014a78, setup_tables_done_option=0) at /home/anel/mariadb/server/src/10.3/sql/sql_select.cc:372
#15 0x0000555555c89ef1 in execute_sqlcom_select (thd=0x7fffe0000d28, all_tables=0x7fffe0013fe0) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:6340
#16 0x0000555555c808c5 in mysql_execute_command (thd=0x7fffe0000d28) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:3871
#17 0x0000555555c8e292 in mysql_parse (thd=0x7fffe0000d28, rawbuf=0x7fffe0013da0 "SELECT `id` FROM t2 WHERE t2.`spaced col` = 'C-003'", length=51, parser_state=0x7ffff161c5b0, is_com_multi=false, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:7871
#18 0x0000555555c7a953 in dispatch_command (command=COM_QUERY, thd=0x7fffe0000d28, packet=0x7fffe00088a9 "", packet_length=51, is_com_multi=false, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:1852
#19 0x0000555555c792f3 in do_command (thd=0x7fffe0000d28) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:1398
#20 0x0000555555dfb812 in do_handle_one_connection (connect=0x555557f7ce18) at /home/anel/mariadb/server/src/10.3/sql/sql_connect.cc:1403
#21 0x0000555555dfb56e in handle_one_connection (arg=0x555557f7ce18) at /home/anel/mariadb/server/src/10.3/sql/sql_connect.cc:1308
#22 0x00005555568ce9df in pfs_spawn_thread (arg=0x555558035ed8) at /home/anel/mariadb/server/src/10.3/storage/perfschema/pfs.cc:1869
#23 0x00007ffff7839609 in start_thread (arg=<optimized out>) at pthread_create.c:477
#24 0x00007ffff775e133 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:95


(gdb) bt
+bt
#0  mysql_parse (thd=0x555555c4c770 <Lex_input_stream::init(THD*, char*, unsigned long)+204>, rawbuf=0x7ffff15d1400 "0\024]\361\377\177", length=32767, parser_state=0x7fffd0010d38, is_com_multi=176, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:7790
#1  0x0000555555c7a953 in dispatch_command (command=COM_QUERY, thd=0x7fffd0000d58, packet=0x7fffd0018cc9 "SELECT `id`, `spaced col` FROM `t1` WHERE spaced col= 'C-003'", packet_length=61, is_com_multi=false, is_next_command=false) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:1852
#2  0x0000555555c792f3 in do_command (thd=0x7fffd0000d58) at /home/anel/mariadb/server/src/10.3/sql/sql_parse.cc:1398
#3  0x0000555555dfb812 in do_handle_one_connection (connect=0x555558000248) at /home/anel/mariadb/server/src/10.3/sql/sql_connect.cc:1403
#4  0x0000555555dfb56e in handle_one_connection (arg=0x555558000248) at /home/anel/mariadb/server/src/10.3/sql/sql_connect.cc:1308
#5  0x00005555568ce9df in pfs_spawn_thread (arg=0x5555580362d8) at /home/anel/mariadb/server/src/10.3/storage/perfschema/pfs.cc:1869
#6  0x00007ffff7839609 in start_thread (arg=<optimized out>) at pthread_create.c:477
#7  0x00007ffff775e133 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:95



Sa patchem palo 
 connect.mysql_exec connect.misc connect.mysql_index
 
 
 pa ovo  connect.misc connect.mysql_index
 
 
 Test
  make && ./mysql-test/mtr connect.mysql_exec connect.misc connect.mysql_index connect.mysql --force --mem

