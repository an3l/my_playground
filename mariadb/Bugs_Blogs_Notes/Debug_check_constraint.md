
# Debuging check constraint
```sql
create table t(t int,
check (t>0),
constraint check(t>1),
constraint t_named check(t>2));
```
- bt
```
Sql_cmd_create_table_like::execute -> create_info created
  mysql_create_table ->
    mysql_create_table_no_lock ->
      create_table_impl
        >build from frm there is no assisted discovery
        >fix_constraint_names <- If it is not automatic_name leave it as it is if not make unique constraint name.
        mysql_create_frm_image->
          mysql_create_frm_image->
            mysql_prepare_create_table ->
              >Assign create_info->check_constraint_list= &alter_info->check_constraint_list; where alter_info is from lex)
              >CHECK TABLE LEVEL CONSTRAINTS from alter_info->check_constraint_list
            build_frm_image-> (create buf as output)
              pack_vcols->
                >PATCH: field constraint checked here and field vs table constraints checked here too.
                pack_expression-> (here we will now expression length and save in create_info and vcol String)
              pack_header-> (assign create_info->field_check_constraints to 0, goes through real fields -not vcols)
              saved vcol->ptr()

```

- `pack_expression`
  - CONSTRAINT_2 `t` > 1 # end with '\000'
	```
	(gdb) x/50bc buf->ptr()+len_off+1
	+x/50bc buf->ptr()+len_off+1
	0x7fffed3d694b: 0 '\000'        12 '\f' 67 'C'  79 'O'  78 'N'  83 'S'  84 'T'  82 'R'
	0x7fffed3d6953: 65 'A'  73 'I'  78 'N'  84 'T'  95 '_'  50 '2'  96 '`'  116 't'
	0x7fffed3d695b: 96 '`'  32 ' '  62 '>'  32 ' '  49 '1'  0 '\000'        105 'i' 61 '='
	0x7fffed3d6963: -19 '\355'      -1 '\377'       127 '\177'      0 '\000'        0 '\000'        92 '\\' 8 '\b'  76 'L'
	0x7fffed3d696b: 88 'X'  0 '\000'        0 '\000'        1 '\001'        0 '\000'        -96 '\240'      105 'i' 61 '='
	0x7fffed3d6973: -19 '\355'      -1 '\377'       127 '\177'      0 '\000'        0 '\000'        62 '>'  -98 '\236'      82 'R'
	0x7fffed3d697b: 88 'X'  85 'U'
	```
- End of `pack_vcols`
```
(gdb) x/10bs buf->ptr()
+x/10bs buf->ptr()
0x7fffed3d692e: "\004\377\377\a"
0x7fffed3d6933: "\fCONSTRAINT_1`t` > 0\004\377\377\a"
0x7fffed3d694c: "\fCONSTRAINT_2`t` > 1\004\377\377\a"
0x7fffed3d6965: "\at_named`t` > 2"
0x7fffed3d6975: "\177"
0x7fffed3d6977: ""
0x7fffed3d6978: ">\236RXUU"
0x7fffed3d697f: ""
0x7fffed3d6980: "\240i=\355\377\177"
0x7fffed3d6987: ""

# see that type, 2B of field_nr: -1, 2B of 0 =[7,0]?, 1B of name_length =12(\f) or 7(\a)n and than expression
(gdb) x/60bc buf->ptr()
+x/60bc buf->ptr()
0x7fffed3d692e: 4 '\004'        -1 '\377'       -1 '\377'       7 '\a'  0 '\000'        12 '\f' 67 'C'  79 'O'
0x7fffed3d6936: 78 'N'  83 'S'  84 'T'  82 'R'  65 'A'  73 'I'  78 'N'  84 'T'
0x7fffed3d693e: 95 '_'  49 '1'  96 '`'  116 't' 96 '`'  32 ' '  62 '>'  32 ' '
0x7fffed3d6946: 48 '0'  4 '\004'        -1 '\377'       -1 '\377'       7 '\a'  0 '\000'        12 '\f' 67 'C'
0x7fffed3d694e: 79 'O'  78 'N'  83 'S'  84 'T'  82 'R'  65 'A'  73 'I'  78 'N'
0x7fffed3d6956: 84 'T'  95 '_'  50 '2'  96 '`'  116 't' 96 '`'  32 ' '  62 '>'
0x7fffed3d695e: 32 ' '  49 '1'  0 '\000'        105 'i' 61 '='  -19 '\355'      -1 '\377'       127 '\177'
0x7fffed3d6966: 0 '\000'        0 '\000'        92 '\\' 8 '\b'
```


-  Duplicate check constraint
```
create table t(t1 int constraint t1_check check(t1>0),
               t2 int check(t2>0),
               t3 int constraint t_field check(t3>0),
               t4 int constraint t_field check(t4>0));
```
```
(gdb) x/10bs buf->ptr()
+x/10bs buf->ptr()
0x7fffed3d696e: "\003"
0x7fffed3d6970: ""
0x7fffed3d6971: "\b"
0x7fffed3d6973: "\at_field`t3` > 0\003\001"
0x7fffed3d6986: "\b"
0x7fffed3d6988: "\at_field`t4` > 0"
0x7fffed3d6999: "\255\247\375\377\017"
0x7fffed3d699f: ""
0x7fffed3d69a0: "\300i=\355\377\177"
0x7fffed3d69a7: ""

```


- For MDEV-30899: Fail to drop CHECK constraint
```
CREATE TABLE t0 (c1 INT CHECK ( c1 > 0 ));
ALTER TABLE t0 DROP CONSTRAINT c1;
```

```
mysql_prepare_alter_table 
>Add new constraints
```



alter_specification:
MODIFY [COLUMN] [IF EXISTS] col_name column_definition
        [FIRST | AFTER col_name]



Test affectin MODIFY specifier
is_columns gcol_column_def_options_innodb gcol_column_def_options_myisam column_compression_parts storage_engine.alter_table jp_comment_column geometry alter_spatial_index innodb-index innodb-index-online-norebuild instant_alter_import innodb_dict alter_candidate_key




--echo #
--echo # MDEV-30899: Fail to drop CHECK constraint
--echo #

CREATE TABLE t0 (c1 INT CHECK ( c1 > 0 ));
show create table t0;
SELECT * from INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE
CONSTRAINT_SCHEMA = 'test';
SELECT * from INFORMATION_SCHEMA.CHECK_CONSTRAINTS WHERE
CONSTRAINT_SCHEMA = 'test';
# Drop field constraint
ALTER TABLE t0 DROP CONSTRAINT c1;

show create table t0;
# To drop column constraint, modify column without constraint
ALTER TABLE t0 MODIFY COLUMN c1 INT;
show create table t0;
# Add constraints, adds table constraints.
ALTER TABLE t0 ADD CONSTRAINT CHECK (c1<0);
show create table t0;
ALTER TABLE t0 ADD CONSTRAINT c1_new CHECK (c1<20);
show create table t0;
ALTER TABLE t0 DROP CONSTRAINT c1_new;
show create table t0;
SELECT * from INFORMATION_SCHEMA.CHECK_CONSTRAINTS WHERE
CONSTRAINT_SCHEMA = 'test';
drop table t0;cleawr



mysql_alter_table (9718 - 10882)
  ->check ALTER_DROP_CHECK_CONSTRAINT (10030)
    > Checks if unique/foreign if name are same and go to continue
  ->mysql_prepare_alter_table (10180)
  ->
