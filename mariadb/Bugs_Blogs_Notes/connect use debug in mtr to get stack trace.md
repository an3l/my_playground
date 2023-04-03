



### Type descriptor block (TDB) of external table TDBEXT call (see first below ODBCDEF)
Query: 
set @old_debug= @@debug_dbug;
SET debug_dbug="d:i:o,/tmp/maria.debug:t";
select @@debug_dbug;
@@debug_dbug
d:i:o,/tmp/maria.debug:t
CREATE TABLE pg_in_maria ENGINE=CONNECT TABNAME='schema1.space_in_column_name' CHARSET=utf8 DATA_CHARSET=utf8 TABLE_TYPE=ODBC CONNECTION='DSN=ConnectEnginePostgresql;UID=mtr;PWD=mtr' QUOTED=3 QCHAR='`';
SELECT * from pg_in_maria; # This one is executed

(gdb) bt
+bt
#0  TDBEXT::TDBEXT (this=0x5555561e3f85 <BLOCK::operator new(unsigned long, _global*, void*)+90>, tdp=0x7ffff15a31e0) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/tabext.cpp:184
#1  0x0000555556271d3f in TDBODBC::TDBODBC (this=0x7fffd7fff380, tdp=0x7fffd7fff090) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/tabodbc.cpp:171
#2  0x0000555556271b5e in ODBCDEF::GetTable (this=0x7fffd7fff090, g=0x7fffe0025b40, m=MODE_READ) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/tabodbc.cpp:155

<>
#3  0x00005555561e8c27 in MYCAT::GetTable (this=0x7fffe0006f30, g=0x7fffe0025b40, tablep=0x7fffd7fff048, mode=MODE_READ, type=0x0) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/mycat.cc:561

<Initialize TDB>
#4  0x00005555561e5000 in CntGetTDB (g=0x7fffe0025b40, name=0x7fffe006747f "pg_in_maria", mode=MODE_READ, h=0x7fffe0076600) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/connect.cc:217

<>
#5  0x00005555561d1f0a in ha_connect::GetTDB (this=0x7fffe0076600, g=0x7fffe0025b40) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/ha_connect.cc:1997

See <my_base.h> used by optimizer - doesn't implement most of fields really needed, sets tdbp
#6  0x00005555561d9de4 in ha_connect::info (this=0x7fffe0076600, flag=18) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/ha_connect.cc:4406

#7  0x0000555555db8417 in TABLE_LIST::fetch_number_of_rows (this=0x7fffe0013fa8) at /home/anel/GitHub/mariadb/server/src/10.3/sql/table.cc:8749


### ODBCDEF is invoked from < MYCAT::MakeTableDesc>

gdb) bt
+bt
#0  ODBCDEF::ODBCDEF (this=0x110) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/tabodbc.cpp:97
#1  0x00005555561e8525 in MYCAT::MakeTableDesc (this=0x7fffe0006f30, g=0x7fffe0025b40, tablep=0x7fffd7fff048, am=0x7fffe00789d0 "ODBC") at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/mycat.cc:479
#2  0x00005555561e82b3 in MYCAT::GetTableDesc (this=0x7fffe0006f30, g=0x7fffe0025b40, tablep=0x7fffd7fff048, type=0x0) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/mycat.cc:431
#3  0x00005555561e8b55 in MYCAT::GetTable (this=0x7fffe0006f30, g=0x7fffe0025b40, tablep=0x7fffd7fff048, mode=MODE_READ, type=0x0) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/mycat.cc:549
#4  0x00005555561e5000 in CntGetTDB (g=0x7fffe0025b40, name=0x7fffe006747f "pg_in_maria", mode=MODE_READ, h=0x7fffe0076600) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/connect.cc:217


After which is called <TABDEF::Define> which defines table definition block from XDB file from which is called  <ODBCDEF::DefineAM > where 

(gdb) bt
+bt
#0  TABDEF::Define (this=0x55555627183a <ODBCDEF::ODBCDEF()+28>, g=0x7ffff15a3170, cat=0x7fffd7fff090, name=0x7ffff15a3170 "\320\061Z\361\377\177", schema=0x555556210100 <EXTDEF::EXTDEF()+28> "H\215\025\271\026\006\001H\213E\370H\211\020H\213E\370Hǀ\250", am=0x7ffff15a3150 "p1Z\361\377\177") at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/reldef.cpp:356
#1  0x00005555561e87b5 in MYCAT::MakeTableDesc (this=0x7fffe0006f30, g=0x7fffe0025b40, tablep=0x7fffd7fff048, am=0x7fffe00789d0 "ODBC") at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/mycat.cc:527

!!!! <<< The function  <ODBCDEF::DefineAM > calls <EXTDEF::DefineAM>   >>>>!!!!
EXTDEF::DefineAM (this=0x7fffd7fff090, g=0x7fffe0025b40, am=0x7fffd7fff1b0 "DSN=ConnectEnginePostgresql;UID=mtr;PWD=mtr", po
ff=32767) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/tabext.cpp:127


For creation of table check function <<connect_assisted_discovery>>

#2  0x00005555561de5c8 in connect_assisted_discovery (thd=0x7fffe0000d28, table_s=0x7ffff15a2fa0, create_info=0x7ffff15a3b50
) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/ha_connect.cc:6028

