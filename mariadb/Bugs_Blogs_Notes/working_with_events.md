
## Creating event

- Follow https://mariadb.com/kb/en/create-event/
### Create user with enough privilege
1. User has to have EVENT privilege on database level to create/drop/alter event
```sql
MariaDB [test]> create user my_user@localhost identified by 'pass';
Query OK, 0 rows affected (0.015 sec)

MariaDB [test]> grant all privileges on test.* to my_user@localhost;
Query OK, 0 rows affected (0.015 sec)

```
2. Login with new user
```bash
$ mariadb -umy_user -ppass
```

### Create test table containg json data
Here you have 2 options
1. using json_table
2. using json data type (we will use this)

#### Create table from json data using `json_table` function (10.6+)
You can follow https://mariadb.com/kb/en/json_table/
```sql
# Create json document
set @json='
[
  {"name":"Laptop", "color":"black", "price":"1000"},
  {"name":"Jeans",  "color":"blue"}
]';

# This is not a table
MariaDB [test]> select * from json_table(@json, '$[*]' 
    ->   columns(
    ->    name  varchar(10) path '$.name', 
    ->    color varchar(10) path '$.color',
    ->    price decimal(8,2) path '$.price' ) 
    -> ) as jt;
+--------+-------+---------+
| name   | color | price   |
+--------+-------+---------+
| Laptop | black | 1000.00 |
| Jeans  | blue  |    NULL |
+--------+-------+---------+
2 rows in set (0.000 sec)

# You need to create the table
MariaDB [test]> create table myjsontbl as (select * from json_table(@json, '$[*]'    columns(    name  varchar(10) path '$.name',     color varchar(10) path '$.color',    price decimal(8,2) path '$.price' )  ) as jt);
Query OK, 2 rows affected (0.028 sec)
Records: 2  Duplicates: 0  Warnings: 0

MariaDB [test]> show tables;
+----------------+
| Tables_in_test |
+----------------+
| myjsontbl      |
+----------------+
1 row in set (0.000 sec)

MariaDB [test]> show create table myjsontbl\G
*************************** 1. row ***************************
       Table: myjsontbl
Create Table: CREATE TABLE `myjsontbl` (
  `name` varchar(10) DEFAULT NULL,
  `color` varchar(10) DEFAULT NULL,
  `price` decimal(8,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
1 row in set (0.000 sec)


```

####  You can create a field/column with json data
(see JSON data type https://mariadb.com/kb/en/json-data-type/)
```sql
MariaDB [test]> create table myjsontbl(kit json);
Query OK, 0 rows affected (0.025 sec)

MariaDB [test]> show create table myjsontbl\G
*************************** 1. row ***************************
       Table: myjsontbl
Create Table: CREATE TABLE `myjsontbl` (
  `kit` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`kit`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
1 row in set (0.000 sec)

MariaDB [test]> insert into myjsontbl values ('{"user":"luffy", "amount":1}'),('{"user":"zoro", "amount":"2"}');
Query OK, 2 rows affected (0.015 sec)
Records: 2  Duplicates: 0  Warnings: 0

MariaDB [test]> select * from myjsontbl;
+-------------------------------+
| kit                           |
+-------------------------------+
| {"user":"luffy", "amount":1}  |
| {"user":"zoro", "amount":"2"} |
+-------------------------------+
2 rows in set (0.000 sec)
```

2. You can use json functions 
```sql
MariaDB [test]> select json_type(kit) from myjsontbl;
+----------------+
| json_type(kit) |
+----------------+
| OBJECT         |
| OBJECT         |
+----------------+
2 rows in set (0.000 sec)


MariaDB [test]> select json_valid(kit) from myjsontbl;
+-----------------+
| json_valid(kit) |
+-----------------+
|               1 |
|               1 |
+-----------------+
2 rows in set (0.000 sec)



MariaDB [test]> select json_keys(kit) from myjsontbl;
+--------------------+
| json_keys(kit)     |
+--------------------+
| ["user", "amount"] |
| ["user", "amount"] |
+--------------------+
2 rows in set (0.000 sec)


MariaDB [test]> select json_value(kit,'$.user') from myjsontbl;
+--------------------------+
| json_value(kit,'$.user') |
+--------------------------+
| luffy                    |
| zoro                     |
+--------------------------+
2 rows in set (0.000 sec)

MariaDB [test]> select json_value(kit,'$.amount') from myjsontbl;
+----------------------------+
| json_value(kit,'$.amount') |
+----------------------------+
| 1                          |
| 2                          |
+----------------------------+
2 rows in set (0.000 sec)

# How to return first or second object ?

MariaDB [test]> select json_detailed(kit) from myjsontbl;
+-------------------------------------------+
| json_detailed(kit)                        |
+-------------------------------------------+
| {
    "user": "luffy",
    "amount": 1
}  |
| {
    "user": "zoro",
    "amount": "2"
} |
+-------------------------------------------+
2 rows in set (0.000 sec)


MariaDB [test]> select json_extract(kit, '$.user'),json_extract(kit, '$.amount') from myjsontbl;
+-----------------------------+-------------------------------+
| json_extract(kit, '$.user') | json_extract(kit, '$.amount') |
+-----------------------------+-------------------------------+
| "luffy"                     | 1                             |
| "zoro"                      | "2"                           |
+-----------------------------+-------------------------------+
2 rows in set (0.000 sec)

# Accessing array index
MariaDB [test]> select json_extract(kit,'$.*') from myjsontbl;
+-------------------------+
| json_extract(kit,'$.*') |
+-------------------------+
| ["luffy", 1]            |
| ["zoro", "2"]           |
+-------------------------+
2 rows in set (0.000 sec)


MariaDB [test]> select * from myjsontbl where json_contains(kit, 1, '$.amount');
+------------------------------+
| kit                          |
+------------------------------+
| {"user":"luffy", "amount":1} |
+------------------------------+
1 row in set (0.000 sec)

```

3. Then you can try to update your table
```sql
MariaDB [test]> update myjsontbl set kit = json_replace(kit, '$.amount',3);
Query OK, 2 rows affected (0.004 sec)
Rows matched: 2  Changed: 2  Warnings: 0

MariaDB [test]> select json_detailed(kit) from myjsontbl;
+------------------------------------------+
| json_detailed(kit)                       |
+------------------------------------------+
| {
    "user": "luffy",
    "amount": 3
} |
| {
    "user": "zoro",
    "amount": 3
}  |
+------------------------------------------+
2 rows in set (0.000 sec)
```


- Additional
https://medium.com/mariadb/json-tables-with-mariadb-578238cec0c6


#### Now you can create an event
```sql

```

