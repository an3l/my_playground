
# MDEV - 24598 duplicate check constraint name


## About table/field constraints in source code

| Create_field::check_constraint    | TABLE_SHARE::check_constraints | TABLE_SHARE::table_check_constraints |
| --------------------------------- | ------------------------------ | ------------------------------------ |

- Problem for JSON type

```
CREATE TABLE t (
path VARCHAR(100) NOT NULL COLLATE 'utf8_general_ci',
json_c1 JSON NOT NULL DEFAULT '' COLLATE 'utf8mb4_bin',
json_c2 JSON NOT NULL DEFAULT '' COLLATE 'utf8mb4_bin',
comment VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
UNIQUE INDEX path (path),
CONSTRAINT json_c1 CHECK (path > 0)
);

```

- Backtrace for each filed
```
+bt
#0  check_expression (vcol=0x555556029671 <add_virtual_expression(THD*, Item*)+58>, name=0x7ffff15ee5b0, type=32767) at /home/anel/GitHub/mariadb/server/src/10.4/sql/field.cc:10660
#1  0x00005555560d92a7 in Column_definition::validate_check_constraint (this=0x7fffe0016458, thd=0x7fffe0000d28) at /home/anel/GitHub/mariadb/server/src/10.4/sql/field.cc:10790
#2  0x0000555555fdb905 in Type_handler::Column_definition_validate_check_constraint (this=0x55555740eed0 <type_handler_json_longtext>, thd=0x7fffe0000d28, c=0x7fffe0016458) at /home/anel/GitHub/mariadb/server/src/10.4/sql/sql_type.cc:2451
#3  0x00005555563284c8 in Type_handler_json_longtext::Column_definition_validate_check_constraint (this=0x55555740eed0 <type_handler_json_longtext>, thd=0x7fffe0000d28, c=0x7fffe0016458) at /home/anel/GitHub/mariadb/server/src/10.4/sql/sql_type_json.cc:54
#4  0x00005555560d9424 in Column_definition::check (this=0x7fffe0016458, thd=0x7fffe0000d28) at /home/anel/GitHub/mariadb/server/src/10.4/sql/field.cc:10808
#5  0x0000555556036808 in MYSQLparse (thd=0x7fffe0000d28) at /home/anel/GitHub/mariadb/server/src/10.4/sql/sql_yacc.yy:6784
#6  0x0000555555db915d in parse_sql (thd=0x7fffe0000d28, parser_state=0x7ffff15f03e0, creation_ctx=0x0, do_pfs_digest=true) at /home/anel/GitHub/mariadb/server/src/10.4/sql/sql_parse.cc:10362
#7  0x0000555555db38b5 in mysql_parse (thd=0x7fffe0000d28, rawbuf=0x7fffe00158c0 "CREATE TABLE t (\npath VARCHAR(100) NOT NULL COLLATE 'utf8_general_ci',\njson_c1 JSON NOT NULL DEFAULT '' COLLATE 'utf8mb4_bin',\njson_c2 JSON NOT NULL DEFAULT '' COLLATE 'utf8mb4_bin',\ncomment VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8_general_ci',\nUNIQUE INDEX path (path),\nCONSTRAINT json_c1 CHECK (path > 0)\n)", length=312, parser_state=0x7ffff15f03e0, is_com_multi=false, is_next_command=false) at /home/anel/GitHub/mariadb/server/src/10.4/sql/sql_parse.cc:7964
```


Note: `/home/anel/GitHub/mariadb/server/src/10.4/sql/sql_type_json.cc:54` 
```
Column_definition_validate_check_constraint::
 !(c->check_constraint= make_json_valid_expr(thd, &c->field_name)))
```

Second call of `check_expression`- because of `default keyword`in 
```
+bt
#0  check_expression (vcol=0x7fffe0016898, name=0x7fffe0016890, type=21845) at /home/anel/GitHub/mariadb/server/src/10.4/sql/field.cc:10660
#1  0x00005555560d9483 in Column_definition::check (this=0x7fffe0016898, thd=0x7fffe0000d28) at /home/anel/GitHub/mariadb/server/src/10.4/sql/field.cc:10814
#2  0x0000555556036808 in MYSQLparse (thd=0x7fffe0000d28) at /home/anel/GitHub/mariadb/server/src/10.4/sql/sql_yacc.yy:6784

```

```

Failing test(s): main.mysqldump main.create_select main.information_schema main.plugin_auth main.alter_table main.column_compression main.mysql_upgrade main.ctype_binary main.ctype_utf16_uca main.ctype_utf32 main.ctype_utf32_uca main.insert_select main.system_mysql_db main.type_json main.subselect main.check_constraint main.check_constraint_show main.constraints main.system_mysql_db_fix40123 main.system_mysql_db_fix50568 main.system_mysql_db_fix50117 main.system_mysql_db_fix50030

```
 main.mysqldump
```
Failing test(s): main.information_schema main.plugin_auth main.alter_table main.column_compression main.ctype_binary main.ctype_utf16_uca main.ctype_utf32 main.ctype_utf32_uca main.insert_select main.system_mysql_db main.type_json main.subselect main.check_constraint main.check_constraint_show main.constraints main.system_mysql_db_fix40123 main.system_mysql_db_fix50568 main.system_mysql_db_fix50117 main.system_mysql_db_fix50030

```


main.check_constraint - bug in check (default(expression))
Caused by:b5e16a6e0381b28b598da80b414168ce9a5016e5



- Latest
```
main.backup_lock 'innodb'                w1 [ fail ]  timeout after 900 seconds
        Test ended at 2023-09-28 15:27:26

Test case timeout after 900 seconds

== /home/anel/GitHub/mariadb/server/build/10.4/mysql-test/var/1/log/backup_lock.log == 
1	NULL
2	0
drop table t1;
# Test with inline alter table, which doesn't block block_commit
create table t1 (a int) engine=innodb;
start transaction;
insert into t1 values (1);
connection con1;
alter table t1 add column (j int);
connection con2;
backup stage start;
backup stage flush;
SELECT LOCK_MODE, LOCK_TYPE, TABLE_SCHEMA, TABLE_NAME FROM information_schema.metadata_lock_info;
LOCK_MODE	LOCK_TYPE	TABLE_SCHEMA	TABLE_NAME
MDL_BACKUP_DDL	Backup lock		
MDL_BACKUP_FLUSH	Backup lock		
MDL_SHARED_WRITE	Table metadata lock	test	t1
MDL_SHARED_UPGRADABLE	Table metadata lock	test	t1
MDL_INTENTION_EXCLUSIVE	Schema metadata lock	test	
backup stage block_ddl;

 == /home/anel/GitHub/mariadb/server/build/10.4/mysql-test/var/1/tmp/analyze-timeout-mysqld.1.err ==
mysqltest: Could not open connection 'default' after 500 attempts: 2002 Can't connect to local MySQL server through socket '/home/anel/GitHub/mariadb/server/build/10.4/mysql-test/var/tmp/1' (111)


 - saving '/home/anel/GitHub/mariadb/server/build/10.4/mysql-test/var/1/log/main.backup_lock-innodb/' to '/home/anel/GitHub/mariadb/server/build/10.4/mysql-test/var/log/main.backup_lock-innodb/'
***Warnings generated in error logs during shutdown after running tests: main.backup_lock main.backup_interaction

Attempting backtrace. You can use the following information to find out

--------------------------------------------------------------------------
The servers were restarted 224 times
Spent 1423.935 of 1007 seconds executing testcases

Completed: Failed 9/1064 tests, 99.15% were successful.

Failing test(s): main.create_select main.alter_table main.default main.ctype_binary main.check_constraint main.check_constraint_show main.type_json main.constraints main.backup_lock

The log files in var/log may give you some hint of what went wrong.

If you want to report this error, please read first the documentation
at http://dev.mysql.com/doc/mysql/en/mysql-test-suite.html

Errors/warnings were found in logfiles during server shutdown after running the
following sequence(s) of tests:
    main.backup_lock main.backup_interaction
53 tests were skipped, 32 by the test itself.

```

Subquery in check constraint is failing, MDEV-12421 - https://github.com/MariaDB/server/commit/22d8bb27066fa841548d57b6d110162093be535a 
```sql
create table t1 (a int check (@b in (select user from mysql.user)));
```

```
sql/sql_base.cc:6204(find_field_in_table_ref(THD*, TABLE_LIST*, char const*, unsigned long, char const*, char const*, char const*, Item**, bool, bool, unsigned int*, bool, TABLE_LIST**))[0x556a34728852]
sql/sql_base.cc:6507(find_field_in_tables(THD*, Item_ident*, TABLE_LIST*, TABLE_LIST*, Item**, find_item_error_report_type, bool, bool))[0x556a34729580]
sql/item.cc:5904(Item_field::fix_fields(THD*, Item**))[0x556a34b49326]
sql/item.h:966(Item::fix_fields_if_needed(THD*, Item**))[0x556a346a8613]
sql/item.h:970(Item::fix_fields_if_needed_for_scalar(THD*, Item**))[0x556a346a864d]
sql/sql_base.cc:7744(setup_fields(THD*, Bounds_checked_array<Item*>, List<Item>&, enum_column_usage, List<Item>*, List<Item>*, bool))[0x556a3472c7e2]
sql/sql_select.cc:1330(JOIN::prepare(TABLE_LIST*, unsigned int, Item*, unsigned int, st_order*, bool, st_order*, Item*, st_order*, st_select_lex*, st_select_lex_unit*))[0x556a34812c81]
sql/item_subselect.cc:3804(subselect_single_select_engine::prepare(THD*))[0x556a34c106ab]
sql/item_subselect.cc:289(Item_subselect::fix_fields(THD*, Item**))[0x556a34c02999]
sql/item_subselect.cc:3466(Item_in_subselect::fix_fields(THD*, Item**))[0x556a34c0f576]
sql/table.cc:3288(Virtual_column_info::fix_expr(THD*))[0x556a34902fb0]
sql/table.cc:3458(Virtual_column_info::fix_and_check_expr(THD*, TABLE*))[0x556a34903967]
sql/table.cc:3590(unpack_vcol_info_from_frm(THD*, TABLE*, String*, Virtual_column_info**, bool*))[0x556a34903f3a]
sql/table.cc:1209(parse_vcol_defs(THD*, st_mem_root*, TABLE*, bool*, vcol_init_mode))[0x556a348fb47c]
sql/table.cc:3996(open_table_from_share(THD*, TABLE_SHARE*, st_mysql_const_lex_string const*, unsigned int, unsigned int, unsigned int, TABLE*, bool, List<String>*))[0x556a34905671]
sql/handler.cc:5313(ha_create_table(THD*, char const*, char const*, char const*, HA_CREATE_INFO*, st_mysql_const_unsigned_lex_string*))[0x556a34b2748c]
sql/sql_table.cc:5182(create_table_impl(THD*, st_mysql_const_lex_string const&, st_mysql_const_lex_string const&, st_mysql_const_lex_string const&, st_mysql_const_lex_string const&, char const*, DDL_options_st, HA_CREATE_INFO*, Alter_info*, int, bool*, st_key**, unsigned int*, st_mysql_const_unsigned_lex_string*))[0x556a348b8205]
sql/sql_table.cc:5266(mysql_create_table_no_lock(THD*, st_mysql_const_lex_string const*, st_mysql_const_lex_string const*, Table_specification_st*, Alter_info*, bool*, int, TABLE_LIST*))[0x556a348b8645]
sql/sql_table.cc:5415(mysql_create_table(THD*, TABLE_LIST*, Table_specification_st*, Alter_info*))[0x556a348b8bc9]
sql/sql_table.cc:11817(Sql_cmd_create_table_like::execute(THD*))[0x556a348cc2ae]

```

3 tEsts:
```
 main.alter_table main.check_constraint main.backup_lock
```
 
 
 
 AFter bb
 ```
 innodb.instant_alter innodb.instant_alter_limit innodb.instant_alter_debug sql_sequence.create innodb.instant_alter_rollback gcol.gcol_column_def_options_innodb compat/oracle.column_compression sql_sequence.other main.check_constraint
 ```

- Checking `mysqldump.test`
  - 1. Revert showing check constraint
  ```bash
--- a/sql/sql_show.cc
+++ b/sql/sql_show.cc
@@ -2348,16 +2348,6 @@ int show_create_table(THD *thd, TABLE_LIST *table_list, String *packet,
 
     append_create_options(thd, packet, field->option_list, check_options,
                           hton->field_options);
-    
-    if (field->check_constraint)
-    {
-      StringBuffer<MAX_FIELD_WIDTH> str(&my_charset_utf8mb4_general_ci);
-      field->check_constraint->print(&str);
-      packet->append(STRING_WITH_LEN(" CHECK ("));
-      packet->append(str);
-      packet->append(STRING_WITH_LEN(")"));
-    }
-
   }

  ```
  - 2. revert adding flag to the field https://github.com/MariaDB/server/pull/2773/files#diff-e324c0cc8407bcbde70d4386ddf26c78ca6443b2fafb254d49da77ec3e0ff3beR6781
Tests affected
```
$ ./mysql-test/mtr alter_table anel check_constraint_show column_compression constraints create_select ctype_binary ctype_utf16_uca ctype_utf32 ctype_utf32_uca default information_schema system_mysql_db system_mysql_db_fix40123 system_mysql_db_fix50030 system_mysql_db_fix50117 system_mysql_db_fix50568 type_json --mem --parallel=auto --force --record
Logging: /home/anel/GitHub/mariadb/server/src/10.4/mysql-test/mysql-test-run.pl  alter_table anel check_constraint_show column_compression constraints create_select ctype_binary ctype_utf16_uca ctype_utf32 ctype_utf32_uca default information_schema system_mysql_db system_mysql_db_fix40123 system_mysql_db_fix50030 system_mysql_db_fix50117 system_mysql_db_fix50568 type_json is_check_constraints is_table_constraints other --mem --parallel=auto --force --record

```
- With reverted
```bash
Failing test(s): main.subselect_no_exists_to_in

```

I got this error not related tot he 
```
ain.subselect_no_exists_to_in           w1 [ fail ]
        Test ended at 2023-10-16 13:27:39

CURRENT_TEST: main.subselect_no_exists_to_in
/home/anel/GitHub/mariadb/server/build/10.4/client//mysqltest: Error on delete of '/home/anel/GitHub/mariadb/server/build/10.4/mysql-test/var/1/tmp/subselect.out.file.1' (Errcode: 2 "No such file or directory")
mysqltest: In included file "/home/anel/GitHub/mariadb/server/src/10.4/mysql-test/main/subselect.test": 
included from /home/anel/GitHub/mariadb/server/src/10.4/mysql-test/main/subselect_no_exists_to_in.test at line 8:
At line 5993: query 'Select 
(Select Sum(`TestCase`.Revenue) From mysql.slow_log E           
Where TestCase.TemplateID not in (Select 1 from mysql.slow_log where 2=2)
) As `ControlRev`
From 
(Select  3 as Revenue, 4 as TemplateID) As `TestCase` 
Group By  TestCase.Revenue, TestCase.TemplateID' failed: 1242: Subquery returns more than 1 row

The result from queries just before the failure was:
< snip >
2	SUBQUERY	t2	ref	b	b	5	test.t1.a	2	Using index
DROP TABLE t1,t2;
#
# MDEV-5991: crash in Item_field::used_tables
#
create table t1 (c int);
select exists(select 1 from t1 group by `c` in (select `c` from t1));
exists(select 1 from t1 group by `c` in (select `c` from t1))
0
drop table t1;
#
# MDEV-7565: Server crash with Signal 6 (part 2)
#
Select 
(Select Sum(`TestCase`.Revenue) From mysql.slow_log E           
Where TestCase.TemplateID not in (Select 1 from mysql.slow_log where 2=2)
) As `ControlRev`
From 
(Select  3 as Revenue, 4 as TemplateID) As `TestCase` 
Group By  TestCase.Revenue, TestCase.TemplateID;

More results from queries before failure can be found in /home/anel/GitHub/mariadb/server/build/10.4/mysql-test/var/1/log/subselect_no_exists_to_in.log

 - saving '/home/anel/GitHub/mariadb/server/build/10.4/mysql-test/var/1/log/main.subselect_no_exists_to_in/' to '/home/anel/GitHub/mariadb/server/build/10.4/mysql-test/var/log/main.subselect_no_exists_to_in/'
***Warnings generated in error logs during shutdown after running tests: main.subselect_mat_cost_bugs main.myisam-system main.subselect_mat main.subselect_exists2in main.subselect_extra main.subselect_gis main.merge main.metadata main.mrr_icp_extra main.merge_debug main.multi_update_debug main.subselect_extra_no_semijoin main.mdev_22370 main.mix2_myisam main.subselect_exists2in_costmat main.subselect_debug main.myisam_debug main.myisam-optimize main.subselect_no_exists_to_in main.mix2_myisam_ucs2

2023-10-16 13:27:37 102 [Warning] Sort aborted, host: localhost, user: root, thread: 102, query: select numeropost as a FROM t1 ORDER BY (SELECT 1 FROM t1 HAVING a=1)
2023-10-16 13:27:37 102 [Warning] Sort aborted, host: localhost, user: root, thread: 102, query: SELECT a FROM t1 GROUP BY a
2023-10-16 13:27:37 102 [Warning] Sort aborted, host: localhost, user: root, thread: 102, query: SELECT a FROM t1 GROUP BY a
2023-10-16 13:27:37 102 [Warning] Sort aborted, host: localhost, user: root, thread: 102, query: SELECT a FROM t1
2023-10-16 13:27:37 102 [Warning] Sort aborted, host: localhost, user: root, thread: 102, query: SELECT a FROM t1
```







