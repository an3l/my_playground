# MTR
MDEV-31541
start mtr with `./mtr test --debug`
there will be 
```
select @@debug_dbug;
@@debug_dbug
d,*:i:A,/home/anel/GitHub/mariadb/server/build/11.2/mysql-test/var/log/mysqld.1.trace:t
```
Options: https://mariadb.com/kb/en/mysql_debug/

build_table_filename
- `sql/sql_yacc.yy` calls `thd->lex` -> `lex->m_sql_cmd= new Sql_cmd_create_table` -> `lex->create_info.init()` (sql_lex.h) < so init is called in lexer
0. `Sql_cmd_create_table::execute` - > `myql_create_table`
1.  mysql_create_table  (Table_specification_st *)-> 
                        |1.--> open_and_lock_tables (create info const)-> 
                        |                         open_tables (create info const)-> 
                        |                                       lock_table_names (create info const)- >
                        |                                                            upgrade_lock_if_not_exists (create info const)-> * S1: here we should mark flag and tbl_name in HA_CREATE_INFO after ha_table_exists
                        |                                                                                           ha_table_exists -> build_table_filename (flag: table existed or not?; tbl_name)
                        |
                        |2.-->mysql_create_table_no_lock() *S1 here we should skip if table exist  and use tbl_name path if created
                                                          ->build_table_filename() 
                        |                                                        |
                        |                                                        |
                                                                                 |3.-->create_table_impl() *S1 again check if table exists and skip if does
                                                                                                          -> ha_table_exists->build_table_filename
 
 Solutions:
 1. Solution 1: Since all paths 1.2.3. (see above) have  reference to const object `const &create_info`
   - Added `create table if not exists t1` - ha_table_exists called 3 times with patch (path 1. & 3 & 1.)
                                           - `build_table_filename` called ... the same number of times as without patch...
  - Debug: `mtr --mem --gdb='b upgrade_lock_if_not_exists; b mysql_create_table_no_lock; b ha_table_exists; r' anel.test`

  
 2. Solution 2: Remove const from all functions - not working HA_CREATE_INFO,DDL are parent classes of Table_specificatoin and only DDL is casted as an argument to nested functions
- add additional variable `create_tbl_path` as an function argument and propagate it to the `ha_table_exists` in path 1.

 3. Solution 3: Add HA_CREATE_INFO variable as an argument into `upgrade_lock_if_not_exists` function
    - check existance of a table in ha_table_exists directly
      - have errors in tests in case of `create or replace` and `create if not exists` - seems table_id aka org_tabledef_version has to be checked in create_table_impl() however:
      `FAILED TESTS`
      main.create_or_replace main.backup_log main.lock main.mdev19198 main.create
      - by adding handlerton(*)create_info->db_type from ha_table_exists got in check_engine NULL < conclusion create_table->db_type shouldn't be changed in ha_table_exists , but it is changed somewhere in open_and_lock_tables(),
        since `(TABLE_LIST)create_table->db_type= 0` at the beginning in `mysql_create_table` and handlerton is set at the beginning of `mysql_create_table`

- This is the case when `create_info->table_exists= false` < so table is just created that is new path: 4. that has `create_table_impl`


4. Handling Create table from SELECT
Sql_cmd_create_table_like::execute (handle_select) ->
                                      select_create::prepare
                                                             -> select_create::create_table_from_items
                                                                                                       -> mysql_create_table_no_lock
                                                                                                                                     -> create_table_impl
 
                                                                                                                                                        -> ha_create_table
                                                                                                                                                        
 
 5. New bug occuring in `create or replace table t1` with lock being held -> path 2. mysql_create_table_no_lock->create_table_impl->ha_create_table the same error `HA_ERR_TABLE_EXIST` that shouldn't be called.
    We have to check that `create_info->table_exists` is set in `ha_table_exists`. It didn't called path 1.
    Path of open_tables(doesn't go int lock_tables)
    
 Sql_cmd_create_table_like::execute(12500)
                                          ->mysql_create_table(4888)
                                                                     -> mysql_create_table_no_lock(4769)
                                                                                                         ->create_table_impl
                                                                                                                              -> ha_create_table
                                                                                                         

6. New bug with `create table replace like` again ddl is OPT_OR_REPLACE but ddl not visible in `create_table_impl()`

Sql_cmd_create_table_like::execute
                                   -> mysql_create_like_table 
                                                              -> mysql_create_table_no_lock
                                                                                             -> create_table_impl
                                     
```
(gdb) bt
+bt
#0  my_message_sql (error=156, str=0x7ffff20169b0 "MyISAM table 't2' is in use (most likely by a MERGE table). Try FLUSH TABLES.", MyFlags=0) at /home/anel/GitHub/mariadb/server/src/11.2/sql/mysqld.cc:3371
#1  0x0000555556883eb0 in my_printf_error (error=error@entry=156, format=format@entry=0x555556d355b0 "MyISAM table '%s' is in use (most likely by a MERGE table). Try FLUSH TABLES.", MyFlags=MyFlags@entry=0) at /home/anel/GitHub/mariadb/server/src/11.2/mysys/my_error.c:153
#2  0x00005555568352f9 in mi_create (name=0x7ffff2018630 "./test/t2", keys=keys@entry=0, keydefs=keydefs@entry=0x7fffe0016570, columns=columns@entry=2, recinfo=recinfo@entry=0x7fffe00164a8, uniques=uniques@entry=0, uniquedefs=0x0, ci=0x7ffff20185f0, flags=0) at /home/anel/GitHub/mariadb/server/src/11.2/storage/myisam/mi_create.c:643
#3  0x0000555556820a2b in ha_myisam::create (this=<optimized out>, name=0x7ffff2019e90 "./test/t2", table_arg=<optimized out>, ha_create_info=<optimized out>) at /home/anel/GitHub/mariadb/server/src/11.2/storage/myisam/ha_myisam.cc:2320
#4  0x00005555560b3511 in handler::ha_create (this=0x7fffe007a800, name=0x7ffff2019e90 "./test/t2", form=form@entry=0x7ffff2018990, info_arg=info_arg@entry=0x7ffff201b270) at /home/anel/GitHub/mariadb/server/src/11.2/sql/handler.cc:5664
#5  0x00005555560b4297 in ha_create_table (thd=thd@entry=0x7fffe0000d48, path=0x7ffff2019e90 "./test/t2", db=0x7fffe0017410 "test", table_name=0x7fffe0016cc8 "t2", create_info=create_info@entry=0x7ffff201b270, frm=frm@entry=0x7ffff2019e80, skip_frm_file=false) at /home/anel/GitHub/mariadb/server/src/11.2/sql/handler.cc:6133

```
```
(gdb) p *create_info->db_type
+p *create_info->db_type
$3 = {
  db_type = DB_TYPE_MYISAM,
  slot = 0,
  savepoint_offset = 0,
  close_connection = 0x0,
  kill_query = 0x0,
  savepoint_set = 0x0,
  savepoint_rollback = 0x0,
  savepoint_rollback_can_release_mdl = 0x0,
  savepoint_release = 0x0,
  commit = 0x0,
  commit_ordered = 0x0,
  rollback = 0x0,
  prepare = 0x0,
  prepare_ordered = 0x0,
  recover = 0x0,
  commit_by_xid = 0x0,
  rollback_by_xid = 0x0,
  commit_checkpoint_request = 0x0,
  checkpoint_state = 0x0,
  create_cursor_read_view = 0x0,
  set_cursor_read_view = 0x0,
  close_cursor_read_view = 0x0,
  create = 0x555556822117 <myisam_create_handler(handlerton*, TABLE_SHARE*, MEM_ROOT*)>,
  drop_database = 0x0,
  drop_table = 0x55555681eb36 <myisam_drop_table(handlerton*, char const*)>,
  panic = 0x55555681ef13 <myisam_panic(handlerton*, ha_panic_function)>,
  start_consistent_snapshot = 0x0,
  flush_logs = 0x0,
  show_status = 0x0,
  partition_flags = 0x0,
  alter_table_flags = 0x0,
  fill_is_table = 0x0,
  flags = 132,
  binlog_func = 0x0,
  binlog_log_query = 0x0,
  abort_transaction = 0x0,
  set_checkpoint = 0x0,
  get_checkpoint = 0x0,
  check_version = 0x0,
  signal_ddl_recovery_done = 0x0,
  update_optimizer_costs = 0x55555681ddb8 <myisam_update_optimizer_costs(OPTIMIZER_COSTS*)>,
  optimizer_costs = 0x555557f83128,
  table_options = 0x0,
  field_options = 0x0,
  index_options = 0x0,
  tablefile_extensions = 0x55555742af70 <ha_myisam_exts>,
  create_group_by = 0x0,
  create_derived = 0x0,
  create_select = 0x0,
  create_unit = 0x0,
  discover_table = 0x0,
  discover_table_names = 0x0,
  discover_table_existence = 0x0,
  discover_table_structure = 0x0,
  notify_tabledef_changed = 0x0,
  prepare_commit_versioned = 0x0,
  disable_internal_writes = 0x0,
  prepare_for_backup = 0x0,
  end_backup = 0x0,
  pre_shutdown = 0x0,
  create_partitioning_metadata = 0x0
}

```
 - It is set to `0` in `execute` (for new SQL CREATE query) and set in `use_default_db_type` method

```
 Old value = (handlerton *) 0x555557f81db8
New value = (handlerton *) 0x0
0x0000555555e64a85 in Sql_cmd_create_table_like::execute

Old value = (handlerton *) 0x0
New value = (handlerton *) 0x555557f81db8
0x0000555555e64cd6 in Table_scope_and_contents_source_pod_st::use_default_db_type (thd=0x7fffe0000d48, this=0x7ffff201b270) at /home/anel/GitHub/mariadb/server/src/11.2/sql/handler.h:2255
(gdb) bt
+bt
#0  0x0000555555e64cd6 in Table_scope_and_contents_source_pod_st::use_default_db_type (thd=0x7fffe0000d48, this=0x7ffff201b270) at /home/anel/GitHub/mariadb/server/src/11.2/sql/handler.h:2255
#1  Sql_cmd_create_table_like::execute (this=<optimized out>, thd=0x7fffe0000d48) at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_table.cc:12270
```
 
 ha_table_exists 
   open_table-> ha_table_exists
   mysql_create_table->open_tables-> lock_table_names(4594)-> upgrade_lock_if_not_exists->ha_table_exists->build_table_filename #create_table_before_check_if_exists (DBUG_SYNC)
   create_table_impl-> ha_table_exists()         (sql_table.cc)
   mysql_alter_table->ha_table_exists()          (--||--)
   
   
   create_table_impl->
## Test for case 1

Indeed for create table only 2 times ha_exists_table is invoked (in path 1.
```sql
--source include/have_debug.inc
--source include/have_debug_sync.inc
select @@debug_dbug;
set @old_debug= @@debug_dbug;
select @old_debug;
set debug_dbug= "d:t:i:o,/tmp/anel.trace";
select @@debug_dbug;
#set debug_sync='create_table_before_check_if_exists SIGNAL parked WAIT_FOR go';
Create table t(t int);
drop table t;
```
- Dbug_sync
```
T@6    : | | | | | >mysql_create_table
T@6    : | | | | | | >open_and_lock_tables
T@6    : | | | | | | | enter: derived handling: 0
T@6    : | | | | | | | >open_tables
T@6    : | | | | | | | | THD::enter_stage: Opening tables at /home/anel/GitHub/mariadb/server/src/11.2/sql/sql_base.cc:4556
T@6    : | | | | | | | | >lock_table_names
T@6    : | | | | | | | | | >upgrade_lock_if_not_exists
T@6    : | | | | | | | | | | >debug_sync
T@6    : | | | | | | | | | | | debug_sync_point: hit: 'create_table_before_check_if_exists'
T@6    : | | | | | | | | | | <debug_sync
T@6    : | | | | | | | | | | >ha_table_exists
T@6    : | | | | | | | | | | | >tdc_lock_share
T@6    : | | | | | | | | | | | <tdc_lock_share
T@6    : | | | | | | | | | | | >build_table_filename
T@6    : | | | | | | | | | | | | enter: db: 'test'  table_name: 't'  ext: ''  flags: 0
T@6    : | | | | | | | | | | | | >tablename_to_filename
T@6    : | | | | | | | | | | | | | enter: from 'test'
T@6    : | | | | | | | | | | | | | >check_if_legal_tablename
T@6    : | | | | | | | | | | | | | <check_if_legal_tablename
T@6    : | | | | | | | | | | | | | exit: to 'test'
T@6    : | | | | | | | | | | | | <tablename_to_filename
T@6    : | | | | | | | | | | | | >tablename_to_filename
T@6    : | | | | | | | | | | | | | enter: from 't'
T@6    : | | | | | | | | | | | | | >check_if_legal_tablename
T@6    : | | | | | | | | | | | | | <check_if_legal_tablename
T@6    : | | | | | | | | | | | | | exit: to 't'
T@6    : | | | | | | | | | | | | <tablename_to_filename
T@6    : | | | | | | | | | | | | exit: buff: './test/t'
T@6    : | | | | | | | | | | | <build_table_filename
```

##  Optimize build_table_filename
- Make single call of build_table_filename in lock_tables_names() and store it ha_create_info
- Remove call of `build_table_filename` from ha_table_exists and use ha_create_info created instead
- New commit - remove call between `mysql_create_table_no_lock` and  `create_table_impl` (sql_table.cc)
- Try to use   lex_string_set3(&cpath, path, path_length); to set the value

1.  mysql_create_table  (Table_specification_st *)-> 
                        |1.--> open_and_lock_tables (create info const)-> 
                        |                         open_tables (create info const)-> 
                        |                                       lock_table_names (create info const)- >
                        |                                                            upgrade_lock_if_not_exists (create info const)-> * S1: here we should mark flag and tbl_name in HA_CREATE_INFO after ha_table_exists
                        |                                                                                           ha_table_exists -> (removed) build_table_filename (flag: table existed or not?; tbl_name)
                        |
                        |2.-->mysql_create_table_no_lock() *S1 here we should skip if table exist  and use tbl_name path if created
                                                          ->build_table_filename() 
                        |                                                        |
                        |                                                        |
                                                                                 |3.-->create_table_impl() *S1 again check if table exists and skip if does
                                                                                                          -> ha_table_exists->build_table_filename
                                                                                                          
```
   build_table_filename(path, sizeof(path) - 1,
                                         db->str, table_name->str, "", 0);
```


# Tricks
```
LEX_CSTRING *table_path= thd->make_clex_string("\0", FN_REFLEN);
```
