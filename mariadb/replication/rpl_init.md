```plantuml

   frame "rpl_init"{
      folder "Parameters"{
        [rpl_server_count] as rpl_server_count
        [rpl_topology] as topology
        [rpl_check_server_ids] as rpl_check_server_ids #pink
        [rpl_skip_reset_master_and_slave] as rpl_skip_reset_master_and_slave
        [rpl_skip_change_master] as rpl_skip_change_master
        [rpl_skip_start_slave] as rpl_skip_start_slave
        [rpl_debug] as rpl_debug
        [slave_timeout] as slave_timeout
      }
    ' Definitions
    () "Start rpl_init" as start
    () "End rpl_init" as end
    () "rpl_init initiated" as initiated
    [assign_ports] as assign_ports
    [check server count] as server_count
    [create connections] as two_connections
    [reset master/slave] as reset_ms
    [check server id] as check_ids #OrangeRed
    [create rpl_master_list] as master_list
    [include mysql-test/include/rpl_change_topology.inc] as change_toplogy
    [include mysql-test/include/rpl_start_slaves.inc] as start_slaves
    [set connection] as set_connection
    [include mysql-test/include/rpl_connection.inc] as rpl_connection
 
    ' Notes
    note left of assign_ports
    Check for:
    * SERVER_MYPORT_1/2 (assign MASTER_MYPORT/SLAVE_MYPORT)
    * SERVER_MYPORT_2
    end note

    note right of server_count
    Based on `rpl_topology` get greatest number
    end note

    note left of two_connections
    Each server (1 and 2) will have following connections
    * `server_1`
    * `server_11` (not needed)
    * `server_2`
    * `server_21` (not needed)
    end note

    note left of set_connection
    Connection name to be set is `server_1` (is this master?)
    end note

    ' Links
    [start]-->[assign_ports]
    [assign_ports]-->[server_count]
    [server_count]-->[two_connections]
    [two_connections]-->[reset_ms]:if not set `rpl_skip_reset_master_and_slave`
    [reset_ms]->[initiated]:rpl initiated
'    [two_connections].->[two_connections]:iterate
    [reset_ms]-[dashed,#red,thickness=3]->[check_ids]:<color:red>all host have different IDs - bug
    [reset_ms]---->[master_list]
    [master_list]-->[change_toplogy]
    [change_toplogy]-->[start_slaves]:if not rpl_skip_start_slave
    [start_slaves]-->[set_connection]
    [set_connection]->[rpl_connection]
    [rpl_connection]-->[end]
    }

    frame "rpl_start_slaves.inc"{
    ' Definitions
    () "Start rpl_start_slaves" as _start_slave
    () "End slave" as end_slave
    [For each slave mysql-test/include/rpl_for_each_slave.inc] as foreach_slave #pink
    [Start slave mysql-test/include/start_slave.inc] as start_slave
    [_start_slave]-->[foreach_slave]:arguments are rpl_source_file
    [foreach_slave]-[dashed,#red,thickness=3]->[start_slave]:source slave file\n<color:red> start slave
    [start_slave]-->[foreach_slave]:next slave
    [foreach_slave]--->[end_slave]
    }

    folder "Parameters for rpl_for_each_slave"{
        [rpl_server_count_length ~~missing~~ obtained in rpl_change_topology] as rpl_server_count_length #pink
        [rpl_server_count ~~missing~~ obtained in rpl_init] as rpl_server_count_ #pink
        [rpl_master_list ~~missing~~ obtained in rpl_init] as rpl_master_list #pink
    }

    frame "start_slave.inc"{
      () "Start start_slave" as _start_single_slave
      () "End start_slave" as end_single_slave
      [START SLAVE] as query_start_slave
      [include mysql-test/include/wait_for_slave_to_start.inc] as wait_slave_to_start

      ' Links
      [_start_single_slave]-->[query_start_slave]
      [query_start_slave]-->[wait_slave_to_start]
      [wait_slave_to_start]-->[end_single_slave]
    }

    frame "wait_for_slave_to_start.inc"{
      () "Start wait_for_slave_to_start" as wait_slave_start
      () "End wait_for_slave_to_start" as wait_slave_end
      [include mysql-test/include/wait_for_slave_io_to_start.inc] as wait_io_to_start
      [include mysql-test/include/wait_for_slave_sql_to_start.inc] as wait_sql_to_start

      ' Links
      [wait_slave_start]-->[wait_io_to_start]
      [wait_io_to_start]-->[wait_sql_to_start]
      [wait_sql_to_start]-->[wait_slave_end]
    }


    frame "wait_for_slave_io_to_start.inc"{
        folder "IO slave start arguments"{
            ' same as rpl_init
            [slave_timeout] as arg_io_timeout #pink 
            [rpl_allow_error] as arg_rpl_allow_error
        }
      ' Definitions
      () "Start wait_for_slave_io_to_start" as start_io_wait_slave
      () "End wait_for_slave_io_to_start" as end_io_wait_slave
      [Set slave_param to Slave_IO_Running=Yes] as set_slave_io_param 
      [include mysql-test/include/wait_for_slave_param.inc] as call_wait_io_for_slave_param

      ' Links
      [start_io_wait_slave]-->[set_slave_io_param]
      [set_slave_io_param]-->[call_wait_io_for_slave_param]
      [call_wait_io_for_slave_param]..>[set_slave_io_param]:set slave_error_param to null
      [set_slave_io_param]...>[arg_rpl_allow_error]:set rpl_allow_error to 0
      [arg_rpl_allow_error]-->[end_io_wait_slave]

      note bottom of arg_io_timeout
      This value is set by rpl_init.inc
      end note
    }

    frame "wait_for_slave_sql_to_start.inc"{
        folder "SQL slave start arguments"{
            ' same as rpl_init
            [slave_timeout] as arg_sql_timeout #pink 
            [rpl_allow_error] as arg_rpl_allow_error_sql #blue
        }
      ' Definitions
      () "Start wait_for_slave_sql_to_start" as start_sql_wait_slave
      () "End wait_for_slave_sql_to_start" as end_sql_wait_slave
      [Set slave_param to Slave_SQL_Running=Yes] as set_slave_param_sql
      [include mysql-test/include/wait_for_slave_param.inc] as call_wait_sql_for_slave_param

      ' Links
      [start_sql_wait_slave]-->[set_slave_param_sql]
      [set_slave_param_sql]-->[call_wait_sql_for_slave_param]
      ' [call_wait_for_slave_param]..>[set_slave_param_sql]:set slave_error_param to null
      ' [set_slave_io_param]...>[arg_rpl_allow_error]:set rpl_allow_error to 0
      [call_wait_sql_for_slave_param]-->[end_sql_wait_slave]

      note bottom of arg_rpl_allow_error_sql
      Slave SQL thread sets //Slave_SQL_Running=Yes// **before** it clears
      //Last_SQL_Errno//, so errors are allowed and this parameter doesn't exist
      end note

      note bottom of set_slave_param_sql
      * There is no set to //slave_error_param// null as in IO thread
      end note
    }

    frame "wait_for_slave_param.inc"{
        folder "Wait for slave param arguments"{
            [slave_error_param] as slave_error_param
            [slave_timeout] as arg_io_timeout #pink 
            [slave_param] as slave_param
            [slave_param_value] as slave_param_value
            [slave_param_comparison] as slave_param_value
        }
        ' Definitions
        () "Start wait_for_slave_param" as start_wait_slave_param
        () "End wait_for_slave_param" as end_io_wait_slave_param
        [Check timeout and set if empty] as check_parameters
        [Check if slave_io_running=1 from show slave status] as slave_io_already_running
        [Slave io not running - exit] as slave_io_not_running
        [Check slave param in 10xtimeout] as check_slave_param_10x
        ' Links
        [start_wait_slave_param]-->[check_parameters]
        [check_parameters]-->[slave_io_already_running]
        [slave_io_already_running]..>slave_io_not_running
        [slave_io_already_running]....>check_slave_param_10x
        check_slave_param_10x-->end_io_wait_slave_param
        ' Notes
        note left of check_parameters
            * Set timeout to 300 if empty
            * Set slave_error_param to 1 if empty
            * Set slave_param_comparison to = if empty
        end note

        note right of check_slave_param_10x
            * Check if there is the custom row in *show slave status*
            * If yes, abort, condition reached
            * Decrease counter each 0.1[s]
        end note
    }
    ' frame "wait_sql_to_start.inc"{
    '   () "Start wait_sql_to_start" as start_sql_wait_slave
    '   () "End wait_sql_to_start" as end_sql_wait_slave
    '   [include mysql-test/include/wait_for_slave_io_to_start.inc] as wait_io_to_start
    '   [include mysql-test/include/wait_for_slave_sql_to_start.inc] as wait_sql_to_start

    '   ' Links
    '   [wait_slave_start]-->[wait_io_to_start]
    '   [wait_io_to_start]-->[wait_sql_to_start]
    '   [wait_sql_to_start]-->[wait_slave_end]
    ' }

    ' Links
    [end]-[hidden]d->[_start_slave]
    [start_slaves]-[dashed,#green,thickness=3]->[_start_slave]:<color:green>//execution//
    [end_slave]-[dashed,#red,thickness=3,hidden]->[rpl_server_count_length]
    [foreach_slave]-[dashed,#pink,thickness=3]->[rpl_server_count_length]:<color:red>//missing paramaters//
    [_start_single_slave]<-[dashed,#blue,thickness=3]l-[start_slave]:<color:green>//execution//
    [wait_slave_to_start]-[dashed,#green,thickness=3]d->[wait_slave_start]:<color:green>//execution//
    [end_single_slave]-[hidden]d->[wait_slave_start]
    
    ' Wait IO
    [wait_io_to_start]-[dashed,#green,thickness=3]r->[start_io_wait_slave]:<color:green>//execution//
    [call_wait_io_for_slave_param]-[dashed,#green,thickness=3]->[start_wait_slave_param]:<color:green>//execution//

    ' Wait SQL 
     [wait_sql_to_start]-[dashed,#green,thickness=3]l->[start_sql_wait_slave]:<color:green>//execution//
     [call_wait_sql_for_slave_param]-[dashed,#green,thickness=3]->[start_wait_slave_param]:<color:green>//execution//

     ' Link slave_param to caller
     [wait_slave_end]-[hidden]d->[start_wait_slave_param]
```
