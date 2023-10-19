# MDEV-31618 - alter temporary sequence crashes the show tables
https://jira.mariadb.org/browse/MDEV-31618

## Test case for regular sequnce
```sql
create sequence s1;
--error 4086
alter table s1 change cache_size cache_size int;

drop table s1;
```

### BT frames
```
#0  my_message_sql (error=4086, str=0x7ffff2018dc0 "Sequence 'test.s1' table structure is invalid (cache_size)", MyFlags=0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/mysqld.cc:3365
#1  0x0000555556896e8e in my_error (nr=nr@entry=4086, MyFlags=MyFlags@entry=0) at /home/anel/GitHub/mariadb/server/src/11.2/mysys/my_error.c:124
#2  0x0000555555ff7230 in check_sequence_fields (lex=0x7fffe00050c0, fields=fields@entry=0x7ffff201c220) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_lex.h:3219
#3  0x0000555555e5fb14 in mysql_prepare_create_table_finalize (thd=thd@entry=0x7fffe0000d48, create_info=create_info@entry=0x7ffff201c2b0, alter_info=alter_info@entry=0x7ffff201c1c0, db_options=db_options@entry=0x7ffff2019408, file=file@entry=0x7fffe0017ff0, key_info_buffer=key_info_buffer@entry=0x7ffff2019df0, key_count=0x7ffff2019de0, create_table_mode=-2, db=<optimized out>, table_name=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:2845
#4  0x0000555555e6511a in mysql_create_frm_image (thd=thd@entry=0x7fffe0000d48, db=@0x7ffff201b4b0: {str = 0x7fffe00173f0 "test", length = 4}, table_name=@0x7ffff201b4c0: {str = 0x7fffe0016ca8 "s1", length = 2}, create_info=create_info@entry=0x7ffff201c2b0, alter_info=alter_info@entry=0x7ffff201c1c0, create_table_mode=create_table_mode@entry=-2, key_info=0x7ffff2019df0, key_count=0x7ffff2019de0, frm=0x7ffff2019e20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4333
#5  0x0000555555e66633 in create_table_impl (thd=thd@entry=0x7fffe0000d48, ddl_log_state_create=ddl_log_state_create@entry=0x0, ddl_log_state_rm=<optimized out>, ddl_log_state_rm@entry=0x0, orig_db=@0x7ffff201b4b0: {str = 0x7fffe00173f0 "test", length = 4}, orig_table_name=@0x7ffff201b4c0: {str = 0x7fffe0016ca8 "s1", length = 2}, db=@0x7ffff201b4f0: {str = 0x7fffe00173f0 "test", length = 4}, table_name=@0x7ffff201b520: {str = 0x7ffff201ba1c "#sql-alter-1caca-3", length = 18}, path=@0x7ffff2019f70: {str = 0x7ffff201bedf "./test/#sql-alter-1caca-3", length = 25}, options=<optimized out>, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, create_table_mode=-2, is_trans=0x0, key_info=0x7ffff2019df0, key_count=0x7ffff2019de0, frm=0x7ffff2019e20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4647
#6  0x0000555555e6d929 in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005a78, new_name=new_name@entry=0x7fffe0005ec8, create_info=create_info@entry=0x7ffff201c2b0, table_list=<optimized out>, table_list@entry=0x7fffe0016ce0, recreate_info=recreate_info@entry=0x7ffff201c180, alter_info=0x7ffff201c1c0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_alter.h:302
#7  0x0000555555f04b81 in Sql_cmd_alter_table::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/structs.h:568
```

## Test case for temproary sequence
```sql

```

### BT frames for error the same as above
```
#0  my_message_sql (error=4086, str=0x7ffff2018dc0 "Sequence 'test.s1' table structure is invalid (cache_size)", MyFlags=0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/mysqld.cc:3365
#1  0x0000555556896e8e in my_error (nr=nr@entry=4086, MyFlags=MyFlags@entry=0) at /home/anel/GitHub/mariadb/server/src/11.2/mysys/my_error.c:124
#2  0x0000555555ff7230 in check_sequence_fields (lex=0x7fffe00050c0, fields=fields@entry=0x7ffff201c220) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_lex.h:3219
#3  0x0000555555e5fb14 in mysql_prepare_create_table_finalize (thd=thd@entry=0x7fffe0000d48, create_info=create_info@entry=0x7ffff201c2b0, alter_info=alter_info@entry=0x7ffff201c1c0, db_options=db_options@entry=0x7ffff2019408, file=file@entry=0x7fffe0017e30, key_info_buffer=key_info_buffer@entry=0x7ffff2019df0, key_count=0x7ffff2019de0, create_table_mode=-2, db=<optimized out>, table_name=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:2845
#4  0x0000555555e6511a in mysql_create_frm_image (thd=thd@entry=0x7fffe0000d48, db=@0x7ffff201b4b0: {str = 0x7fffe00173f0 "test", length = 4}, table_name=@0x7ffff201b4c0: {str = 0x7fffe0016ca8 "s1", length = 2}, create_info=create_info@entry=0x7ffff201c2b0, alter_info=alter_info@entry=0x7ffff201c1c0, create_table_mode=create_table_mode@entry=-2, key_info=0x7ffff2019df0, key_count=0x7ffff2019de0, frm=0x7ffff2019e20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4333
#5  0x0000555555e66633 in create_table_impl (thd=thd@entry=0x7fffe0000d48, ddl_log_state_create=ddl_log_state_create@entry=0x0, ddl_log_state_rm=<optimized out>, ddl_log_state_rm@entry=0x0, orig_db=@0x7ffff201b4b0: {str = 0x7fffe00173f0 "test", length = 4}, orig_table_name=@0x7ffff201b4c0: {str = 0x7fffe0016ca8 "s1", length = 2}, db=@0x7ffff201b4f0: {str = 0x7fffe00173f0 "test", length = 4}, table_name=@0x7ffff201b520: {str = 0x7ffff201ba1c "#sql-alter-1d207-3", length = 18}, path=@0x7ffff2019f70: {str = 0x7ffff201bedf "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-1d207-3-1", length = 96}, options=<optimized out>, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, create_table_mode=-2, is_trans=0x0, key_info=0x7ffff2019df0, key_count=0x7ffff2019de0, frm=0x7ffff2019e20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4647
#6  0x0000555555e6d929 in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005a78, new_name=new_name@entry=0x7fffe0005ec8, create_info=create_info@entry=0x7ffff201c2b0, table_list=<optimized out>, table_list@entry=0x7fffe0016ce0, recreate_info=recreate_info@entry=0x7ffff201c180, alter_info=0x7ffff201c1c0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_alter.h:302
#7  0x0000555555f04b81 in Sql_cmd_alter_table::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/structs.h:568

```

### 1. BT of creatig the temporay SEQUENCE `create temporary sequence s1`
```
# 0. mysql_prepare_create_table_finalize
#0  mysql_prepare_create_table_finalize (thd=0x7fffe0000d48, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, db_options=0x7ffff201a3b8, file=0x7fffe0018488, key_info_buffer=0x7ffff201ad08, key_count=0x7ffff201ad04, create_table_mode=0, db={str = 0x7fffe0017300 "test", length = 4}, table_name={str = 0x7fffe0016b80 "s1", length = 2}) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:2798
#1  0x0000555555e6511a in mysql_create_frm_image (thd=0x7fffe0000d48, db=@0x7fffe0016c08: {str = 0x7fffe0017300 "test", length = 4}, table_name=@0x7fffe0016c18: {str = 0x7fffe0016b80 "s1", length = 2}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4333
#2  0x0000555555e66633 in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=<optimized out>, orig_db=@0x7fffe0016c08: {str = 0x7fffe0017300 "test", length = 4}, orig_table_name=@0x7fffe0016c18: {str = 0x7fffe0016b80 "s1", length = 2}, db=@0x7fffe0016c08: {str = 0x7fffe0017300 "test", length = 4}, table_name=@0x7fffe0016c18: {str = 0x7fffe0016b80 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-33fd-3-0", length = 95}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4647
#3  0x0000555555e66da0 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, db=0x7fffe0016c08, table_name=0x7fffe0016c18, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016bf0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#4  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016bf0, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888


# 1. ha_create_table
#0  ha_create_table (thd=0x7fffe0000d48, path=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-2db0-3-0", db=0x7fffe0017300 "test", table_name=0x7fffe0016b80 "s1", create_info=0x7ffff201b300, frm=0x7ffff201ad20, skip_frm_file=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/handler.cc:6085
#1  0x0000555555e667bc in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=<optimized out>, orig_db=@0x7fffe0016c08: {str = 0x7fffe0017300 "test", length = 4}, orig_table_name=@0x7fffe0016c18: {str = 0x7fffe0016b80 "s1", length = 2}, db=@0x7fffe0016c08: {str = 0x7fffe0017300 "test", length = 4}, table_name=@0x7fffe0016c18: {str = 0x7fffe0016b80 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-2db0-3-0", length = 95}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4671

# 2. create_temporary_table
#0  THD::create_temporary_table (this=0x7fffe0000d48, frm=0x7ffff201ad20, path=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-2db0-3-0", db=0x7fffe0017300 "test", table_name=0x7fffe0016b80 "s1") at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:951
#1  0x000055555600ac54 in THD::create_and_open_tmp_table (this=0x7fffe0000d48, frm=0x7ffff201ad20, path=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-2db0-3-0", db=0x7fffe0017300 "test", table_name=0x7fffe0016b80 "s1", open_internal_tables=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:71
#2  0x0000555555e668fa in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=<optimized out>, orig_db=@0x7fffe0016c08: {str = 0x7fffe0017300 "test", length = 4}, orig_table_name=@0x7fffe0016c18: {str = 0x7fffe0016b80 "s1", length = 2}, db=@0x7fffe0016c08: {str = 0x7fffe0017300 "test", length = 4}, table_name=@0x7fffe0016c18: {str = 0x7fffe0016b80 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-2db0-3-0", length = 95}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4685


#3. sequence_definition:store_fields
#0  sequence_definition::store_fields (this=this@entry=0x7fffe0017308, table=table@entry=0x0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_sequence.cc:164
#1  0x0000555555ff7f94 in sequence_definition::write_initial_sequence (this=this@entry=0x7fffe0017308, table=0x0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_sequence.cc:614
#2  0x0000555555ff84ca in sequence_insert (thd=0x7fffe0000d48, lex=0x7fffe00050c0, org_table_list=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_sequence.cc:375
#3  0x0000555555e66df8 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, db=0x7fffe0016c08, table_name=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016bf0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4786
#4  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016bf0, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888


```

### 2. BT of altering the temporay sequence `alter table s1 change cache_size cache_size int`
```

  lex->sql_command = SQLCOM_ALTER_TABLE

# 0. mysql_prepare_create_table_finalize

#0  mysql_prepare_create_table_finalize (thd=0x7fffe0000d48, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, db_options=0x7ffff2019408, file=0x7fffe0017db0, key_info_buffer=0x7ffff2019df0, key_count=0x7ffff2019de0, create_table_mode=-2, db={str = 0x7fffe0017370 "test", length = 4}, table_name={str = 0x7fffe0016c28 "s1", length = 2}) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:2798
#1  0x0000555555e6511a in mysql_create_frm_image (thd=0x7fffe0000d48, db=@0x7ffff201b4b0: {str = 0x7fffe0017370 "test", length = 4}, table_name=@0x7ffff201b4c0: {str = 0x7fffe0016c28 "s1", length = 2}, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, create_table_mode=-2, key_info=0x7ffff2019df0, key_count=0x7ffff2019de0, frm=0x7ffff2019e20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4333
#2  0x0000555555e66633 in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=<optimized out>, orig_db=@0x7ffff201b4b0: {str = 0x7fffe0017370 "test", length = 4}, orig_table_name=@0x7ffff201b4c0: {str = 0x7fffe0016c28 "s1", length = 2}, db=@0x7ffff201b4f0: {str = 0x7fffe0017370 "test", length = 4}, table_name=@0x7ffff201b520: {str = 0x7ffff201ba1c "#sql-alter-33fd-3", length = 17}, path=@0x7ffff2019f70: {str = 0x7ffff201bedf "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-33fd-3-1", length = 95}, options=<optimized out>, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, create_table_mode=-2, is_trans=0x0, key_info=0x7ffff2019df0, key_count=0x7ffff2019de0, frm=0x7ffff2019e20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4647
#3  0x0000555555e6d929 in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005a78, new_name=new_name@entry=0x7fffe0005ec8, create_info=create_info@entry=0x7ffff201c2b0, table_list=<optimized out>, table_list@entry=0x7fffe0016c60, recreate_info=recreate_info@entry=0x7ffff201c180, alter_info=0x7ffff201c1c0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_alter.h:302
#4  0x0000555555f04b83 in Sql_cmd_alter_table::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/structs.h:568
#5  0x0000555555d70a4f in mysql_execute_command (thd=thd@entry=0x7fffe0000d48, is_called_from_prepared_stmt=is_called_from_prepared_stmt@entry=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:5766
#6  0x0000555555d575e5 in mysql_parse (thd=thd@entry=0x7fffe0000d48, rawbuf=<optimized out>, length=<optimized out>, parser_state=parser_state@entry=0x7ffff201d290) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:7769
#7  0x0000555555d66827 in dispatch_command (command=command@entry=COM_QUERY, thd=thd@entry=0x7fffe0000d48, packet=packet@entry=0x7fffe000b129 "alter table s1 change cache_size cache_size int", packet_length=packet_length@entry=47, blocking=blocking@entry=true) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_class.h:1371


# 1.  my_message_sql
#1  0x0000555556896e8e in my_error (nr=nr@entry=4086, MyFlags=MyFlags@entry=0) at /home/anel/GitHub/mariadb/server/src/11.2/mysys/my_error.c:124
#2  0x0000555555ff7230 in check_sequence_fields (lex=0x7fffe00050c0, fields=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_lex.h:3219
#3  0x0000555555e5fb14 in mysql_prepare_create_table_finalize (thd=0x7fffe0000d48, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, db_options=0x7ffff2019408, file=0x7fffe0017db0, key_info_buffer=0x7ffff2019df0, key_count=0x7ffff2019de0, create_table_mode=-2, db=<optimized out>, table_name=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:2845


# AFTER DEBUGGING
find_temporary_table() fails since there is nocall of mysql_create_table_no_lock that is expected to be called!
Possible fix: check create_info->sequence in alter and call function()

mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005a78, new_name=new_name@entry=0x7fffe0005ec8, create_info=cre
ate_info@entry=0x7ffff201c2b0, table_list=<optimized out>, table_list@entry=0x7fffe0016c60, recreate_info=recreate_info@entry=0x7ffff201c180
, alter_info=0x7ffff201c1c0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_tab
le.cc:10695


```

### 3. BT of create or replace temporary sequence `create or replace temporary sequence s1`
```

0. mysql_prepare_create_table_finalize
#0  mysql_prepare_create_table_finalize (thd=0x7fffe0000d48, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, db_options=0x7ffff201a3b8, file=0x7fffe0018510, key_info_buffer=0x7ffff201ad08, key_count=0x7ffff201ad04, create_table_mode=0, db={str = 0x7fffe0017388 "test", length = 4}, table_name={str = 0x7fffe0016c08 "s1", length = 2}) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:2798
#1  0x0000555555e6511a in mysql_create_frm_image (thd=0x7fffe0000d48, db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c08 "s1", length = 2}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4333
#2  0x0000555555e66633 in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=<optimized out>, orig_db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, orig_table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c08 "s1", length = 2}, db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c08 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-33fd-3-3", length = 95}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4647
#3  0x0000555555e66da0 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, db=0x7fffe0016c90, table_name=0x7fffe0016ca0, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016c78) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#4  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016c78, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888


# 1. ha_create_table
#0  ha_create_table (thd=0x7fffe0000d48, path=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-33fd-3-3", db=0x7fffe0017388 "test", table_name=0x7fffe0016c08 "s1", create_info=0x7ffff201b300, frm=0x7ffff201ad20, skip_frm_file=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/handler.cc:6085
#1  0x0000555555e667bc in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=<optimized out>, orig_db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, orig_table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c08 "s1", length = 2}, db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c08 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-33fd-3-3", length = 95}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4671


3. create_temporary_table
#0  THD::create_temporary_table (this=0x7fffe0000d48, frm=0x7ffff201ad20, path=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-33fd-3-3", db=0x7fffe0017388 "test", table_name=0x7fffe0016c08 "s1") at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:951
#1  0x000055555600ac6e in THD::create_and_open_tmp_table (this=0x7fffe0000d48, frm=0x7ffff201ad20, path=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-33fd-3-3", db=0x7fffe0017388 "test", table_name=0x7fffe0016c08 "s1", open_internal_tables=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:71
#2  0x0000555555e668fa in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=<optimized out>, orig_db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, orig_table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c08 "s1", length = 2}, db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c08 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-33fd-3-3", length = 95}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4685

```

### BUG in SHOW FULL TABLES
```
(gdb) bt
+bt
#0  get_all_tables (thd=0x7fffe0000d48, tables=0x7fffe00173b0, cond=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:5317
#1  0x0000555555e3caa0 in get_schema_tables_result (join=join@entry=0x7fffe0017e50, executed_place=executed_place@entry=PROCESSED_BY_JOIN_EXEC) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:9131

```


### 4. Adding `CREATE OR REPLACE TEMPORARY TABLE s1` instead SEQUENCE - possible workaoround with the patch
```
0. my_message_sql
#1  0x0000555556896e8e in my_error (nr=1113, MyFlags=0) at /home/anel/GitHub/mariadb/server/src/11.2/mysys/my_error.c:124
#2  0x0000555555e664c2 in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=<optimized out>, orig_db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, orig_table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c40 "s1", length = 2}, db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c40 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-36e9-3-3", length = 95}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=-3, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4598
#3  0x0000555555e66da0 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, db=0x7fffe0016c90, table_name=0x7fffe0016ca0, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=-3, table_list=0x7fffe0016c78) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#4  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016c78, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888

```

### 5. BT of creating temporary TABLE `create temporary TABLE s1`
```

```


### 6. BT of create or replace temporary TABLE `create or replace temporary TABLE s1`
```
```



### 7. BT of alter temporary TABLE `alter TABLE s1 change t t text`
```

```

# Conclusoions

`mysql_prepare_create_table_finalize` uses `tmp_table` as false, since `C_ALTER_TABLE_FRM_ONLY (-2)` and not `C_ALTER_TABLE(-1)` when `create_info->sequence == 1`

Path:

create_table_impl->
		    mysql_create_frm_image ->
				             mysql_prepare_create_table_finalize
				                                                 -> check_sequence_fields()
				                                                 
				                                                 
				                                                
`init_tmp_table_share` (implemented in `table.cc`) is called in:
  1. `create_table_impl` create_table_mode= C_ASSISTED_DISCOVERY but we are in c_alter_frm_only mode (not in path ), paramaeter `alter_ctx.get_tmp_cstring_path()`
  2. `create_table_for_inplace_alter`  (sql_table.cc)
  3. `mysql_rm_tmp_tables` (sql_base.cc)
  4. `create_temporary_table` (temporary_tables.cc) - storing in TMP_TABLE_SHARE of *THD but for frm - here is sad that alter table doesn't have image available table::read_frm_image
  5. `ha_create_table` (handler.cc) - 
  
  
 Check `get_tmp_path\get_tmp_cstring_path` temp table returned during alter table - called from (sql_table.cc) 
 
 
 
## BUG FIX

Bug is that key_length is calculated as 31 (correct) in THD::find_temporary table that is an argument for find_temporay_table(key, key_length, state)

```
(gdb) p key
+p key
$11 =   "test\000#sql-alter-5356-3\000\001\000\000\000\003\000\000\000!\020\223\001\362\377\177\000\000\000\000\000\000\000\000\000\000\260\
302\001\362\377\177\000\000\300\301\001\362\377\177\000\000 \265\001\362\377\177\000\000\000\000\000\000\000\000\000\000\220\224\001\362\377
\177\000\000\260\342\344UUU\000\000H\r\000\340\377\177\000\000\260\302\001\362\377\177\000\000P\302\001\362\377\177\000\000\061.2/mysql-test
/var/tmp/mysqld.1/\000\000\000\000\000

+p key_length
$13 = 31
```

For each share i list of temp tables
```
+p share
$17 = (TMP_TABLE_SHARE *) 0x7fffe0015b98
(gdb) p temporary_tables
+p temporary_tables
$18 = (All_tmp_tables_list *) 0x7fffe0016278

+p this->temporary_tables
$21 = (All_tmp_tables_list *) 0x7fffe0016278  # this is actually temporary table list in THD that is filled

```

that is compared with share->table_cache_key.length (that is not valid)
```
  THD::find_temporary_table (this=this@entry=0x7fffe0000d48, key=key@entry=0x7ffff20192d0 "test", key_length=key_length@entry=31, state=st
ate@entry=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1069
(gdb) p share->table_cache_key 
+p share->table_cache_key
$14 = {
  str = 0x7fffe0016218 "test",
  length = 16
}

(gdb) p share->table_cache_key.length == key_length
+p share->table_cache_key.length == key_length
value has been optimized out


```

And table is not locked !

Looking from `mysql_rm_table_no_locks` that is called with my path by adding `mysql_no_lock` before `create_table_impl` 
is still pointing that share doesn't exist and is still calling `find_temporary_table()`.

```

(gdb) bt
+bt
#0  mysql_rm_table_no_locks (thd=0x7fffe0000d48, tables=0x7fffe0016c60, current_db=0x7fffe0000de8, ddl_log_state=0x7ffff20193d0, if_exists=true, drop_temporary=true, drop_view=false, drop_sequence=true, dont_log_query=true, dont_free_locks=true) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:1390
#1  0x0000555555e66e48 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=0x0, db=0x7ffff201b4f0, table_name=<optimized out>, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, is_trans=0x0, create_table_mode=-2, table_list=0x7fffe0016c60) at /home/anel/GitHub/mariadb/server/src/11.2/sql/handler.h:2252
#2  0x0000555555e6d96e in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005a78, new_name=new_name@entry=0x7fffe0005ec8, create_info=create_info@entry=0x7ffff201c2b0, table_list=<optimized out>, table_list@entry=0x7fffe0016c60, recreate_info=recreate_info@entry=0x7ffff201c180, alter_info=0x7ffff201c1c0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:10682
#3  0x0000555555f04be1 in Sql_cmd_alter_table::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/structs.h:568



(gdb) p table->table
+p table->table
$7 = (TABLE *) 0x7fffe001dfe8
(gdb) p table->table->s
+p table->table->s
$8 = (TABLE_SHARE *) 0x8f8f8f8f8f8f8f8f


(gdb) p *table->table
+p *table->table
$10 = {
  s = 0x8f8f8f8f8f8f8f8f,
  file = 0x8f8f8f8f8f8f8f8f,
  next = 0x8f8f8f8f8f8f8f8f,
  prev = 0x8f8f8f8f8f8f8f8f,
  share_all_next = 0x8f8f8f8f8f8f8f8f,
  share_all_prev = 0x8f8f8f8f8f8f8f8f,
  global_free_next = 0x8f8f8f8f8f8f8f8f,
  global_free_prev = 0x8f8f8f8f8f8f8f8f,
  instance = 2408550287,
  in_use = 0x8f8f8f8f8f8f8f8f,
```
Failed with `SIGSEGV` instead of `ER_SEQUENCE_INVALID_TABLE_STRUCTURE` called by `check_sequence_fields()`
 


## THD temporary tables during create temporay sequence

- It creates temporay table
```
#0  0x000055555600a7a8 in THD::create_temporary_table (this=this@entry=0x7fffe0000d48, frm=frm@entry=0x7ffff201ad20, path=<optimized out>, path@entry=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-6500-3-0", db=db@entry=0x7fffe0017300 "test", table_name=table_name@entry=0x7fffe0016b80 "s1") at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1018
#1  0x000055555600acce in THD::create_and_open_tmp_table (this=this@entry=0x7fffe0000d48, frm=frm@entry=0x7ffff201ad20, path=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-6500-3-0", db=0x7fffe0017300 "test", table_name=0x7fffe0016b80 "s1", open_internal_tables=open_internal_tables@entry=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:71
#2  0x0000555555e668fa in create_table_impl (thd=thd@entry=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_create@entry=0x7ffff201b060, ddl_log_state_rm=<optimized out>, ddl_log_state_rm@entry=0x7ffff201b080, orig_db=@0x7fffe0016c08: {str = 0x7fffe0017300 "test", length = 4}, orig_table_name=@0x7fffe0016c18: {str = 0x7fffe0016b80 "s1", length = 2}, db=@0x7fffe0016c08: {str = 0x7fffe0017300 "test", length = 4}, table_name=@0x7fffe0016c18: {str = 0x7fffe0016b80 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-6500-3-0", length = 95}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4685
#3  0x0000555555e66d9f in mysql_create_table_no_lock (thd=thd@entry=0x7fffe0000d48, ddl_log_state_create=ddl_log_state_create@entry=0x7ffff201b060, ddl_log_state_rm=ddl_log_state_rm@entry=0x7ffff201b080, db=db@entry=0x7fffe0016c08, table_name=table_name@entry=0x7fffe0016c18, create_info=create_info@entry=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016bf0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772


# There is a share


(gdb) p share
+p share
$4 = (TMP_TABLE_SHARE *) 0x7fffe0015b98


    table_cache_key = {
      str = 0x7fffe0016218 "test",
      length = 16
    },
    db = {
      str = 0x7fffe0016218 "test",
      length = 4
    },
    table_name = {
      str = 0x7fffe001621d "s1",
      length = 2
    },
    path = {
      str = 0x7fffe00161b8 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-6500-3-0",
      length = 95
    },
    normalized_path = {
      str = 0x7fffe00161b8 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-6500-3-0",
      length = 95
    },


in find_temporary_table(const char*, uint, state)
(gdb) p share
+p share
$19 = <optimized out>

It goes in while(!found )
(gdb) p found
+p found
(gdb) p table
+p table
$22 = (TABLE *) 0x7fffe001dfe8
(gdb) p state
+p state
$23 = THD::TMP_TABLE_ANY
(gdb) n
+n
(gdb) n
+n
(gdb) p found
+p found
$24 = <optimized out>

and calls
if (table && unlikely(table->needs_reopen()))                                                                        │
│   1086              {                                                                                                                    │
│   1087                share->all_tmp_tables.remove(table);

```

Monty added commit dfb41fddf69c
                TABLE *tmp_table= thd->find_temporary_table(db.str, table_name.str);
+    TABLE *tmp_table= thd->find_temporary_table(db.str, table_name.str,
+                                                THD::TMP_TABLE_ANY);

MONTY ADDed commit be647ff14d61
```
Fixed deadlock with LOCK TABLES and ALTER TABLE

if (table && unlikely(table->m_needs_reopen))
+      if (table && unlikely(table->needs_reopen()))
       {

```

It is used in mysql_prepare_alter_table ( table->mark_table_for_reopen();) that is called before `mysql_alter_table` (sql_table.cc:9885), called before create_table_impl()
```

0. mysql_prepare_alter_table

#0  mysql_prepare_alter_table (thd=0x7fffe0000d48, table=0x7fffe001dfe8, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, alter_ctx=0x7ffff201b4a0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:8032
#1  0x0000555555e6d0d9 in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005a78, new_name=new_name@entry=0x7fffe0005ec8, create_info=create_info@entry=0x7ffff201c2b0, table_list=<optimized out>, table_list@entry=0x7fffe0016c60, recreate_info=recreate_info@entry=0x7ffff201c180, alter_info=0x7ffff201c1c0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:10479
#2  0x0000555555f04b81 in Sql_cmd_alter_table::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/structs.h:568


1. create_table_impl
#0  create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=0x0, orig_db=@0x7ffff201b4b0: {str = 0x7fffe0017370 "test", length = 4}, orig_table_name=@0x7ffff201b4c0: {str = 0x7fffe0016c28 "s1", length = 2}, db=@0x7ffff201b4f0: {str = 0x7fffe0017370 "test", length = 4}, table_name=@0x7ffff201b520: {str = 0x7ffff201ba1c "#sql-alter-725e-3", length = 17}, path=@0x7ffff2019f70: {str = 0x7ffff201bedf "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-725e-3-1", length = 95}, options={m_options = DDL_options_st::OPT_NONE}, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, create_table_mode=-2, is_trans=0x0, key_info=0x7ffff2019df0, key_count=0x7ffff2019de0, frm=0x7ffff2019e20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4402
#1  0x0000555555e6d929 in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005a78, new_name=new_name@entry=0x7fffe0005ec8, create_info=create_info@entry=0x7ffff201c2b0, table_list=<optimized out>, table_list@entry=0x7fffe0016c60, recreate_info=recreate_info@entry=0x7ffff201c180, alter_info=0x7ffff201c1c0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_alter.h:302


```

TODO debug mysql_prepare_alter_table() and find out how share is optimized

- NOtes about `mysql_prepare_alter_table()`
  - `thd->calloc` uses size of fields from created sequences (it is 8 fields table->s->fields), the same is for indexes (`thd->calloc( table->s->keys))`)
    - Note that calloc takes n elements and not the size.
  - Unnecessary is created 8 elements for 1 change
  ```
	(gdb) p new_create_list
	+p new_create_list
	$14 = {
	  <base_list> = {
	    <Sql_alloc> = {<No data fields>},
	    members of base_list:
	    first = 0x7fffe0017730,
	    last = 0x7fffe0017da0,
	    elements = 8
	  }, <No data fields>}

  ```
- In case of altering - there is optimization since columns are not virtual expression, check contriant or defautl value
`  table->mark_table_for_reopen();` is called 8385 but it is not


- If alter table fails, than create field shouldn't be failed and/or restored to original file!
- Note that it was caused by Serg's patch: b1c5d7e05ec5


- Try `mysql_prepare_create_table_finalize` not to check sequence fields, since alter_info->create_fields (is optimized, but not the alter_info iteself) and is done in `mysql_prepare_alter()`
`check_sequence_fields (lex=0x7fffe00050c0, fields=<optimized out>)`
Possible problem in check_sequence_fields
```
+p sequence_structure
$25 =   {[0] = {
    field_name = 0x555556ad6aee "next_not_cached_value",
    length = 21,
    type_handler = 0x55555751f230 <type_handler_slonglong>,
    comment = {
      str = 0x555556c43f8f "",
      length = 0
    },
    flags = 4097 < to je FL (NOT_NULL_FLAG | NO_DEFAULT_VALUE_FLAG)  (1 | 4096)
  },  
  [1] = {
    field_name = 0x555556ad6b04 "minimum_value",
    length = 21,
    type_handler = 0x55555751f230 <type_handler_slonglong>,
    comment = {
      str = 0x555556c43f8f "",
      length = 0
    },
    flags = 4097
  },
  [2] = {
    field_name = 0x555556ad6b12 "maximum_value",
    length = 21,
    type_handler = 0x55555751f230 <type_handler_slonglong>,
    comment = {
      str = 0x555556c43f8f "",
      length = 0
    },
    flags = 4097
  },
  [3] = {
    field_name = 0x555556ad6b20 "start_value",
    length = 21,
    type_handler = 0x55555751f230 <type_handler_slonglong>,
    comment = {
      str = 0x555556ad7078 "start value when sequences is created or value if RESTART is used",
      length = 65
    },
    flags = 4097
  },
  [4] = {
    field_name = 0x555556cba349 "increment",
    length = 21,
    type_handler = 0x55555751f230 <type_handler_slonglong>,
    comment = {
      str = 0x555556ad6ade "increment value",
      length = 15
    },
    flags = 4097
  },
  [5] = {
    field_name = 0x555556aac535 "cache_size",
    length = 21,
    type_handler = 0x55555751f190 <type_handler_ulonglong>,
    comment = {
      str = 0x555556c43f8f "",
      length = 0
    },
    flags = 4129  FL | UNSIGNED_FLAG (4096 | 32  => 4128) 
  },
```




### Add bt in find_temporary_table
- Possible hen altering
```
(gdb) p state
+p state
$6 = THD::TMP_TABLE_NOT_IN_USE

(gdb) bt
+bt
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201ca00 "test", key_length=16, state=THD::TMP_TABLE_NOT_IN_USE) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1056
#1  0x000055555600afc3 in THD::find_and_use_tmp_table (this=0x7fffe0000d48, tl=0x7fffe0016c68, out_table=0x7ffff201cbd8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1181
#2  0x000055555600b800 in THD::open_temporary_table (this=0x7fffe0000d48, tl=0x7fffe0016c68) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:379
#3  0x000055555600b8c8 in THD::open_temporary_tables (this=0x7fffe0000d48, tl=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:476
#4  0x0000555555d6b722 in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:3806
#5  0x0000555555d575e5 in mysql_parse (thd=0x7fffe0000d48, rawbuf=<optimized out>, length=<optimized out>, parser_state=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:7769
#6  0x0000555555d66827 in dispatch_command (command=COM_QUERY, thd=0x7fffe0000d48, packet=0x7fffe000b129 "alter table s1 change cache_size cache_size text", packet_length=48, blocking=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_class.h:1371
```

This is what happens in case of `alter` and `create or replace temporary sequence` in `find_temporary_table` by deleting the temporary sequence. (NOTE TMP_TABLE_ANY and path of query)
```
alter table s1 change cache_size cache_size text;
ERROR HY000: Sequence 'test.s1' table structure is invalid (cache_size)
CREATE OR REPLACE TEMPORARY sequence s1;

Thread 6 "mariadbd" hit Breakpoint 1, THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201a280 "test", key_length=16, state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1088
1088	        free_temporary_table(table);

+bt
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201a280 "test", key_length=16, state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1088
#1  0x000055555600b0d3 in THD::find_temporary_table (this=this@entry=0x7fffe0000d48, db=<optimized out>, table_name=<optimized out>, state=state@entry=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:134
#2  0x0000555555e65ceb in create_table_impl (thd=thd@entry=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_create@entry=0x7ffff201b060, ddl_log_state_rm=0x0, ddl_log_state_rm@entry=0x7ffff201b080, orig_db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, orig_table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c08 "s1", length = 2}, db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c08 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-6877-3-3", length = 95}, options={m_options = DDL_options_st::OPT_OR_REPLACE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4458
#3  0x0000555555e66da0 in mysql_create_table_no_lock (thd=thd@entry=0x7fffe0000d48, ddl_log_state_create=ddl_log_state_create@entry=0x7ffff201b060, ddl_log_state_rm=ddl_log_state_rm@entry=0x7ffff201b080, db=db@entry=0x7fffe0016c90, table_name=table_name@entry=0x7fffe0016ca0, create_info=create_info@entry=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016c78) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#4  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016c78, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888
```



This is what happens in case of `alter` and `create or replace temporary table` in `find_temporary_table` by deleting the temporary table. (NOTE TMP_TABLE_NOT_IN_USE and path of query)
```
(gdb) bt
+bt
#0  THD::find_temporary_table (this=this@entry=0x7fffe0000d48, key=key@entry=0x7ffff201ca00 "test", key_length=16, state=state@entry=THD::TMP_TABLE_NOT_IN_USE) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1088
#1  0x000055555600afc3 in THD::find_and_use_tmp_table (this=this@entry=0x7fffe0000d48, tl=tl@entry=0x7fffe0016d08, out_table=out_table@entry=0x7ffff201cbd8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1181
#2  0x000055555600b800 in THD::open_temporary_table (this=this@entry=0x7fffe0000d48, tl=tl@entry=0x7fffe0016d08) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:379
#3  0x000055555600b8c8 in THD::open_temporary_tables (this=this@entry=0x7fffe0000d48, tl=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:476
#4  0x0000555555d6b722 in mysql_execute_command (thd=thd@entry=0x7fffe0000d48, is_called_from_prepared_stmt=is_called_from_prepared_stmt@entry=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:3806
#5  0x0000555555d575e5 in mysql_parse (thd=thd@entry=0x7fffe0000d48, rawbuf=<optimized out>, length=<optimized out>, parser_state=parser_state@entry=0x7ffff201d290) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:7769
#6  0x0000555555d66827 in dispatch_command (command=command@entry=COM_QUERY, thd=thd@entry=0x7fffe0000d48, packet=packet@entry=0x7fffe000b129 "CREATE OR REPLACE TEMPORARY table t1 (t1 int)", packet_length=packet_length@entry=45, blocking=blocking@entry=true) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_class.h:1371
```

## 1. Find out where the temporary table is reopened
Interested in `table->m_needs_reopen`

b: open_temporary_tables
   find_temporary_table
   mark_table_for_reopen
   mark_tmp_table_as_free_for_reuse
   mark_tmp_tables_as_free_for_reuse

### A) CREATE TEMPORARY TABLE t1(t int);
```
A.1. open_temporary_tables



A.2. create_table_impl
#0  create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, orig_db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, orig_table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c40 "t1", length = 2}, db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c40 "t1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19b69-3-0", length = 96}, options={m_options = DDL_options_st::OPT_NONE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4402
#1  0x0000555555e66da0 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, db=0x7fffe0016c90, table_name=0x7fffe0016ca0, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016c78) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#2  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016c78, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888
#3  Sql_cmd_create_table_like::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:12492



A.3. find_temporary_table (TMP_TABLE_ANY)
#0  THD::find_temporary_table (this=0x7fffe0000d48, db=0x7fffe0017388 "test", table_name=0x7fffe0016c40 "t1", state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:118
#1  0x0000555555e65ceb in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=0x0, orig_db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, orig_table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c40 "t1", length = 2}, db=@0x7fffe0016c90: {str = 0x7fffe0017388 "test", length = 4}, table_name=@0x7fffe0016ca0: {str = 0x7fffe0016c40 "t1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19b69-3-0", length = 96}, options={m_options = DDL_options_st::OPT_NONE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4458


A.4.mark_tmp_tables_as_free_for_reuse (table->m_needs_reopen = false)
#0  THD::mark_tmp_tables_as_free_for_reuse (this=this@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:729
#1  0x0000555555cc7681 in close_thread_tables (thd=thd@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.cc:907
#2  0x0000555555cc795d in close_thread_tables_for_query (thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.cc:792
#3  0x0000555555d7141d in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:5832


4.mark_tmp_tables_as_free_for_reuse (table->m_needs_reopen = false)
```
### B) ALTER TABLE t1 CHANGE t2 t3 int
```
B.1.  open_temporary_tables
#0  THD::open_temporary_tables (this=0x7fffe0000d48, tl=0x7fffe0016cc0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:457
#1  0x0000555555d6b722 in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:3806


B.2. find_temporary_table (from open_temporary_tables - TMP_TABLE_NOT_IN_USE)
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201ca00 "test", key_length=16, state=THD::TMP_TABLE_NOT_IN_USE) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1056
#1  0x000055555600afc3 in THD::find_and_use_tmp_table (this=0x7fffe0000d48, tl=0x7fffe0016cc0, out_table=0x7ffff201cbd8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1181
#2  0x000055555600b800 in THD::open_temporary_table (this=0x7fffe0000d48, tl=0x7fffe0016cc0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:379
#3  0x000055555600b8c8 in THD::open_temporary_tables (this=0x7fffe0000d48, tl=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:476


B.3 find_temporary_table (again, why?)
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201ca00 "test", key_length=16, state=THD::TMP_TABLE_NOT_IN_USE) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1066
#1  0x000055555600afc3 in THD::find_and_use_tmp_table (this=0x7fffe0000d48, tl=0x7fffe0016cc0, out_table=0x7ffff201cbd8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1181


```

## 2. Find out where the temporary sequence is reopened



### Latest patch
- don't mark table for reopen in alter table
Failed tests:
```
main.alter_table_errors main.temp_table

```


- With the patch the same happens for temporary tables and there is init_tmp_table_share, after freeing the temporary table in `create or replace`
```
(gdb) bt
+bt
#0  init_tmp_table_share (thd=thd@entry=0x7fffe0000d48, share=share@entry=0x7ffff2019df0, key=key@entry=0x7fffe0017418 "test", key_length=key_length@entry=0, table_name=table_name@entry=0x7fffe0016cd0 "t1", path=path@entry=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-131ed-3-2") at /home/anel/GitHub/mariadb/server/src/11.2/sql/table.cc:428
#1  0x00005555560c47af in ha_create_table (thd=thd@entry=0x7fffe0000d48, path=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-131ed-3-2", db=0x7fffe0017418 "test", table_name=0x7fffe0016cd0 "t1", create_info=create_info@entry=0x7ffff201b300, frm=frm@entry=0x7ffff201ad20, skip_frm_file=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/handler.cc:6096
#2  0x0000555555e667db in create_table_impl (thd=thd@entry=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_create@entry=0x7ffff201b060, ddl_log_state_rm=<optimized out>, ddl_log_state_rm@entry=0x7ffff201b080, orig_db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, orig_table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-131ed-3-2", length = 96}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4671
#3  0x0000555555e66dbf in mysql_create_table_no_lock (thd=thd@entry=0x7fffe0000d48, ddl_log_state_create=ddl_log_state_create@entry=0x7ffff201b060, ddl_log_state_rm=ddl_log_state_rm@entry=0x7ffff201b080, db=db@entry=0x7fffe0016d20, table_name=table_name@entry=0x7fffe0016d30, create_info=create_info@entry=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016d08) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#4  0x0000555555e68f86 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016d08, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888


# then here
(gdb) bt
+bt
#0  init_tmp_table_share (thd=0x7fffe0000d48, share=0x7fffe001cc08, key=0x7fffe001d289 "test", key_length=16, table_name=0x7fffe001d28e "t1", path=0x7fffe001d228 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-131ed-3-2") at /home/anel/GitHub/mariadb/server/src/11.2/sql/table.cc:427
#1  0x000055555600a649 in THD::create_temporary_table (this=0x7fffe0000d48, frm=0x7ffff201ad20, path=<optimized out>, db=<optimized out>, table_name=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:983
#2  0x000055555600ac8e in THD::create_and_open_tmp_table (this=this@entry=0x7fffe0000d48, frm=frm@entry=0x7ffff201ad20, path=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-131ed-3-2", db=0x7fffe0017418 "test", table_name=0x7fffe0016cd0 "t1", open_internal_tables=open_internal_tables@entry=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:71
#3  0x0000555555e66919 in create_table_impl (thd=thd@entry=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_create@entry=0x7ffff201b060, ddl_log_state_rm=<optimized out>, ddl_log_state_rm@entry=0x7ffff201b080, orig_db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, orig_table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-131ed-3-2", length = 96}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4685
#4  0x0000555555e66dbf in mysql_create_table_no_lock (thd=thd@entry=0x7fffe0000d48, ddl_log_state_create=ddl_log_state_create@entry=0x7ffff201b060, ddl_log_state_rm=ddl_log_state_rm@entry=0x7ffff201b080, db=db@entry=0x7fffe0016d20, table_name=table_name@entry=0x7fffe0016d30, create_info=create_info@entry=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016d08) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772

```

Than in `show full tables`
```

(gdb) bt
+bt
#0  init_tmp_table_share (thd=thd@entry=0x7fffe0000d48, share=0x7fffe002cad8, key=key@entry=0x555556c43f8f "", key_length=key_length@entry=0, table_name=table_name@entry=0x555556a84054 "(temporary)", path=0x7fffe002d530 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-131ed-3-3") at /home/anel/GitHub/mariadb/server/src/11.2/sql/table.cc:427
#1  0x0000555555dd9a46 in Create_tmp_table::start (this=this@entry=0x7ffff201c470, thd=thd@entry=0x7fffe0000d48, param=param@entry=0x7fffe0017bc0, table_alias=table_alias@entry=0x7fffe0017478) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_select.cc:21097
#2  0x0000555555de26d1 in create_tmp_table_for_schema (thd=thd@entry=0x7fffe0000d48, param=param@entry=0x7fffe0017bc0, schema_table=@0x555557406ac0: {table_name = 0x555556a87657 "TABLE_NAMES", fields_info = 0x5555574f76c0 <Show::table_names_fields_info>, reset_table = 0x0, fill_table = 0x555555e39a8a <get_all_tables(THD*, TABLE_LIST*, Item*)>, old_format = 0x555555e12e72 <make_table_names_old_format(THD*, st_schema_table*)>, process_table = 0x0, idx_field1 = 1, idx_field2 = 2, hidden = true, i_s_requested_object = 524288}, select_options=<optimized out>, table_alias=@0x7fffe0017478: {str = 0x7fffe0017420 "TABLE_NAMES", length = 11}, do_not_open=<optimized out>, keep_row_order=true) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_select.cc:21926
#3  0x0000555555e3b6a8 in create_schema_table (thd=thd@entry=0x7fffe0000d48, table_list=table_list@entry=0x7fffe0017430) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:8493
#4  0x0000555555e3b79a in mysql_schema_table (thd=thd@entry=0x7fffe0000d48, lex=lex@entry=0x7fffe00050c0, table_list=table_list@entry=0x7fffe0017430) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:8703
#5  0x0000555555ccfa34 in open_and_process_table (ot_ctx=0x7ffff201c700, has_prelocking_list=false, prelocking_strategy=0x7ffff201c820, flags=0, counter=0x7ffff201c79c, tables=0x7fffe0017430, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.cc:4010
#6  open_tables (thd=thd@entry=0x7fffe0000d48, options=@0x7fffe0006718: {m_options = DDL_options_st::OPT_NONE}, start=start@entry=0x7ffff201c788, counter=counter@entry=0x7ffff201c79c, flags=flags@entry=0, prelocking_strategy=prelocking_strategy@entry=0x7ffff201c820) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.cc:4625
#7  0x0000555555cd0fad in open_and_lock_tables (thd=thd@entry=0x7fffe0000d48, options=@0x7fffe0006718: {m_options = DDL_options_st::OPT_NONE}, tables=<optimized out>, tables@entry=0x7fffe0017430, derived=derived@entry=true, flags=flags@entry=0, prelocking_strategy=prelocking_strategy@entry=0x7ffff201c820) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.cc:5599
#8  0x0000555555d5de8c in open_and_lock_tables (flags=0, derived=true, tables=0x7fffe0017430, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.h:525
#9  execute_sqlcom_select (thd=thd@entry=0x7fffe0000d48, all_tables=0x7fffe0017430) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:5950

```

