use test;
create table vips (vip_id int primary key, name varchar(10));
insert into vips values (1, "anel"),(2,"melisa"),(3,"majra"),(4,"tarik");	

create table guests (guest_id int primary key, name varchar(10));
insert into guests values (1, "g1"),(2,"anel"),(3,"g2"),(4,"melisa"),(5,"g3");

# Inner join without `ON` keyword - Cartesian product (4 rows x 5 rows = 20 rows)
# compares each row of first table with each row of second table
/*
MariaDB [test]> select * from vips v inner join guests g;
+--------+--------+----------+--------+
| vip_id | name   | guest_id | name   |
+--------+--------+----------+--------+
|      1 | anel   |        1 | g1     |
|      2 | melisa |        1 | g1     |
|      3 | majra  |        1 | g1     |
|      4 | tarik  |        1 | g1     |
|      1 | anel   |        2 | anel   |
|      2 | melisa |        2 | anel   |
|      3 | majra  |        2 | anel   |
|      4 | tarik  |        2 | anel   |
|      1 | anel   |        3 | g2     |
|      2 | melisa |        3 | g2     |
|      3 | majra  |        3 | g2     |
|      4 | tarik  |        3 | g2     |
|      1 | anel   |        4 | melisa |
|      2 | melisa |        4 | melisa |
|      3 | majra  |        4 | melisa |
|      4 | tarik  |        4 | melisa |
|      1 | anel   |        5 | g3     |
|      2 | melisa |        5 | g3     |
|      3 | majra  |        5 | g3     |
|      4 | tarik  |        5 | g3     |
+--------+--------+----------+--------+
20 rows in set (0.001 sec)
*/

# Inner join on same IDs
/*
MariaDB [test]> select * from vips v inner join guests g on v.vip_id=g.guest_id; 
+--------+--------+----------+--------+
| vip_id | name   | guest_id | name   |
+--------+--------+----------+--------+
|      1 | anel   |        1 | g1     |
|      2 | melisa |        2 | anel   |
|      3 | majra  |        3 | g2     |
|      4 | tarik  |        4 | melisa |
+--------+--------+----------+--------+
*/

# Inner join on same names (instead of `inner join` we could use `cross join`)
/*
MariaDB [test]> select * from vips v inner join guests g on v.name=g.name;
+--------+--------+----------+--------+
| vip_id | name   | guest_id | name   |
+--------+--------+----------+--------+
|      1 | anel   |        2 | anel   |
|      2 | melisa |        4 | melisa |
+--------+--------+----------+--------+
*/

# Inner join with `using` keyword on columns that have the same name
/*
MariaDB [test]> select * from vips v cross join guests g using(name);
+--------+--------+----------+
| name   | vip_id | guest_id |
+--------+--------+----------+
| anel   |      1 |        2 |
| melisa |      2 |        4 |
+--------+--------+----------+
*/
 
# Left (outer) join - vips (4 rows)- left table
# Compare each row of left table (vips) with row of right table (guests) based on condition
/*
MariaDB [test]> select * from vips v left join guests g on v.name=g.name;
+--------+--------+----------+--------+
| vip_id | name   | guest_id | name   |
+--------+--------+----------+--------+
|      1 | anel   |        2 | anel   |
|      2 | melisa |        4 | melisa |
|      3 | majra  |     NULL | NULL   |
|      4 | tarik  |     NULL | NULL   |
+--------+--------+----------+--------+
4 rows in set (0.001 sec)

*/

# Left (outer) join - guests (5 rows) - left table
# Compare each row of left table (guests) with row of right table (vips) based on condition
/*
MariaDB [test]> select * from guests g left join vips v on v.name=g.name;
+----------+--------+--------+--------+
| guest_id | name   | vip_id | name   |
+----------+--------+--------+--------+
|        2 | anel   |      1 | anel   |
|        4 | melisa |      2 | melisa |
|        1 | g1     |   NULL | NULL   |
|        3 | g2     |   NULL | NULL   |
|        5 | g3     |   NULL | NULL   |
+----------+--------+--------+--------+
5 rows in set (0.001 sec)
*/

# Left (outer) join without NULL - use `where` condition
/*
MariaDB [test]> select * from guests g left join vips v on v.name=g.name where v.vip_id is not null;
+----------+--------+--------+--------+
| guest_id | name   | vip_id | name   |
+----------+--------+--------+--------+
|        2 | anel   |      1 | anel   |
|        4 | melisa |      2 | melisa |
+----------+--------+--------+--------+
*/

# Right join - takes right table and show all rows
/*
MariaDB [test]> select * from vips v right join guests g on v.name=g.name;
+--------+--------+----------+--------+
| vip_id | name   | guest_id | name   |
+--------+--------+----------+--------+
|      1 | anel   |        2 | anel   |
|      2 | melisa |        4 | melisa |
|   NULL | NULL   |        1 | g1     |
|   NULL | NULL   |        3 | g2     |
|   NULL | NULL   |        5 | g3     |
+--------+--------+----------+--------+
5 rows in set (0.001 sec)

MariaDB [test]>  select * from vips v right join guests g using(name);
+--------+----------+--------+
| name   | guest_id | vip_id |
+--------+----------+--------+
| anel   |        2 |      1 |
| melisa |        4 |      2 |
| g1     |        1 |   NULL |
| g2     |        3 |   NULL |
| g3     |        5 |   NULL |
+--------+----------+--------+
5 rows in set (0.001 sec)

*/


# Full join (takes left union right join)
# cannot use `using(column_name)`
/*
MariaDB [test]> select * from vips v left join guests g on v.name=g.name union select * from vips v right join guests g on v.name=g.name;
+--------+--------+----------+--------+
| vip_id | name   | guest_id | name   |
+--------+--------+----------+--------+
|      1 | anel   |        2 | anel   |
|      2 | melisa |        4 | melisa |
|      3 | majra  |     NULL | NULL   |
|      4 | tarik  |     NULL | NULL   |
|   NULL | NULL   |        1 | g1     |
|   NULL | NULL   |        3 | g2     |
|   NULL | NULL   |        5 | g3     |
+--------+--------+----------+--------+
7 rows in set (0.001 sec)

MariaDB [test]> select * from vips v left join guests g on v.name=g.name union select * from vips v right join guests g using(name);
ERROR 1222 (21000): The used SELECT statements have a different number of columns

MariaDB [test]> select * from vips v left join guests g using(name)  union select * from vips v right join guests g using(name);
+--------+--------+----------+
| name   | vip_id | guest_id |
+--------+--------+----------+
| anel   |      1 |        2 |
| melisa |      2 |        4 |
| majra  |      3 |     NULL |
| tarik  |      4 |     NULL |
| anel   |      2 |        1 |
| melisa |      4 |        2 |
| g1     |      1 |     NULL |
| g2     |      3 |     NULL |
| g3     |      5 |     NULL |
+--------+--------+----------+
9 rows in set (0.001 sec)

*/
# Self join
/*
MariaDB [test]> select * from vips v1, vips v2;
+--------+--------+--------+--------+
| vip_id | name   | vip_id | name   |
+--------+--------+--------+--------+
|      1 | anel   |      1 | anel   |
|      2 | melisa |      1 | anel   |
|      3 | majra  |      1 | anel   |
|      4 | tarik  |      1 | anel   |
|      1 | anel   |      2 | melisa |
|      2 | melisa |      2 | melisa |
|      3 | majra  |      2 | melisa |
|      4 | tarik  |      2 | melisa |
|      1 | anel   |      3 | majra  |
|      2 | melisa |      3 | majra  |
|      3 | majra  |      3 | majra  |
|      4 | tarik  |      3 | majra  |
|      1 | anel   |      4 | tarik  |
|      2 | melisa |      4 | tarik  |
|      3 | majra  |      4 | tarik  |
|      4 | tarik  |      4 | tarik  |
+--------+--------+--------+--------+
16 rows in set (0.001 sec)

MariaDB [test]> select v1.vip_id as id1, v2.vip_id as id2, v1.name as vips1, v2.name as vips2 from vips v1, vips v2;
+-----+-----+--------+--------+
| id1 | id2 | vips1  | vips2  |
+-----+-----+--------+--------+
|   1 |   1 | anel   | anel   |
|   2 |   1 | melisa | anel   |
|   3 |   1 | majra  | anel   |
|   4 |   1 | tarik  | anel   |
|   1 |   2 | anel   | melisa |
|   2 |   2 | melisa | melisa |
|   3 |   2 | majra  | melisa |
|   4 |   2 | tarik  | melisa |
|   1 |   3 | anel   | majra  |
|   2 |   3 | melisa | majra  |
|   3 |   3 | majra  | majra  |
|   4 |   3 | tarik  | majra  |
|   1 |   4 | anel   | tarik  |
|   2 |   4 | melisa | tarik  |
|   3 |   4 | majra  | tarik  |
|   4 |   4 | tarik  | tarik  |
+-----+-----+--------+--------+
16 rows in set (0.001 sec)

MariaDB [test]> select v1.vip_id as id1, v2.vip_id as id2, v1.name as vips1, v2.name as vips2 from vips v1, vips v2 where v1.vip_id <> v2.vip_id;
+-----+-----+--------+--------+
| id1 | id2 | vips1  | vips2  |
+-----+-----+--------+--------+
|   2 |   1 | melisa | anel   |
|   3 |   1 | majra  | anel   |
|   4 |   1 | tarik  | anel   |
|   1 |   2 | anel   | melisa |
|   3 |   2 | majra  | melisa |
|   4 |   2 | tarik  | melisa |
|   1 |   3 | anel   | majra  |
|   2 |   3 | melisa | majra  |
|   4 |   3 | tarik  | majra  |
|   1 |   4 | anel   | tarik  |
|   2 |   4 | melisa | tarik  |
|   3 |   4 | majra  | tarik  |
+-----+-----+--------+--------+
12 rows in set (0.001 sec)


# Order by + limit
MariaDB [test]> select v1.vip_id as id1, v2.vip_id as id2, v1.name as vips1, v2.name as vips2 from vips v1, vips v2 where v1.vip_id <> v2.vip_id order by v1.name asc limit 5;
+-----+-----+-------+--------+
| id1 | id2 | vips1 | vips2  |
+-----+-----+-------+--------+
|   1 |   2 | anel  | melisa |
|   1 |   3 | anel  | majra  |
|   1 |   4 | anel  | tarik  |
|   3 |   4 | majra | tarik  |
|   3 |   1 | majra | anel   |
+-----+-----+-------+--------+
5 rows in set (0.001 sec)

*/




