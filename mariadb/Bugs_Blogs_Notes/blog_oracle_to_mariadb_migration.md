# Blog migrate from Oracle to MariaDB

# Introduction
In this blog we are going to learn how to migrate data from Oracle to MariaDB.
At the beginning we'll learn basis about the Oracle database and on demo example we'll create some table in Oracle and migrate data to MariaDB.
To migrate data from Oracle there are 2 ways:
1. dump Oracle data to CSV and load data in MariaDB,
2. use Connect SE to create or insert into a table from Oracle's source definition. 

For demonstration, we are going to use docker container with Oracle Express Edition (XE) image.
On the same container MariaDB instance will be started and data migration will happen.

# Oracle terminlogy
To have a clear picture what changes are going to be done, let's explain basis
terminology what we are going to use later in examples.

## About SID
In Oracle, `SID` stands for system identifier, and it is a unique name that identifies a specific Oracle database instance on a particular server or system. Each Oracle database instance has a unique SID assigned to it, which distinguishes it from other instances on the same system and one can check specific database instance
with [ORACLE_SID](https://docs.oracle.com/en/database/oracle/oracle-database/21/ntqrf/oracle-sid.html) environment variable.
SID is only used if you want an alternative way to connect to a container database.In our example it will be `XE`.

## About listener
Listener listens for incoming client connections to the Oracle database.
The listener is responsible for accepting client connections and routing them to the appropriate Oracle database instance.
By default listens on port `1521`.
Changing the port and adding new services and networks addresses which listner should be listen to,
can be added in `listener.ora` file.
It is controled by `lsnrctl` utility.

## About services
A service name is a unique identifier for a specific service that is used to establish a connection between the client and the database. Each service name is associated with a connect descriptor located in `tnsnames.ora` file,
that is used by the client to resolve network address of the listener that hosts the service.
Testing the service name can be done using `tnsping` utility.

## About users
There are default users `SYS`,`SYSTEM`, `PDB_ADMIN` that can be used to connect with specified `ORACLE_PWD`environment variable.
The `pdbadmin` account has privileges that allow it to manage PDBs, create new PDBs, and perform other administrative tasks related to the multitenant architecture.

## About CDB & PDB
Oracle has introduced concept of the multitenant architecture with the container database (`CDB`) storing zero or
more plugabble databases (`PDB`) [oracle-pdb].
Each pluggable database is essentially a self-contained database that can be managed independently,
but is hosted within the context of the container database.
`pdbadmin` is a user account in Oracle Database that is used to manage pluggable databases (`PDB`) (https://www.databasestar.com/oracle-pdb/).


# Oracle source data
- At the first attempt, I tried to use images from [oracle registry](https://container-registry.oracle.com/), but after days of trying I couldn't make ODBC connector
work on AMD platform.
- Second attempt was to use Oracle's [docker-images](https://github.com/oracle/docker-images.git) repository and I used
```bash
 $ git clone https://github.com/oracle/docker-images.git
 $ cd docker-images/OracleDatabase/SingleInstance/dockerfiles
 # It will take some time
 $ ./buildContainerImage.sh -x -v 18.4.0 -o '--build-arg SLIMMING=false'
  Build completed in 390 seconds.
 $ docker images|grep oracle
 REPOSITORY                                          TAG         IMAGE ID       CREATED          SIZE
 oracle/database                                     18.4.0-xe   4a141cc0a851   10 seconds ago   6.03GB
```

## Start the container
- An environment variables that are set to default and that will be used are
```bash
-e ORACLE_SID: The Oracle Database SID that should be used (default: XE).
-e ORACLE_PDB: The Oracle Database PDB name that should be used (default: XEPDB1).
-e ORACLE_PWD: The Oracle Database SYS, SYSTEM and PDB_ADMIN password (default: auto generated).
```
- Start the container in the background.
```bash
$ docker run --name oracle18xe --rm -d -p 1521:1521 -p 5500:5500 -e ORACLE_PWD=oracle oracle/database:18.4.0-xe
#Output
ORACLE PASSWORD FOR SYS AND SYSTEM: oracle
Specify a password to be used for database accounts. Oracle recommends that the password entered should be at least 8 characters in length, contain at least 1 uppercase character, 1 lower case character and 1 digit [0-9]. Note that the same password will be used for SYS, SYSTEM and PDBADMIN accounts:
Confirm the password:
Configuring Oracle Listener.
Listener configuration succeeded.
Configuring Oracle Database XE.
Enter SYS user password: 
*******
Enter SYSTEM user password: 
*********
Enter PDBADMIN User Password: 
******
Prepare for db operation
7% complete
Copying database files
29% complete
Creating and starting Oracle instance
30% complete
31% complete
34% complete
38% complete
41% complete
43% complete
Completing Database Creation
47% complete
50% complete
Creating Pluggable Databases
54% complete
71% complete
Executing Post Configuration Actions
93% complete
Running Custom Scripts
100% complete
Database creation complete. For details check the logfiles at:
 /opt/oracle/cfgtoollogs/dbca/XE.
Database Information:
Global Database Name:XE
System Identifier(SID):XE
Look at the log file "/opt/oracle/cfgtoollogs/dbca/XE/XE.log" for further details.

Connect to Oracle Database using one of the connect strings:
     Pluggable database: 7f2f6dd37f01/XEPDB1
     Multitenant container database: 7f2f6dd37f01
Use https://localhost:5500/em to access Oracle Enterprise Manager for Oracle Database XE
The Oracle base remains unchanged with value /opt/oracle
#########################
DATABASE IS READY TO USE!
#########################
The following output is now a tail of the alert.log:
2023-04-03T10:14:42.163893+00:00
XEPDB1(3):Resize operation completed for file# 10, old size 358400K, new size 368640K
2023-04-03T10:14:44.390892+00:00
XEPDB1(3):CREATE SMALLFILE TABLESPACE "USERS" LOGGING  DATAFILE  '/opt/oracle/oradata/XE/XEPDB1/users01.dbf' SIZE 5M REUSE AUTOEXTEND ON NEXT  1280K MAXSIZE UNLIMITED  EXTENT MANAGEMENT LOCAL  SEGMENT SPACE MANAGEMENT  AUTO
XEPDB1(3):Completed: CREATE SMALLFILE TABLESPACE "USERS" LOGGING  DATAFILE  '/opt/oracle/oradata/XE/XEPDB1/users01.dbf' SIZE 5M REUSE AUTOEXTEND ON NEXT  1280K MAXSIZE UNLIMITED  EXTENT MANAGEMENT LOCAL  SEGMENT SPACE MANAGEMENT  AUTO
XEPDB1(3):ALTER DATABASE DEFAULT TABLESPACE "USERS"
XEPDB1(3):Completed: ALTER DATABASE DEFAULT TABLESPACE "USERS"
2023-04-03T10:14:45.465773+00:00
ALTER PLUGGABLE DATABASE XEPDB1 SAVE STATE
Completed: ALTER PLUGGABLE DATABASE XEPDB1 SAVE STATE
```

- You should get the status `healthy` of your container (`docker ps`) before proceeding
```bash
$ docker ps
CONTAINER ID   IMAGE                       COMMAND                  CREATED       STATUS                 PORTS                                                                                  NAMES
7f2f6dd37f01   oracle/database:18.4.0-xe   "/bin/sh -c 'exec $O…"   2 hours ago   Up 2 hours (healthy)   0.0.0.0:1521->1521/tcp, :::1521->1521/tcp, 0.0.0.0:5500->5500/tcp, :::5500->5500/tcp   oracle18xe

$ docker ps --format "table {{.Status}}"
STATUS
Up About an hour (healthy)

```

- More about see [1- Oracle running container](https://github.com/oracle/docker-images/tree/main/OracleDatabase/SingleInstance#running-oracle-database-21c18c-express-edition-in-a-container)

### Note for Anel:
- [2 - valeries](http://mysqlentomologist.blogspot.com/2017/04/accessing-oracle-tables-via-mariadb.html) used `-e ORACLE_ALLOW_REMOTE=true` but it is not an option.
- [3- charsets](https://docs.oracle.com/database/121/NLSPG/applocaledata.htm#NLSPG014)

## Check the service names in container
- Service names used as connect descriptor are defined in `tnsnames.ora` on server and
  by default with docker image there are 2 `XE` and `XEPDB1` that we may use to connect with our client.
  There is also default listener port and network address that will client use in order to connect to the listener.
```bash
bash-4.2# cat $ORACLE_HOME/network/admin/tnsnames.ora
# tnsnames.ora Network Configuration File:
XE =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = XE)
    )
  )

LISTENER_XE =
  (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521))

XEPDB1 =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = XEPDB1)
    )
  )
```

## Check listener in container
Connect to the container and check following
- listener configuration `listener.ora`
  It defines TCP port and host and IPC connection on which listener listens
```bash
bash-4.2# cat $ORACLE_HOME/network/admin/listener.ora 
# listener.ora Network Configuration File:
         
         SID_LIST_LISTENER = 
           (SID_LIST =
             (SID_DESC =
               (SID_NAME = PLSExtProc)
               (ORACLE_HOME = /opt/oracle/product/18c/dbhomeXE)
               (PROGRAM = extproc)
             )
           )
         
         LISTENER =
           (DESCRIPTION_LIST =
             (DESCRIPTION =
               (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC_FOR_XE))
               (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521))
             )
           )
         
         DEFAULT_SERVICE_LISTENER = (XE)
```
- `lsnrctl services`
  Inovking this command we get services that are defined
  in `tnsnames.ora` file on which listener listens to.
  There are 4 services:
  - `XE` - defined in `tnsnames.ora`
  - `xepdb1` - defined in `tnsnames.ora`
  - `XEXDB`
  - `f86f5d81e3a40b54e053020011ac03ad`
  It can be checked by quering the view `ALL_SERVICES` that `XE` service is configured to connect to root CDB `CDB$ROOT` and that `xepdb1` is configured to connect to pluggable `XEPDB1` database.
```bash
bash-4.2# lsnrctl services

LSNRCTL for Linux: Version 18.0.0.0.0 - Production on 03-APR-2023 14:15:40

Copyright (c) 1991, 2018, Oracle.  All rights reserved.

Connecting to (ADDRESS=(PROTOCOL=tcp)(HOST=)(PORT=1521))
Services Summary...
Service "XE" has 1 instance(s).
  Instance "XE", status READY, has 1 handler(s) for this service...
    Handler(s):
      "DEDICATED" established:10 refused:0 state:ready
         LOCAL SERVER
Service "XEXDB" has 1 instance(s).
  Instance "XE", status READY, has 1 handler(s) for this service...
    Handler(s):
      "D000" established:0 refused:0 current:0 max:1022 state:ready
         DISPATCHER <machine: 7888669ad116, pid: 2579>
         (ADDRESS=(PROTOCOL=tcp)(HOST=7888669ad116)(PORT=46211))
Service "f86f5d81e3a40b54e053020011ac03ad" has 1 instance(s).
  Instance "XE", status READY, has 1 handler(s) for this service...
    Handler(s):
      "DEDICATED" established:10 refused:0 state:ready
         LOCAL SERVER
Service "xepdb1" has 1 instance(s).
  Instance "XE", status READY, has 1 handler(s) for this service...
    Handler(s):
      "DEDICATED" established:10 refused:0 state:ready
         LOCAL SERVER
The command completed successfully
```

- `lnsrctl status`
  Useful command to check about the status of listener
```bash
bash-4.2# lsnrctl status

LSNRCTL for Linux: Version 18.0.0.0.0 - Production on 03-APR-2023 12:47:39

Copyright (c) 1991, 2018, Oracle.  All rights reserved.

Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=2b2b2e9be7a0)(PORT=1521)))
STATUS of the LISTENER
------------------------
Alias                     LISTENER
Version                   TNSLSNR for Linux: Version 18.0.0.0.0 - Production
Start Date                03-APR-2023 12:47:08
Uptime                    0 days 0 hr. 0 min. 31 sec
Trace Level               off
Security                  ON: Local OS Authentication
SNMP                      OFF
Default Service           XE
Listener Parameter File   /opt/oracle/product/18c/dbhomeXE/network/admin/listener.ora
Listener Log File         /opt/oracle/diag/tnslsnr/2b2b2e9be7a0/listener/alert/log.xml
Listening Endpoints Summary...
  (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=2b2b2e9be7a0)(PORT=1521)))
  (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1521)))
Services Summary...
Service "XE" has 1 instance(s).
  Instance "XE", status READY, has 1 handler(s) for this service...
The command completed successfully
```

### Check the service names using tnsping
When we know the names of service, before connecting to the database we can check for which service names we can connect.
```bash
$ docker exec -it oracle18xe tnsping XEPDB1
Used TNSNAMES adapter to resolve the alias
Attempting to contact (DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = XEPDB1)))
OK (0 msec)

$ docker exec -it oracle18xe tnsping XE
Used TNSNAMES adapter to resolve the alias
Attempting to contact (DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = XE)))
OK (0 msec)
```
Note that we cannot use `XEXDB` and `f86f5d81e3a40b54e053020011ac03ad` since they are not defined in `tnsnames.ora` and `tnsping`-ing it failed to resolve the name.

## Connect with the client to the databases
- As an client `sqlplus` utility will be used to connect with Oracle server.
- There are multiple ways to connect to the database using different accounts and/or services:
1. Using `sys` user (super user) needs to be connected as `sysdba` or `sysoper` to PDB or service.
`sysdba` and `sysoper` are system privileges to work on root (CDB) database.
```bash
$ docker exec -it oracle18xe sqlplus sys/oracle@XEPDB1 as sysdba
$ docker exec -it oracle18xe sqlplus sys/oracle@XEPDB1 as sysoper
$ docker exec -it oracle18xe sqlplus sys/oracle@XE as sysdba
```
2. Using `system` user, standard user that doesn't have privilege as super user, use the same service names
```bash
$ docker exec -it oracle18xe sqlplus system/oracle@XE
```
3. Using `pdbadmin` user, that can be connected only to `XEPDB1` pluggable database.
```bash
$ docker exec -it oracle18xe sqlplus pdbadmin/oracle@XEPDB1
```

## Create data in Oracle database
Further pluggable database `XEPDB1` with standard `SYSTEM` user will be used.
`pdbadmin` doesn't have privileges to create table.
After that, table will be created and some data inserted.
```sql
$ docker exec -it oracle18xe sqlplus sysetm/oracle@XEPDB1
Connected to:
Oracle Database 18c Express Edition Release 18.0.0.0.0 - Production
Version 18.4.0.0.0

SQL> show con_name;

CON_NAME
------------------------------
XEPDB1

SQL> -- Create
SQL> create table t(t number);

Table created.

SQL> desc t;
 Name					   Null?    Type
 ----------------------------------------- -------- ----------------------------
 T						    NUMBER

SQL> -- Insert
SQL> insert all into t(t) values (1) into t(t) values (2) into t(t) values(3) select 1 from dual;

3 rows created.

SQL> select * from t;

	 T
----------
	 1
	 2
	 3
```

Now we have data that we want to migrate to MariaDB

# MariaDB side
We need to install MariaDB on running container and install MariaDB connect plugin

# Install MariaDB
Before installing we will need some dependecies, like epel repository and editor
```bash
$ docker exec -it oracle bash
$ yum update
$ yum install http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm vi
```
We will install from [MariaDB Foundation repo-config](https://mariadb.org/download/?t=repo-config) repository
and download latest 11.0 RC version.
```bash
$ cat /etc/yum.repos.d/mariadb.repo 
# MariaDB 11.0 [RC] CentOS repository list - created 2023-04-04 11:01 UTC
# https://mariadb.org/download/
[mariadb]
name = MariaDB
# rpm.mariadb.org is a dynamic mirror if your preferred mirror goes offline. See https://mariadb.org/mirrorbits/ for details.
# baseurl = https://rpm.mariadb.org/11.0/centos/$releasever/$basearch
baseurl = https://ftp.bme.hu/pub/mirrors/mariadb/yum/11.0/centos/$releasever/$basearch
module_hotfixes = 1
# gpgkey = https://rpm.mariadb.org/RPM-GPG-KEY-MariaDB
gpgkey = https://ftp.bme.hu/pub/mirrors/mariadb/yum/RPM-GPG-KEY-MariaDB
gpgcheck = 1

$ yum repolist
Loaded plugins: ovl
repo id                                                                                repo name                                                                                                      status
epel/x86_64                                                                            Extra Packages for Enterprise Linux 7 - x86_64                                                                 13770
mariadb/7Server/x86_64                                                                 MariaDB                                                                                                           49
ol7_latest/x86_64                                                                      Oracle Linux 7Server Latest (x86_64)                                                                           25426
```

Now install the MariaDB server
```bash
$ yum install MariaDB-server
$ rpm -q -a|grep -e Maria
MariaDB-common-11.0.1-1.el7.centos.x86_64
MariaDB-client-compat-11.0.1-1.el7.centos.noarch
MariaDB-server-compat-11.0.1-1.el7.centos.noarch
MariaDB-compat-11.0.1-1.el7.centos.x86_64
MariaDB-client-11.0.1-1.el7.centos.x86_64
MariaDB-server-11.0.1-1.el7.centos.x86_64
```

From this step there are 2 ways how to migrate data
# Case 1: Dump data in Oracle in CSV form
Oracle XE doesn't support dump data from sqlplus, that could be done
using `spool` command.
- Example how it should like:
First we will dump data to CSV by creating the script `dumpOracle`
```sql
SQL> edit dumpOracle
# Write the content
SET MARKUP CSV ON
SET HEADING OFF
SET FEEDBACK OFF
SET COLSEP ','
SET TRIMSPOOL ON
SPOOL table_oracle.csv
SELECT t FROM t;
# execute the script
SQL> @dumpOracle
SQL>  SPOOL OFF
```

TL;DR
- However there is `expdp` utility
`chown oracle:oinstall /tmp/newdir` and it is enough to create a directory
as system user.

- Make sure to create a directory, and be sure that oracle user has right to write to it.
- We need to create a directory as an `system` user, but and granting privileges to that user should be done from `sysdba`, since current user cannot grant privileges to it self and connection should happen from `XE` root container DB, and not from pluggable db.

With `system` user create directory:
```bash
> CREATE DIRECTORY SYSTEM_DIR AS '/tmp/sysdir/';
```
With `sysdba` user:
```bash
$ sqlplus sys/oracle@XE as sysdba
```

Run queries on `sysdba`
```sql
SQL> ALTER USER system IDENTIFIED BY oracle ACCOUNT UNLOCK CONTAINER=ALL;
SQL> GRANT READ, WRITE ON DIRECTORY SYSTEM_DIR TO SYSTEM;
SQL> select * from all_directories where DIRECTORY_NAME='SYSTEM_DIR';
```

- To grant the privileges log in as sysdba
```
$ sqlplus sys/oracle@XEPDB1 as sysdba;
```sql
SQL> GRANT READ, WRITE ON DIRECTORY TEST_DIR TO SYSTEM;
 GRANT READ, WRITE ON DIRECTORY MY_DIR2 TO SYSTEM;
 # See privileges
 SELECT * FROM USER_SYS_PRIVS;
 SELECT privilege FROM dba_sys_privs WHERE grantee = 'SYSTEM';
 SELECT * FROM DBA_DIRECTORIES WHERE DIRECTORY_NAME = 'MY_DIR2';
```
To see all directories
```sql
select * from all_directories where DIRECTORY_NAME='MY_DIR';
select * from all_directories where DIRECTORY_NAME='TEST_DIR';
OWNER
--------------------------------------------------------------------------------
DIRECTORY_NAME
--------------------------------------------------------------------------------
DIRECTORY_PATH
--------------------------------------------------------------------------------
ORIGIN_CON_ID
-------------
SYS
MY_DIR2
/tmp/dumps
	    1
```

- Execute
```bash
expdp system/oracle@XEPDB1 tables=t directory=MY_DIR2 dumpfile=oracle_table.dmp logfile=oracle_log.dmp
```
On MariaDB side
```sql
MariaDB [test]> create table t(t int);

LOAD DATA INFILE '/table_orace.csv'
INTO TABLE t
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

```
# Case 2: Using connect SE
## Install mariadb-connect package
```
$ yum install MariaDB-connect-engine
$ rpm -q -a|grep -e MariaDB-connect
MariaDB-connect-engine-10.3.38-1.el7.centos.x86_64
# Check shared library
$ ls /usr/lib64/mysql/plugin/|grep connect
ha_connect.so

# Check
bash-4.2# ls /usr/lib64/mysql/plugin/|grep connect
ha_connect.so
```

## Setup OracleODBC driver
- To create ODBC connection we need `unixODBC`driver that is dependency on `mariadb-connect`,
  so it is installed already
```bash
rpm -q -a|grep -e ODBC
unixODBC-2.3.1-14.0.1.el7.x86_64
```
`unixODBC` has utilites like `isql`(CLI SQL tool)  and `odbcinst` (CLI for ODBC configuration) that we are going to use later.
- After installing the driver manager, we need to connect to Oracle's database,
  using Oracle's ODBC driver.
- For that, ODBC driver `libsqora.so` shared library is used and we need to export the path to the environment `LD_LIBRARY_PATH`
```bash
# Export LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$ORACLE_HOME/lib/
```
- Set unixODBC driver, by writing `odbcinst.ini` file
  There are already connection unixODBC driver settings for MySQL and PostgreSQL,
  we need to update to use `OracleODBC` configuration
```bash
bash-4.2# cat /etc/odbcinst.ini 
...
[OracleODBC]
Description    = ODBC for Oracle
Driver         = /opt/oracle/product/18c/dbhomeXE/lib/libsqora.so.18.1
```

- Check the changes
```bash
bash-4.2# vim /etc/odbcinst.ini 
bash-4.2# odbcinst -q -d
[PostgreSQL]
[MySQL]
[OracleODBC]
```

## Setup ODBC data source name
- We need to add configuration to access the Oracle database
  using above step in `~/.odbc.ini` just like we have connected to the Oracle.
```bash
# Note it didn't work when XE was used with system
bash-4.2# cat ~/.odbc.ini 
[oracle]
Driver = OracleODBC
DSN = Oracle ODBC connection
ServerName = XEPDB1
UserID = system
Password = oracle
# Check
bash-4.2# odbcinst -q -s
[oracle]
```
## Check connection
- To check connection we may use `isql` utility
```bash
bash-4.2# isql -v oracle
+---------------------------------------+
| Connected!                            |
|                                       |
| sql-statement                         |
| help [tablename]                      |
| quit                                  |
|                                       |
+---------------------------------------+
SQL> select * from t;
+-----------------------------------------+
| T                                       |
+-----------------------------------------+
| 1                                       |
| 2                                       |
| 3                                       |
+-----------------------------------------+
SQLRowCount returns -1
3 rows fetched
```


## Start mysqld
- Start mariadb server and load Connect SE on startupe
```bash
$ mariadbd --user=root --plugin-load-add=ha_connect.so &
2023-01-16 16:03:23 0 [Note] mysqld (mysqld 10.3.37-MariaDB) starting as process 3181 ...
2023-01-16 16:03:23 0 [Note] CONNECT: Version 1.07.0003 June 06, 2021

Version: '10.3.37-MariaDB'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  MariaDB Server
```
### Check plugin
- Connect with the client 
```bash
$ mariadb -uroot -e "show plugins;"
---
| CONNECT                       | ACTIVE   | STORAGE ENGINE     | ha_connect.so | GPL     |
+-------------------------------+----------+--------------------+---------------+---------+
54 rows in set (0.001 sec)

```
### Create table on mariadb
- Create table using Connect SE by using ODBC connection to Oracle database with DSN that's set in previous step and select all data from table.
```bash
$ mariadb -uroot test
MariaDB [test]> create table table_maria engine=connect table_type=ODBC tabname='t' Connection='DSN=oracle' SRCDEF='select * from t';
Query OK, 0 rows affected (0.059 sec)

MariaDB [test]> select * from table_maria;
+------+
| T    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.052 sec)

MariaDB [test]> show create table table_maria \G
*************************** 1. row ***************************
       Table: table_maria
Create Table: CREATE TABLE `table_maria` (
  `T` double(40,0) DEFAULT NULL
) ENGINE=CONNECT DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci CONNECTION='DSN=oracle' `TABLE_TYPE`='ODBC' `TABNAME`='t' `SRCDEF`='select * from t'
1 row in set (0.000 sec)
```



## Links
[0] https://www.databasestar.com/oracle-pdb/
[1] https://github.com/oracle/docker-images/tree/main/OracleDatabase/
[2] http://mysqlentomologist.blogspot.com/2017/04/accessing-oracle-tables-via-mariadb.html
[2] https://container-registry.oracle.com/ 
SingleInstance#running-oracle-database-21c18c-express-edition-in-a-container
[4] https://jira.mariadb.org/browse/MDEV-24493
[5] https://docs.oracle.com/cd/B28359_01/network.111/b28317/tnsnames.htm#NETRF007
[6] https://super-unix.com/ubuntu/ubuntu-how-to-install-sqlplus/


# Interesting

- Check for services from `all_services` view (shows only
services registered by the listener)
```sql
SQL> describe all_services
 Name					   Null?    Type
 ----------------------------------------- -------- ----------------------------
 SERVICE_ID					    NUMBER
 NAME						    VARCHAR2(64)
 NAME_HASH					    NUMBER
 NETWORK_NAME					    VARCHAR2(512)
 CREATION_DATE					    DATE
 CREATION_DATE_HASH				    NUMBER
 FAILOVER_METHOD				    VARCHAR2(64)
 FAILOVER_TYPE					    VARCHAR2(64)
 FAILOVER_RETRIES				    NUMBER(10)
 FAILOVER_DELAY 				    NUMBER(10)
 MIN_CARDINALITY				    NUMBER
 MAX_CARDINALITY				    NUMBER
 GOAL						    VARCHAR2(12)
 DTP						    VARCHAR2(1)
 ENABLED					    VARCHAR2(3)
 AQ_HA_NOTIFICATIONS				    VARCHAR2(3)
 CLB_GOAL					    VARCHAR2(5)
 EDITION					    VARCHAR2(128)
 COMMIT_OUTCOME 				    VARCHAR2(3)
 RETENTION_TIMEOUT				    NUMBER
 REPLAY_INITIATION_TIMEOUT			    NUMBER
 SESSION_STATE_CONSISTENCY			    VARCHAR2(128)
 GLOBAL_SERVICE 				    VARCHAR2(3)
 PDB						    VARCHAR2(128)
 SQL_TRANSLATION_PROFILE			    VARCHAR2(261)
 MAX_LAG_TIME					    VARCHAR2(128)
 GSM_FLAGS					    NUMBER
 PQ_SVC 					    VARCHAR2(64)
 STOP_OPTION					    VARCHAR2(13)
 FAILOVER_RESTORE				    VARCHAR2(6)
 DRAIN_TIMEOUT					    NUMBER


SQL> select name, pdb, global_service from all_services where name='xe';  

NAME
----------------------------------------------------------------
PDB
--------------------------------------------------------------------------------
GLO
---
xe
CDB$ROOT
NO


# Similar with view dba_service


SQL> select name, pdb from dba_services where name='xe';

NAME
----------------------------------------------------------------
PDB
--------------------------------------------------------------------------------
xe
CDB$ROOT


# However if connect via XEPDB1 service,
# we will get the service name XEPDB1 and that is responsible
# for XEPDB1 PDB

SQL>  select name, pdb from dba_services;
NAME
----------------------------------------------------------------
PDB
--------------------------------------------------------------------------------
XEPDB1
XEPDB1

```