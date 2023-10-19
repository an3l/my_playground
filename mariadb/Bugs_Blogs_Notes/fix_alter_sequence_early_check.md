# Call early check for sequence in alter statement

https://github.com/an3l/server/commit/cf43137ca5da3a038acc1f99d2f1cc97f5cc1e3c#diff-f223b918b8e982bb3edaed26dc567ac653c0cf35f5ca624e2e3b664d4be5d49d

# First call
mysql_alter_table->
                    mysql_prepare_alter_table
```
(gdb) bt
+bt
#0  mysql_prepare_alter_table (thd=0xdd956581a3f, table=0x555556c21bc3, create_info=0x7fffe0000ce0, alter_info=0x7fff00000009, alter_ctx=0x7ffff1f2f140) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_table.cc:8411
#1  0x0000555555fa82d8 in mysql_alter_table (thd=0x7fffe0000d48, new_db=0x7fffe00057d8, new_name=0x7fffe0005c28, create_info=0x7ffff1f312e0, table_list=0x7fffe00165f0, recreate_info=0x7ffff1f311b0, alter_info=0x7ffff1f311f0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_table.cc:10570

```
# Second call

Path:

create_table_impl->
		    mysql_create_frm_image ->
				             mysql_prepare_create_table_finalize
				                                                 -> check_sequence_fields()
```
(gdb) bt
+bt
#0  my_message_sql (error=21845, str=0x7ffff1f2e570 "\240\345\362\361\377\177", MyFlags=93825015206591) at /home/anel/GitHub/mariadb/server/src/10.5/sql/mysqld.cc:3094
#1  0x0000555556b2f5a6 in my_error (nr=4086, MyFlags=0) at /home/anel/GitHub/mariadb/server/src/10.5/mysys/my_error.c:124
#2  0x000055555612f898 in check_sequence_fields (lex=0x7fffe0004e30, fields=0x7ffff1f31270) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_sequence.cc:237
#3  0x0000555555f92b67 in mysql_prepare_create_table (thd=0x7fffe0000d48, create_info=0x7ffff1f312e0, alter_info=0x7ffff1f311f0, db_options=0x7ffff1f2ec4c, file=0x7fffe0017760, key_info_buffer=0x7ffff1f2f5f8, key_count=0x7ffff1f2f5d8, create_table_mode=-2) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_table.cc:3621
#4  0x0000555555f979d9 in mysql_create_frm_image (thd=0x7fffe0000d48, create_info=0x7ffff1f312e0, alter_info=0x7ffff1f311f0, create_table_mode=-2, key_info=0x7ffff1f2f5f8, key_count=0x7ffff1f2f5d8, frm=0x7ffff1f2f670) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_table.cc:5069
#5  0x0000555555f98600 in create_table_impl (thd=0x7fffe0000d48, orig_db=@0x7ffff1f306b0: {str = 0x7fffe0016d10 "test", length = 4}, orig_table_name=@0x7ffff1f306c0: {str = 0x7fffe00165d0 "seq1", length = 4}, db=@0x7ffff1f306e0: {str = 0x7fffe0016d10 "test", length = 4}, table_name=@0x7ffff1f30710: {str = 0x7ffff1f30a4b "#sql-alter-9696-3", length = 17}, path=0x7ffff1f30f0e "/home/anel/GitHub/mariadb/server/build/10.5/mysql-test/var/tmp/mysqld.1/#sql-temptable-9696-3-1", options={m_options = DDL_options_st::OPT_NONE}, create_info=0x7ffff1f312e0, alter_info=0x7ffff1f311f0, create_table_mode=-2, is_trans=0x0, key_info=0x7ffff1f2f5f8, key_count=0x7ffff1f2f5d8, frm=0x7ffff1f2f670) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_table.cc:5349
#6  0x0000555555fa8b43 in mysql_alter_table (thd=0x7fffe0000d48, new_db=0x7fffe00057d8, new_name=0x7fffe0005c28, create_info=0x7ffff1f312e0, table_list=0x7fffe0016610, recreate_info=0x7ffff1f311b0, alter_info=0x7ffff1f311f0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_table.cc:10753
```

# With patch - interesting, there is an optimization
if (cond1 && check_sequence_field()) , note that the lines are not good
```
(gdb) bt
+bt
#0  my_message_sql (error=4086, str=0x7ffff20194a0 "Sequence 'test.seq1' table structure is invalid (cache_size)", MyFlags=0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/mysqld.cc:3372
#1  0x000055555689557f in my_error (nr=nr@entry=4086, MyFlags=MyFlags@entry=0) at /home/anel/GitHub/mariadb/server/src/11.2/mysys/my_error.c:124
#2  0x0000555556001bb4 in check_sequence_fields (lex=0x7fffe0005180, fields=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_lex.h:3212
#3  0x0000555555e6974e in mysql_prepare_alter_table (thd=0x7fffe0000d48, table=0x7fffe001e0e8, create_info=0x7ffff201c270, alter_info=0x7ffff201c180, alter_ctx=0x7ffff201b460) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_list.h:225
#4  0x0000555555e7933c in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005b38, new_name=new_name@entry=0x7fffe0005f88, create_info=create_info@entry=0x7ffff201c270, table_list=<optimized out>, table_list@entry=0x7fffe0016d40, recreate_info=recreate_info@entry=0x7ffff201c140, alter_info=0x7ffff201c180, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:10491
#5  0x0000555555f101d5 in Sql_cmd_alter_table::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/structs.h:568

```
# WIth patch - split if branches
```
(gdb) bt
+bt
#0  my_message_sql (error=4086, str=0x7ffff20194a0 "Sequence 'test.seq1' table structure is invalid (cache_size)", MyFlags=0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/mysqld.cc:3372
#1  0x0000555556895573 in my_error (nr=nr@entry=4086, MyFlags=MyFlags@entry=0) at /home/anel/GitHub/mariadb/server/src/11.2/mysys/my_error.c:124
#2  0x0000555556001ba8 in check_sequence_fields (lex=0x7fffe0005180, fields=fields@entry=0x7ffff20198c0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_lex.h:3212
#3  0x0000555555e69772 in mysql_prepare_alter_table (thd=thd@entry=0x7fffe0000d48, table=table@entry=0x7fffe001e0e8, create_info=create_info@entry=0x7ffff201c270, alter_info=alter_info@entry=0x7ffff201c180, alter_ctx=alter_ctx@entry=0x7ffff201b460) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:8525
#4  0x0000555555e79330 in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005b38, new_name=new_name@entry=0x7fffe0005f88, create_info=create_info@entry=0x7ffff201c270, table_list=<optimized out>, table_list@entry=0x7fffe0016d40, recreate_info=recreate_info@entry=0x7ffff201c140, alter_info=0x7ffff201c180, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:10489
#5  0x0000555555f101c9 in Sq
```
