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


A.5. mark_tmp_tables_as_free_for_reuse (table->m_needs_reopen = false)
```
### B) ALTER TABLE t1 CHANGE t2 t3 int (error)
```
B.1.  open_temporary_tables
#0  THD::open_temporary_tables (this=0x7fffe0000d48, tl=0x7fffe0016cc0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:457
#1  0x0000555555d6b722 in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:3806


B.2. find_temporary_table (from open_temporary_tables - TMP_TABLE_NOT_IN_USE)
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201ca00 "test", key_length=16, state=THD::TMP_TABLE_NOT_IN_USE) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1056
#1  0x000055555600afc3 in THD::find_and_use_tmp_table (this=0x7fffe0000d48, tl=0x7fffe0016cc0, out_table=0x7ffff201cbd8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1181
#2  0x000055555600b800 in THD::open_temporary_table (this=0x7fffe0000d48, tl=0x7fffe0016cc0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:379
#3  0x000055555600b8c8 in THD::open_temporary_tables (this=0x7fffe0000d48, tl=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:476


B.3 find_temporary_table (again, why?) - Iterator?
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201ca00 "test", key_length=16, state=THD::TMP_TABLE_NOT_IN_USE) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1066
#1  0x000055555600afc3 in THD::find_and_use_tmp_table (this=0x7fffe0000d48, tl=0x7fffe0016cc0, out_table=0x7ffff201cbd8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1181


B.4 mark_table_for_reopen (table->m_needs_reopen = true) <HEY>
#0  TABLE::mark_table_for_reopen (this=0x7fffe001d408) at /home/anel/GitHub/mariadb/server/src/11.2/sql/table.cc:10625
#1  0x0000555555e5cd6c in mysql_prepare_alter_table (thd=0x7fffe0000d48, table=0x7fffe001d408, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, alter_ctx=0x7ffff201b4a0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:8385
#2  0x0000555555e6d0d9 in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005a78, new_name=new_name@entry=0x7fffe0005ec8, create_info=create_info@entry=0x7ffff201c2b0, table_list=<optimized out>, table_list@entry=0x7fffe0016cc0, recreate_info=recreate_info@entry=0x7ffff201c180, alter_info=0x7ffff201c1c0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:10479
#3  0x0000555555f04b81 in Sql_cmd_alter_table::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/structs.h:568
#4  0x0000555555d70a4f in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:5766
#5  0x0000555555d575e5 in mysql_parse (thd=0x7fffe0000d48, rawbuf=<optimized out>, length=<optimized out>, parser_state=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:7769
#6  0x0000555555d66827 in dispatch_command (command=COM_QUERY, thd=0x7fffe0000d48, packet=0x7fffe000b129 "alter table t1 change t2 t3 int", packet_length=31, blocking=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_class.h:1371

B.5. my_message_sql
#2  0x0000555555e5f50b in mysql_prepare_alter_table (thd=0x7fffe0000d48, table=0x7fffe001d408, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, alter_ctx=0x7ffff201b4a0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:8429
#3  0x0000555555e6d0d9 in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005a78, new_name=new_name@entry=0x7fffe0005ec8, create_info=create_info@entry=0x7ffff201c2b0, table_list=<optimized out>, table_list@entry=0x7fffe0016cc0, recreate_info=recreate_info@entry=0x7ffff201c180, alter_info=0x7ffff201c1c0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:10479
#4  0x0000555555f04b81 in Sql_cmd_alter_table::execut

B.6.mark_tmp_tables_as_free_for_reuse
#0  THD::mark_tmp_tables_as_free_for_reuse (this=this@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:729
#1  0x0000555555cc7681 in close_thread_tables (thd=thd@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.cc:907
#2  0x0000555555cc795d in close_thread_tables_for_query (thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.cc:792
#3  0x0000555555d7141d in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:5832

B.7.mark_tmp_table_as_free_for_reuse
#0  THD::mark_tmp_table_as_free_for_reuse (this=0x7fffe0000d48, table=0x7fffe001d408) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:791
#1  0x000055555600a1bb in THD::mark_tmp_tables_as_free_for_reuse (this=this@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:759
```

### C) CREATE OR REPLACE TEMPORARY TABLE t1;
```
C.1 open_temporary_tables
#0  THD::open_temporary_tables (this=0x7fffe0000d48, tl=0x7fffe0016d08) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_table
s.cc:457
#1  0x0000555555d6b722 in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/
mariadb/server/src/11.2/sql/sql_parse.cc:3806
#2  0x0000555555d575e5 in mysql_parse (thd=0x7fffe0000d48, rawbuf=<optimized out>, length=<optimized out>, parser_state=<optimized out>)
 at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:7769
#3  0x0000555555d66827 in dispatch_command (command=COM_QUERY, thd=0x7fffe0000d48, packet=0x7fffe000b129 "CREATE OR REPLACE TEMPORARY ta
ble t1 (t1 int)", packet_length=45, blocking=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_class.h:1371

C.2.find_temporary_table (TMP_TABLE_NOT_IN_USE)
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201ca00 "test", key_length=16, state=THD::TMP_TABLE_NOT_IN_USE) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1056
#1  0x000055555600afc3 in THD::find_and_use_tmp_table (this=0x7fffe0000d48, tl=0x7fffe0016d08, out_table=0x7ffff201cbd8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1181
#2  0x000055555600b800 in THD::open_temporary_table (this=0x7fffe0000d48, tl=0x7fffe0016d08) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:379

C.3.find_temporary_table (again, TMP_TABLE_NOT_IN_USE) - Iterator?
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201ca00 "test", key_length=16, state=THD::TMP_TABLE_NOT_IN_USE) at /home/
anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1066
#1  0x000055555600afc3 in THD::find_and_use_tmp_table (this=0x7fffe0000d48, tl=0x7fffe0016d08, out_table=0x7ffff201cbd8) at /home/anel/G
itHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1181

C.4. find_temporary_table(remove table), since it is set!, will be reseted in all_tmp_tables.remove(table)
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201ca00 "test", key_length=16, state=THD::TMP_TABLE_NOT_IN_USE) at /home/
anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1087

C.4.1. open_table_from_share
#0  open_table_from_share (thd=0x7fffe0000d48, share=0x7fffe0015858, alias=0x7ffff201cb70, db_stat=<optimized out>, prgflag=<optimized out>, ha_open_flags=<optimized out>, outparam=<optimized out>, is_create_table=<optimized out>, partitions_to_open=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/table.cc:4210
#1  0x00005555560089a9 in THD::open_temporary_table (this=0x7fffe0000d48, share=0x7fffe0015858, alias_arg=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1131
#2  0x000055555600b5b5 in THD::open_temporary_table (this=0x7fffe0000d48, tl=0x7fffe0016d08) at /home/anel/GitHub/mariadb/server/src/11.2/sql/table.h:3018
#3  0x000055555600b8c8 in THD::open_temporary_tables (this=0x7fffe0000d48, tl=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:476


C.5 create_table_impl
#0  create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, orig_db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, orig_table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19b69-3-2", length = 96}, options={m_options = DDL_options_st::OPT_OR_REPLACE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4402
#1  0x0000555555e66da0 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, db=0x7fffe0016d20, table_name=0x7fffe0016d30, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016d08) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#2  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016d08, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888
#3  Sql_cmd_create_table_like::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:12492
#4  0x0000555555d70a4f in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:5766
#5  0x0000555555d575e5 in mysql_parse (thd=0x7fffe0000d48, rawbuf=<optimized out>, length=<optimized out>, parser_state=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:7769
#6  0x0000555555d66827 in dispatch_command (command=COM_QUERY, thd=0x7fffe0000d48, packet=0x7fffe000b129 "CREATE OR REPLACE TEMPORARY table t1 (t1 int)", packet_length=45, blocking=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_class.h:1371


C.6 find_temporary_table
#0  THD::find_temporary_table (this=0x7fffe0000d48, db=0x7fffe0017418 "test", table_name=0x7fffe0016cd0 "t1", state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:118
#1  0x0000555555e65ceb in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=0x0, orig_db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, orig_table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19b69-3-2", length = 96}, options={m_options = DDL_options_st::OPT_OR_REPLACE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4458
#2  0x0000555555e66da0 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, db=0x7fffe0016d20, table_name=0x7fffe0016d30, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016d08) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#3  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016d08, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888
#4  Sql_cmd_create_table_like::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:12492


C.7 find_temporary_table
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201a280 "test", key_length=16, state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1056
#1  0x000055555600b0d3 in THD::find_temporary_table (this=0x7fffe0000d48, db=<optimized out>, table_name=<optimized out>, state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:134
#2  0x0000555555e65ceb in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=0x0, orig_db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, orig_table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19b69-3-2", length = 96}, options={m_options = DDL_options_st::OPT_OR_REPLACE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4458

C.8.find_temporary_table (again)
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201a280 "test", key_length=16, state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1066
#1  0x000055555600b0d3 in THD::find_temporary_table (this=0x7fffe0000d48, db=<optimized out>, table_name=<optimized out>, state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:134

C.8.1. delete
(gdb) bt
+bt
#0  __memset_avx2_unaligned_erms () at ../sysdeps/x86_64/multiarch/memset-vec-unaligned-erms.S:216
#1  0x000055555689d991 in memset (__len=960, __ch=143, __dest=0x7fffe001d408) at /usr/include/x86_64-linux-gnu/bits/string_fortified.h:71
#2  my_free (ptr=0x7fffe001d408) at /home/anel/GitHub/mariadb/server/src/11.2/mysys/my_malloc.c:211
#3  0x0000555556008d54 in THD::close_temporary_table (this=0x7fffe0000d48, table=0x7fffe001d408) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1252
#4  0x00005555560098da in THD::free_temporary_table (this=0x7fffe0000d48, table=0x7fffe001d408) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1502
#5  0x000055555600aa52 in THD::drop_temporary_table (this=0x7fffe0000d48, table=<optimized out>, is_trans=0x0, delete_table=true) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:665
#6  0x0000555555e65de0 in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=<optimized out>, orig_db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, orig_table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19b69-3-2", length = 96}, options={m_options = DDL_options_st::OPT_OR_REPLACE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4470

C.8.2 malloc  table->m_needs_reopen
#0  __memset_avx2_unaligned_erms () at ../sysdeps/x86_64/multiarch/memset-vec-unaligned-erms.S:216
#1  0x000055555689d87e in memset (__len=960, __ch=165, __dest=0x7fffe001d408) at /usr/include/x86_64-linux-gnu/bits/string_fortified.h:71
#2  my_malloc (key=62, size=960, my_flags=16) at /home/anel/GitHub/mariadb/server/src/11.2/mysys/my_malloc.c:114
#3  0x0000555556008966 in THD::open_temporary_table (this=0x7fffe0000d48, share=0x7fffe001cc08, alias_arg=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1125
#4  0x000055555600ac92 in THD::create_and_open_tmp_table (this=0x7fffe0000d48, frm=<optimized out>, path=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19b69-3-2", db=0x7fffe0017418 "test", table_name=0x7fffe0016cd0 "t1", open_internal_tables=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:74
#5  0x0000555555e668fa in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=<optimized out>, orig_db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, orig_table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19b69-3-2", length = 96}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4685

C.8.3
#0  0x0000555555eaf5e6 in memset (__len=960, __ch=0, __dest=0x7fffe001d408) at /usr/include/x86_64-linux-gnu/bits/string_fortified.h:71
#1  open_table_from_share (thd=0x7fffe0000d48, share=0x7fffe001cc08, alias=0x7ffff201a380, db_stat=<optimized out>, prgflag=<optimized out>, ha_open_flags=<optimized out>, outparam=<optimized out>, is_create_table=<optimized out>, partitions_to_open=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/table.cc:4209
#2  0x00005555560089a9 in THD::open_temporary_table (this=0x7fffe0000d48, share=0x7fffe001cc08, alias_arg=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1131
#3  0x000055555600ac92 in THD::create_and_open_tmp_table (this=0x7fffe0000d48, frm=<optimized out>, path=0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19b69-3-2", db=0x7fffe0017418 "test", table_name=0x7fffe0016cd0 "t1", open_internal_tables=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:74
#4  0x0000555555e668fa in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=<optimized out>, orig_db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, orig_table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, db=@0x7fffe0016d20: {str = 0x7fffe0017418 "test", length = 4}, table_name=@0x7fffe0016d30: {str = 0x7fffe0016cd0 "t1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19b69-3-2", length = 96}, options=<optimized out>, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4685
#5  0x0000555555e66da0 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, db=0x7fffe0016d20, table_name=0x7fffe0016d30, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016d08) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#6  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016d08, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888


C.9. mark_tmp_tables_as_free_for_reuse
#0  THD::mark_tmp_tables_as_free_for_reuse (this=this@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_t
ables.cc:729
#1  0x0000555555cc7681 in close_thread_tables (thd=thd@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.c
c:907
#2  0x0000555555cc795d in close_thread_tables_for_query (thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.c
c:792

C.10 mark_tmp_table_as_free_for_reuse
#0  THD::mark_tmp_table_as_free_for_reuse (this=0x7fffe0000d48, table=0x7fffe001d408) at /home/anel/GitHub/mariadb/server/src/11.2/sql/t
emporary_tables.cc:791
#1  0x000055555600a1bb in THD::mark_tmp_tables_as_free_for_reuse (this=this@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/sr
c/11.2/sql/temporary_tables.cc:759
```

### D) show full tables
```
D.1. mark_tmp_tables_as_free_for_reuse
#0  THD::mark_tmp_tables_as_free_for_reuse (this=this@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_t
ables.cc:729
#1  0x0000555555cc7681 in close_thread_tables (thd=thd@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.c
c:907
#2  0x0000555555cc795d in close_thread_tables_for_query (thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.c
c:792
#3  0x0000555555d7141d in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/
mariadb/server/src/11.2/sql/sql_parse.cc:5832

```


## 2. Find out where the temporary sequence is reopened

### A) create temporary sequence s1;
```
A.1 create_table_impl
#0  create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, orig_db=@0x7fffe0016c88: {str = 0x7fffe0017380 "test", length = 4}, orig_table_name=@0x7fffe0016c98: {str = 0x7fffe0016c00 "s1", length = 2}, db=@0x7fffe0016c88: {str = 0x7fffe0017380 "test", length = 4}, table_name=@0x7fffe0016c98: {str = 0x7fffe0016c00 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19f70-3-0", length = 96}, options={m_options = DDL_options_st::OPT_NONE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4402
#1  0x0000555555e66da0 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, db=0x7fffe0016c88, table_name=0x7fffe0016c98, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016c70) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#2  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016c70, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888
#3  Sql_cmd_create_table_like::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:12492
#4  0x0000555555d70a4f in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:5766
#5  0x0000555555d575e5 in mysql_parse (thd=0x7fffe0000d48, rawbuf=<optimized out>, length=<optimized out>, parser_state=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:7769
#6  0x0000555555d66827 in dispatch_command (command=COM_QUERY, thd=0x7fffe0000d48, packet=0x7fffe000b129 "create temporary sequence s1", packet_length=28, blocking=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_class.h:1371


A.2 find_temporary_table
#0  THD::find_temporary_table (this=0x7fffe0000d48, db=0x7fffe0017380 "test", table_name=0x7fffe0016c00 "s1", state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:118
#1  0x0000555555e65ceb in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=0x0, orig_db=@0x7fffe0016c88: {str = 0x7fffe0017380 "test", length = 4}, orig_table_name=@0x7fffe0016c98: {str = 0x7fffe0016c00 "s1", length = 2}, db=@0x7fffe0016c88: {str = 0x7fffe0017380 "test", length = 4}, table_name=@0x7fffe0016c98: {str = 0x7fffe0016c00 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19f70-3-0", length = 96}, options={m_options = DDL_options_st::OPT_NONE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4458
#2  0x0000555555e66da0 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, db=0x7fffe0016c88, table_name=0x7fffe0016c98, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016c70) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#3  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016c70, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888

A.3. mark_tmp_tables_as_free_for_reuse

```

### B) alter table s1 change cache_size cache_size text; (error)
```
B.1. open_temporary_tables
#0  THD::open_temporary_tables (this=0x7fffe0000d48, tl=0x7fffe0016ce8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:457
#1  0x0000555555d6b722 in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:3806

B.2. find_temporary_table
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201ca00 "test", key_length=16, state=THD::TMP_TABLE_NOT_IN_USE) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1056
#1  0x000055555600afc3 in THD::find_and_use_tmp_table (this=0x7fffe0000d48, tl=0x7fffe0016ce8, out_table=0x7ffff201cbd8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1181
#2  0x000055555600b800 in THD::open_temporary_table (this=0x7fffe0000d48, tl=0x7fffe0016ce8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:379
#3  0x000055555600b8c8 in THD::open_temporary_tables (this=0x7fffe0000d48, tl=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:476

B.3. mark_table_for_reopen (<HEY> This should be ON)
#0  TABLE::mark_table_for_reopen (this=0x7fffe001e068) at /home/anel/GitHub/mariadb/server/src/11.2/sql/table.cc:10625
#1  0x0000555555e5cd6c in mysql_prepare_alter_table (thd=0x7fffe0000d48, table=0x7fffe001e068, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, alter_ctx=0x7ffff201b4a0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:8385
#2  0x0000555555e6d0d9 in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005a78, new_name=new_name@entry=0x7fffe0005ec8, create_info=create_info@entry=0x7ffff201c2b0, table_list=<optimized out>, table_list@entry=0x7fffe0016ce8, recreate_info=recreate_info@entry=0x7ffff201c180, alter_info=0x7ffff201c1c0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:10479
#3  0x0000555555f04b81 in Sql_cmd_alter_table::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/structs.h:568
#4  0x0000555555d70a4f in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:5766

B.4. create_table_impl
#0  create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=0x0, orig_db=@0x7ffff201b4b0: {str = 0x7fffe00173f8 "test", length = 4}, orig_table_name=@0x7ffff201b4c0: {str = 0x7fffe0016cb0 "s1", length = 2}, db=@0x7ffff201b4f0: {str = 0x7fffe00173f8 "test", length = 4}, table_name=@0x7ffff201b520: {str = 0x7ffff201ba1c "#sql-alter-19f70-3", length = 18}, path=@0x7ffff2019f70: {str = 0x7ffff201bedf "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19f70-3-2", length = 96}, options={m_options = DDL_options_st::OPT_NONE}, create_info=0x7ffff201c2b0, alter_info=0x7ffff201c1c0, create_table_mode=-2, is_trans=0x0, key_info=0x7ffff2019df0, key_count=0x7ffff2019de0, frm=0x7ffff2019e20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4402
#1  0x0000555555e6d929 in mysql_alter_table (thd=thd@entry=0x7fffe0000d48, new_db=new_db@entry=0x7fffe0005a78, new_name=new_name@entry=0x7fffe0005ec8, create_info=create_info@entry=0x7ffff201c2b0, table_list=<optimized out>, table_list@entry=0x7fffe0016ce8, recreate_info=recreate_info@entry=0x7ffff201c180, alter_info=0x7ffff201c1c0, order_num=0, order=0x0, ignore=false, if_exists=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_alter.h:302


```

### C) CREATE OR REPLACE TEMPORARY sequence s1;
```
C.1. create_table_impl
#0  create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, orig_db=@0x7fffe0016d10: {str = 0x7fffe0017408 "test", length = 4}, orig_table_name=@0x7fffe0016d20: {str = 0x7fffe0016c88 "s1", length = 2}, db=@0x7fffe0016d10: {str = 0x7fffe0017408 "test", length = 4}, table_name=@0x7fffe0016d20: {str = 0x7fffe0016c88 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19f70-3-3", length = 96}, options={m_options = DDL_options_st::OPT_OR_REPLACE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4402
#1  0x0000555555e66da0 in mysql_create_table_no_lock (thd=0x7fffe0000d48, ddl_log_state_create=0x7ffff201b060, ddl_log_state_rm=0x7ffff201b080, db=0x7fffe0016d10, table_name=0x7fffe0016d20, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, is_trans=0x7ffff201b040, create_table_mode=0, table_list=0x7fffe0016cf8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4772
#2  0x0000555555e68f66 in mysql_create_table (alter_info=0x7ffff201b120, create_info=0x7ffff201b300, create_table=0x7fffe0016cf8, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4888


C.2.find_temporary_table
#0  THD::find_temporary_table (this=0x7fffe0000d48, db=0x7fffe0017408 "test", table_name=0x7fffe0016c88 "s1", state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:118
#1  0x0000555555e65ceb in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=0x0, orig_db=@0x7fffe0016d10: {str = 0x7fffe0017408 "test", length = 4}, orig_table_name=@0x7fffe0016d20: {str = 0x7fffe0016c88 "s1", length = 2}, db=@0x7fffe0016d10: {str = 0x7fffe0017408 "test", length = 4}, table_name=@0x7fffe0016d20: {str = 0x7fffe0016c88 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19f70-3-3", length = 96}, options={m_options = DDL_options_st::OPT_OR_REPLACE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4458

C.3.1 find_temporary_table
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201a280 "test", key_length=16, state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1056
#1  0x000055555600b0d3 in THD::find_temporary_table (this=0x7fffe0000d48, db=<optimized out>, table_name=<optimized out>, state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:134
#2  0x0000555555e65ceb in create_table_impl (thd=0x7fffe0000d48, ddl_log_state_create=0x0, ddl_log_state_rm=0x0, orig_db=@0x7fffe0016d10: {str = 0x7fffe0017408 "test", length = 4}, orig_table_name=@0x7fffe0016d20: {str = 0x7fffe0016c88 "s1", length = 2}, db=@0x7fffe0016d10: {str = 0x7fffe0017408 "test", length = 4}, table_name=@0x7fffe0016d20: {str = 0x7fffe0016c88 "s1", length = 2}, path=@0x7ffff201ad10: {str = 0x7ffff201ad30 "/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/tmp/mysqld.1/#sql-temptable-19f70-3-3", length = 96}, options={m_options = DDL_options_st::OPT_OR_REPLACE}, create_info=0x7ffff201b300, alter_info=0x7ffff201b120, create_table_mode=0, is_trans=0x7ffff201b040, key_info=0x7ffff201ad08, key_count=0x7ffff201ad04, frm=0x7ffff201ad20) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:4458

C.3.2. find_temporary_table(again)
#0  THD::find_temporary_table (this=0x7fffe0000d48, key=0x7ffff201a280 "test", key_length=16, state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:1066
#1  0x000055555600b0d3 in THD::find_temporary_table (this=0x7fffe0000d48, db=<optimized out>, table_name=<optimized out>, state=THD::TMP_TABLE_ANY) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:134

C.4. mark_tmp_tables_as_free_for_reuse

#0  THD::mark_tmp_tables_as_free_for_reuse (this=this@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/temporary_tables.cc:729
#1  0x0000555555cc7681 in close_thread_tables (thd=thd@entry=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.cc:907
#2  0x0000555555cc795d in close_thread_tables_for_query (thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.cc:792
#3  0x0000555555d7141d in mysql_execute_command (thd=0x7fffe0000d48, is_called_from_prepared_stmt=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:5832

```

### D) show full tables
```
```

