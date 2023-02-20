(gdb) info b
+info b
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x00005555561febf0 in MYSQLtoPLG(char*, char*) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/myutil.cpp:36
2       breakpoint     keep y   0x00005555561ff1a6 in MYSQLtoPLG(int, char*) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/myutil.cpp:180
3       breakpoint     keep y   0x00005555561ff3a7 in MyDateFmt(int) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/myutil.cpp:272
4       breakpoint     keep y   0x00005555561fefa8 in PLGtoMYSQL(int, bool, char) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/myutil.cpp:110
5       breakpoint     keep y   0x00005555561ff09a in PLGtoMYSQLtype(int, bool, char) at /home/anel/GitHub/mariadb/server/src/10.3/storage/connect/myutil.cpp:157


b MYSQLtoPLG(char*, char*) 
b MYSQLtoPLG(int, char*) 
b MyDateFmt(int) 
b PLGtoMYSQL(int, bool, char) 
b PLGtoMYSQLtype(int, bool, char)
