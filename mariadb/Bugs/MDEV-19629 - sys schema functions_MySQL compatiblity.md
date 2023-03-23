# MDEV-19629 - add format_bytes(), format_pico_time() and ps_thread_id()

https://jira.mariadb.org/browse/MDEV-19629

https://mysql.wisborg.dk/2019/05/28/performance-schema-functions/

native function instead of sql funciton


## Performance schema in MariaDB
List of tables https://mariadb.com/kb/en/list-of-performance-schema-tables/
We need:
- `PS_CURRENT_THREAD_ID()`: should return `threads.THREAD_ID` column from https://mariadb.com/kb/en/performance-schema-threads-table/
- `ps_thread_id(conID)`: argument `threads.PROCESSLIST_ID` or ( `ID` of `show processlist`, or `id` column from  `show processlist` https://mariadb.com/kb/en/show-processlist/ (or from `IS.processlist` https://mariadb.com/kb/en/information-schema-processlist-table/ , or `processlist` command of https://mariadb.com/kb/en/mysqladmin/)). If reutnr is `null`, thread is not instrumented, or conID is null
  - It relates to `https://dev.mysql.com/doc/refman/8.0/en/performance-schema-system-variables.html#sysvar_performance_schema_max_thread_instances` (`performance_schema_max_thread_instances`)  https://mariadb.com/kb/en/performance-schema-system-variables/#performance_schema_max_thread_instances  
    - if `performance_schema_max_thread_instances == 0` (disabled instrumentation) `ps_thread_id` is NULL
    - if not zero, there is thread_id allocated and there is not enough memory to be allocated `Performance_schema_thread_instances_lost` https://mariadb.com/kb/en/performance-schema-status-variables/#performance_schema_thread_instances_lost
    - error if perf is disabled

## format_bytes() 
- MySQL: https://dev.mysql.com/doc/refman/8.0/en/sys-format-bytes.html added in 8.0.16 FORMAT_BYTES(), format_bytes() deprecated
FORMAT_BYTES should be used: https://dev.mysql.com/doc/refman/8.0/en/performance-schema-functions.html#function_format-bytes
Difference `FORMAT_BYTES() uses the EiB units indicator. sys.format_bytes() does not.`

- MariaDB has sysschema function that should be also deprecated and create native built-in function
https://mariadb.com/kb/en/format_bytes/

./scripts/sys_schema/functions/format_bytes.sql added with aa2ff62082c4 (from 10.6.0) cmake
` MDEV-9077 Use sys schema in bootstrapping, incl. mtr`
but the function script is added with 4bac804c90c6 (same MDEV)
and we can compare it with MySQL https://github.com/mysql/mysql-server/blob/8.0/scripts/sys_schema/functions/format_bytes.sql
Note the path in `mysql-server/scripts/sys_schema/functions/format_bytes.sql`
Differences:
- `DROP FUNCTION IF EXISTS format_bytes;` in mysql it is `sys.format_bytes`
- `DEFINER='mariadb.sys'@'localhost'` in mysql it is `mysql.sys`
- Also note that this function is calling in `else` that we need to change
`RETURN format_bytes(bytes);`


## format_pico_time() 
- MySQL https://dev.mysql.com/doc/refman/8.0/en/performance-schema-functions.html#function_format-pico-time
FORMAT_PICO_TIME

##  ps_thread_id()
- MySQL https://dev.mysql.com/doc/refman/8.0/en/sys-ps-thread-id.html same PS_THREAD_ID() and PS_CURRENT_THREAD_ID()
see https://dev.mysql.com/doc/refman/8.0/en/performance-schema-functions.html#function_ps-thread-id

MySQL implementation:
https://github.com/mysql/mysql-server/blob/8.0/scripts/sys_schema/functions/ps_thread_id.sql
```
  IF (in_connection_id IS NULL) THEN
    RETURN ps_current_thread_id();
  ELSE
    RETURN ps_thread_id(in_connection_id);
  END IF;
```

Source code definition:
`/** format_pico_time() */`
`/** format_bytes() */`
`/** ps_thread_id() */`
`/** ps_current_thread_id() */`
https://github.com/mysql/mysql-server/blob/8.0/sql/item_pfs_func.h


Source code declaration:
https://github.com/mysql/mysql-server/blob/8.0/sql/item_create.cc#L1416
https://github.com/mysql/mysql-server/blob/8.0/sql/item_pfs_func.cc

Test cases are in `suite/perfschema/t/` 
- https://github.com/mysql/mysql-server/blob/8.0/mysql-test/suite/perfschema/t/native_func_format_time.test
- https://github.com/mysql/mysql-server/blob/8.0/mysql-test/suite/perfschema/t/native_func_format_bytes.test
- https://github.com/mysql/mysql-server/blob/8.0/mysql-test/suite/perfschema/t/native_func_thread_id.test
- https://github.com/mysql/mysql-server/blob/8.0/mysql-test/suite/perfschema/t/native_func_thread_id_no_ps.test
- https://github.com/mysql/mysql-server/blob/8.0/mysql-test/suite/perfschema/t/native_func_thread_id_null.test
- added with commit
```
commit 260e09ea654a9688f588c13f5303bcc34dfc4a7d
Author: Christopher Powers <chris.powers@oracle.com>
Date:   Thu Dec 13 01:33:24 2018 +0100

    WL#7803 Performance Schema, Native Functions
    
    Added native functions:
    
      ps_current_thread_id()
      ps_thread_id()
      format_bytes()
      format_pico_time()

```

