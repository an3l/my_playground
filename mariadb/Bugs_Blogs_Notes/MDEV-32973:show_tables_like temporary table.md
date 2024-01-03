# MDEV-32973: show tables like temporary 
-https://jira.mariadb.org/browse/MDEV-32973
- It works for real table, but not for base table
  - Reason is because `IS_table_read_plan` is created and filled with wild_db_value, wild_table_value 
    where in function `optimize_for_get_all_tables` checks are done.
    Since it is not wildcard on DB, it partial_cond and `make_cond_for_info_schema` is called that is NULL.
  - Reason `get_schema_tables_record1` not called for real table
    - In yacc `show`, `show_param` rules
    - `SQLCOM_SHOW_TABLES` (sql/sql_parse.cc|mysqld.cc|sql_show.cc|sql_prepare.cc)
      - mysqld.cc (`show_table_definitions`) - not invoked in real table
      - sql_show.cc 
        - calls get_lookup_field_values - find wild and checks for lowercase
       `get_lookup_field_values -> make_lex_string() | lookup_field_values->wild_table_value=1`
        ```
        # Temporary table (make_lex_string)
        +p *lookup_field_values
	$3 = {
	  db_value = {
	    str = 0x0,
	    length = 0
	  },
	  table_value = {
	    str = 0x0,
	    length = 0
	  },
	  wild_db_value = false,
	  wild_table_value = false
	}
	+p *wild
	$7 = {
	  <Charset> = {
	    m_charset = 0x55555b6f9be0 <my_charset_utf8mb3_general_ci>
	  }, 
	  <Binary_string> = {
	    <Sql_alloc> = {<No data fields>}, 
	    members of Binary_string:
	    Ptr = 0x6290000e62f8 "%pt%",
	    str_length = 4,
	    Alloced_length = 0,
	    extra_alloc = 0,
	    alloced = false,
	    thread_specific = false
	  }, <No data fields>}
	  # Above update lookup_field_values
	  table_value = {
	    str = 0x6290000e9e60 "%pt%",
	    length = 4
	  },
	  wild_db_value = false,
	  wild_table_value = true
}
        ```
        - bt
        ```
	#0  get_lookup_field_values (thd=0x62c0000c0218, cond=0x0, fix_table_name_case=true, tables=0x6290000e6a10, lookup_field_values=0x6290000e9e18) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:4329
	#1  0x00005555574100df in optimize_for_get_all_tables (thd=0x62c0000c0218, tables=0x6290000e6a10, cond=0x0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:9038
	#2  0x0000555557411dcc in optimize_schema_tables_reads (join=0x6290000e74e0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:9191
        ```
- Plan looks like
```
+p *plan
$3 = {
  <Sql_alloc> = {<No data fields>}, 
  members of IS_table_read_plan:
  no_rows = false,
  trivial_show_command = false,
  lookup_field_vals = {
    db_value = {
      str = 0x6290000e9e88 "test",
      length = 4
    },
    table_value = {
      str = 0x6290000e9e98 "faketable",
      length = 9
    },
    wild_db_value = false,
    wild_table_value = true
  },
  partial_cond = 0x0
}
```
        
Different paths for temporary table with/without lookup
A) like `faketable`
1. called `get_lookup_field_values`
```
+bt
#0  get_lookup_field_values (thd=0x6130000500d8, cond=0x606000015fe0, fix_table_name_case=85, tables=0x7fffec176bb0, lookup_field_values=0x61300004ff80) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:4292
#1  0x00005555574100df in optimize_for_get_all_tables (thd=0x62c0000c0218, tables=0x6290000e6a48, cond=0x0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:9038
#2  0x0000555557411dcc in optimize_schema_tables_reads (join=0x6290000e7518) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:9191
#3  0x00005555572b9d25 in JOIN::optimize_stage2 (this=0x6290000e7518) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_select.cc:3225
#4  0x00005555572b3eb2 in JOIN::optimize_inner (this=0x6290000e7518) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_select.cc:2672
#5  0x00005555572aca96 in JOIN::optimize (this=0x6290000e7518) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_select.cc:1966
#6  0x00005555572cee54 in mysql_select (thd=0x62c0000c0218, tables=0x6290000e6a48, fields=@0x62c0000c5240: {<base_list> = {<Sql_alloc> = {<No data fields>}, first = 0x6290000e6990, last = 0x6290000e6990, elements = 1}, <No data fields>}, conds=0x0, og_num=0, order=0x0, group=0x0, having=0x0, proc_param=0x0, select_options=2701396736, result=0x6290000e74e8, unit=0x62c0000c4750, select_lex=0x62c0000c4f88) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_select.cc:5287
#7  0x000055555729ddd8 in handle_select (thd=0x62c0000c0218, lex=0x62c0000c4670, result=0x6290000e74e8, setup_tables_done_option=0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_select.cc:630
#8  0x00005555571bf873 in execute_sqlcom_select (thd=0x62c0000c0218, all_tables=0x6290000e6a48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:6066
#9  0x00005555571b04c5 in mysql_execute_command (thd=0x62c0000c0218, is_called_from_prepared_stmt=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:3957
#10 0x00005555571ca757 in mysql_parse (thd=0x62c0000c0218, rawbuf=0x6290000e6238 "SHOW TABLES LIKE 'faketable'", length=28, parser_state=0x7fffec1787f0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:7808
#11 0x00005555571a2a60 in dispatch_command (command=COM_QUERY, thd=0x62c0000c0218, packet=0x6290000dc219 "SHOW TABLES LIKE 'faketable'", packet_length=28, blocking=true) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:1893
#12 0x000055555719f7aa in do_command (thd=0x62c0000c0218, blocking=true) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_parse.cc:1406
#13 0x0000555557680b08 in do_handle_one_connection (connect=0x6080000020b8, put_in_cache=true) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_connect.cc:1418
#14 0x0000555557680465 in handle_one_connection (arg=0x6080000020b8) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_connect.cc:1320
#15 0x00005555582f8464 in pfs_spawn_thread (arg=0x617000004a18) at /home/anel/GitHub/mariadb/server/src/11.2/storage/perfschema/pfs.cc:2201
#16 0x00007ffff6ffa609 in start_thread (arg=<optimized out>) at pthread_create.c:477
#17 0x00007ffff6bcb353 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:95
```

2. `get_all_tables`
```
(gdb) bt
+bt
#0  get_all_tables (thd=0x7fffec1760c8, tables=0x7fffec179ce8, cond=0x0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:5241
#1  0x0000555557412bb7 in get_schema_tables_result (join=0x6290000e74e0, executed_place=PROCESSED_BY_JOIN_EXEC) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_show.cc:9314
#2  0x00005555572ccb4f in JOIN::exec_inner (this=0x6290000e74e0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_select.cc:4943
#3  0x00005555572ca7da in JOIN::exec (this=0x6290000e74e0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_select.cc:4763

```
