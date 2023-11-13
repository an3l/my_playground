# MDEV-28367: BACKUP LOCKS on table to be accessible to those with database LOCK TABLES privileges

https://jira.mariadb.org/browse/MDEV-28367

[Backup lock](https://mariadb.com/kb/en/backup-lock/)
- Blocks a table from DDL statements (create, modify, remove tables/indexxes)
- Implemented by taking an `MDLSHARED_HIGH_PRIO` MDL lock
  on the table object, which protects the table from any DDL operations.
- Used by mariabackup
  - When table files (.frm, .MAI, MAD) are opened,
    ensure there are no DDLs.
    
- Usage
```SQL
BACKUP LOCK [database.]table_name;
 - Open all files related to a table (for example, t.frm, t.MAI and t.MYD)
BACKUP UNLOCK;
- Copy data
- Close files
```

- Requires [RELOAD](https://mariadb.com/kb/en/grant/#reload) privilege
  ```
  Execute FLUSH statements or equivalent mariadb-admin commands.
  ```
  - Stopping `mysqld` via `mariadb-admin` - need a user with `SUPER` or `SHUTDOWN` privilege
  - [FLUSH](https://mariadb.com/kb/en/flush/) statements clears/reloads internal caches
    - Cleanup open table cache and table definition cache from not in use tables.
      - This free file descriptors and memory.
    - Take backup on same tables
  
# Implementation
```
	    if (unlikely(!Select->add_table_to_list(thd, 
	                                            $3 (table),
	                                            NULL (alias),
	                                            0 (table_options),
                                                   TL_READ (lock_type),
                                                   MDL_SHARED_HIGH_PRIO (mdl_type))))
             MYSQL_YYABORT;
            Lex->sql_command= SQLCOM_BACKUP_LOCK;
            Lex->pop_select(); //main select
          }
```
- Calls `add_table_to_list` table to a list of used tables,
  with `TL_READ` and `MDL_SHARED_HIGH_PRIO`
  - `add_table_to_list`
    -  `MDL_SHARED_HIGH_PRIO` - type of metadata to acquire on the table, called with `mdl_request.init()`
    ```
	  /*
	    A high priority shared metadata lock.
	    Used for cases when there is no intention to access object data (i.e.
	    data in the table).
	    "High priority" means that, unlike other shared locks, it is granted
	    ignoring pending requests for exclusive locks. Intended for use in
	    cases when we only need to access metadata and not data, e.g. when
	    filling an INFORMATION_SCHEMA table.
	    Since SH lock is compatible with SNRW lock, the connection that
	    holds SH lock lock should not try to acquire any kind of table-level
	    or row-level lock, as this can lead to a deadlock. Moreover, after
	    acquiring SH lock, the connection should not wait for any other
	    resource, as it might cause starvation for X locks and a potential
	    deadlock during upgrade of SNW or SNRW to X lock (e.g. if the
	    upgrading connection holds the resource that is being waited for).
	  */
    ```
    
 - Locks:
   1) Scoped locks - DBs, schema locks
   2) Object locks - tables, triggers
  
 - Function `can_grant_lock()` `SQLCOM_BACKUP_LOCK`
 
 - We need to add beside `RELOAD_ACL` also `LOCK_TABLES_ACL` to function `check_global_access()`
 - There is `PRIV_LOCK_TABLES (SELECT_ACL | LOCK_TABLES_ACL)`
 - LOCK TABLE is calling `lock_tables_precheck` with `check_table_access(thd, PRIV_LOCK_TABLES, table, FALSE, 1, FALSE)`
 - `PRIV_LOCK_TABLES` is related to the `DB_ACLS`, `GLOBAL_ACLS`, 
 - `RELOAD_ACL` is `GLOBAL_ACLS`, not `DB_ACLS`, so in order to have `DB_ACLS` we should use either `SELECT_ACL` or `LOCK_TABLES_ACL`, so if one has `LOCK_TABLES_ACL`
 
 - `People with only a database privilege won't have the global RELOAD privilege currently required to use backup locks.`
 - Use lower level privilege.
 
