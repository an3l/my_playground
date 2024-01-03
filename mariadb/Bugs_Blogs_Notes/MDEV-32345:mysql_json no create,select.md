#MDEV-32235: mysql_json cannot be used on newly created table

https://jira.mariadb.org/browse/MDEV-32235
```
open_table_def,
create_table_for_inplace_alter
                              ->init_from_binary_frm_image
```


SQLCOM_CREATE_TABLE:

mysql_execute_command->

#0  mysql_execute_command (thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_parse.cc:3524
#1  0x0000555555eae916 in mysql_parse (thd=0x7fffe0000d48, rawbuf=0x7fffe0016500 "CREATE TABLE t(j mysql_json)", length=28, parser_state=0x7ffff1cac320, is_com_multi=false, is_next_command=false) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_parse.cc:8121
#2  0x0000555555e9a654 in dispatch_command (command=COM_QUERY, thd=0x7fffe0000d48, packet=0x7fffe000aaa9 "CREATE TABLE t(j mysql_json)", packet_length=28, is_com_multi=false, is_next_command=false) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_parse.cc:1891
#3  0x0000555555e98e5e in do_command (thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_parse.cc:1375
#4  0x0000555556053fa8 in do_handle_one_connection (connect=0x555558727918, put_in_cache=true) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_connect.cc:1416
#5  0x0000555556053d0b in handle_one_connection (arg=0x555558727918) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_connect.cc:1318
#6  0x0000555556582ae9 in pfs_spawn_thread (arg=0x55555872ebf8) at /home/anel/GitHub/mariadb/server/src/10.5/storage/perfschema/pfs.cc:2201
#7  0x00007ffff79e1609 in start_thread (arg=<optimized out>) at pthread_create.c:477
#8  0x00007ffff75b2133 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:95


#0  mysql_execute_command (thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_parse.cc:3524
#1  0x0000555555eae916 in mysql_parse (thd=0x7fffe0000d48, rawbuf=0x7fffe0016500 "CREATE TABLE t(j mysql_json)", length=28, parser_state=0x7ffff1cac320, is_com_multi=false, is_next_command=false) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_parse.cc:8121
#2  0x0000555555e9a654 in dispatch_command (command=COM_QUERY, thd=0x7fffe0000d48, packet=0x7fffe000aaa9 "CREATE TABLE t(j mysql_json)", packet_length=28, is_com_multi=false, is_next_command=false) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_parse.cc:1891
#3  0x0000555555e98e5e in do_command (thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_parse.cc:1375
#4  0x0000555556053fa8 in do_handle_one_connection (connect=0x555558727918, put_in_cache=true) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_connect.cc:1416
#5  0x0000555556053d0b in handle_one_connection (arg=0x555558727918) at /home/anel/GitHub/mariadb/server/src/10.5/sql/sql_connect.cc:1318
#6  0x0000555556582ae9 in pfs_spawn_thread (arg=0x55555872ebf8) at /home/anel/GitHub/mariadb/server/src/10.5/storage/perfschema/pfs.cc:2201
#7  0x00007ffff79e1609 in start_thread (arg=<optimized out>) at pthread_create.c:477
#8  0x00007ffff75b2133 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:95

+p *lex->m_sql_cmd
$8 = {
  <Sql_alloc> = {<No data fields>},
  members of Sql_cmd:
  _vptr.Sql_cmd = 0x555557556908 <vtable for Sql_cmd_create_table+16>
}

  12134       bool Sql_cmd_create_table_like::execute(THD *thd)                                                                                                                                                                                                                │
│   12135       {                                                                                                                                                                                                                                                                │
│  >12136         DBUG_ENTER("Sql_cmd_create_table::execute");  


mysql_create_table() -> mysql_create_table_no_lock() -> create_table)_impl() -> (ordinary create)mysql_create_frm_image() -> mysql_prepare_create_table() [1]
                                                                                                                          -> build_frm_image
                                                                                                                          
In [1] there is check of `sql_field`
```
(gdb) p *sql_field
+p *sql_field
$15 = {
  <Column_definition> = {
    <Sql_alloc> = {<No data fields>}, 
    <Type_handler_hybrid_field_type> = {
      m_type_handler = 0x7ffff2fca160 <type_handler_mysql_json> # <<<
    }, 
    <Column_definition_attributes> = {
      length = 0,
      decimals = 0,
      unireg_check = Field::NONE,
      interval = 0x0,
      charset = 0x555557696ec0 <my_charset_bin>,
      srid = 0,
      pack_flag = 0
    }, 
    members of Column_definition:
    compression_method_ptr = 0x0,
    field_name = {
      <Lex_cstring> = {
        <st_mysql_const_lex_string> = {
          str = 0x7fffe0016d00 "j",
          length = 1
        }, <No data fields>}, <No data fields>},
    comment = {
      str = 0x0,
      length = 0
    },
    on_update = 0x0,
    invisible = VISIBLE,
    char_length = 0,
    flags = 16,
    pack_length = 0,
    interval_list = {
      <base_list> = {
        <Sql_alloc> = {<No data fields>}, 
        members of base_list:
        first = 0x555557856cf0 <end_of_list>,
        last = 0x7fffe0016ea8,
        elements = 0
      }, <No data fields>},
    option_list = 0x0,
    explicitly_nullable = false,
    vcol_info = 0x0,
    default_value = 0x0,
    check_constraint = 0x0,
    versioning = Column_definition::VERSIONING_NOT_SET,
    period = 0x0
  }, 
  members of Create_field:
  change = {
    str = 0x0,
    length = 0
  },
  after = {
    str = 0x0,
    length = 0
  },
  field = 0x0,
  save_interval = 0xa5a5a5a5a5a5a5a5,
  option_struct = 0x0,
  offset = 2779096485,
  interval_id = 165 '\245',
  create_if_not_exists = false
}

+p *sql_field->m_type_handler
$17 = {
  _vptr.Type_handler = 0x7ffff2fc8cf8 <vtable for Type_handler_mysql_json+16>,
  m_name = {
    <st_mysql_const_lex_string> = {
      str = 0x7ffff2fc3f08 "MYSQL_JSON",
      length = 10
    }, <No data fields>}
}

(gdb) p sql_field->m_type_handler->m_name
+p sql_field->m_type_handler->m_name
$19 = {
  <st_mysql_const_lex_string> = {
    str = 0x7ffff2fc3f08 "MYSQL_JSON",
    length = 10
  }, <No data fields>}

+p sql_field->m_type_handler->m_name.str
$20 = 0x7ffff2fc3f08 "MYSQL_JSON"


(gdb) p sql_field->real_field_type()
+p sql_field->real_field_type()
$24 = MYSQL_TYPE_BLOB
```
