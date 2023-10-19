# Create the test in replication suite

1. Need configuration `test.cnf`
2. Need test `test.test`
3.

# 1. Configuration
```plantuml
  package "Dependecies" {
    ' skinparam arrowThickness 4
    ' Test case
    folder "Test case folder" {
        ' Definitions
        [test.cnf] as tcnf
        [test.test] as test

        ' Links
    }

    ' Include for the configuration file
    frame "Test.cnf"{
        ' Definitions
        () "Start test.cnf" as start_testcnf
        [include ./mysql-test/suite/rpl/my.cnf] as mycnf
        [include ./mysql-test/suite/rpl/rpl_1slave_base.cnf] as rpl_slavebase
        [include ./mysql-test/include/default_mysqld.cnf] as default_mysqld #LightGreen
        [Setting up the master/slave\nwith optional override] as rpl_slavebase_implementation #Pink
        [Optionally override \n master/slave/server configuration] as overridecnf #Red
        () "End test.cnf" as end_testcnf
        
        ' Links configuration
          [start_testcnf]..>[mycnf]
          [mycnf]..>[rpl_slavebase]
          [rpl_slavebase]..>[default_mysqld]
          [default_mysqld]..>[rpl_slavebase_implementation]
          [rpl_slavebase_implementation]..>(end_testcnf)
        [mycnf]..[#Red]>overridecnf
        ' hidden link
        ' [rpl_slavebase_implementation]~~>overridecnf

        ' Notes
        note right of default_mysqld
          Defined default groups for the server
          * [mysqld]
          * [embedded]
          * [server]
        end note

        note right of rpl_slavebase_implementation
            Override defaults groups for master/slave servers:
                * [mysqld.1] - master
                * [mysqld.2] - slave
                * [ENV] [MASTER|SLAVE]_[MYPORT|SOCK]
        end note
    }

    ' Include for the test file
    frame "Test.test"{
        () "Start" as start_test
        [include mysql-test/include/master-slave.inc] as ms
        [Queries] as query
        () "End test.test" as end_test

        ' Links test with ms
        [start_test]..>[ms]
        [ms]..>[query]
        [query]..>[end_test]
    }

    frame "Master-slave.cnf"{
        ' Definitions
        () "Start master-slave.cnf" as start_ms
        [include mysql-test/include/rpl_init.inc] as rplinit
        [include mysql-test/include/rpl_connect.inc] as rpl_connect_master
        [include mysql-test/include/rpl_connect.inc] as rpl_connect_slave
        [include mysql-test/include/rpl_connection.inc] as set_default_connection
        () "End master-slave.cnf" as end_ms

        ' Links ms with replication inint
        [start_ms]..>[rplinit]
        [start_ms]-[hidden]d-[rplinit]
        [rplinit].[dashed,#red,thickness=3].>[rpl_connect_master]:<color:red>default ports SERVER_MYPORT_1,2 set in rpl_init
        [rpl_connect_master]..>[rpl_connect_slave]
        [rpl_connect_slave]..>[set_default_connection]
        [set_default_connection]..>(end_ms)

        'Notes
        note top of rplinit
        Set topology 1->2.
        rpl_server_count is not set, but maximum number from topology is used
        as a count.
        end note
        note bottom of rplinit
        For function check `rpl_init` diagram
        end note
        note left of rpl_connect_master
        Dependent on the **rpl_init** that sets the default ports
        to **SERVER_MYPORT_1,2** to **MASTER_MYPORT**,**SLAVE_MYPORT**,
        that are set **rpl_1slave_base**
        Connections:
        * master (server_id=1)
        * master1 (server_id=1)
        end note
        note right of rpl_connect_slave
        Connections:
        * slave (server_id=2)
        * slave1 (server_id=2)
        end note
        note left of set_default_connection
        Set default connection:
        * master (server_id=1)
        end note
    }

 
    ' Links between components
      ' Up from tcnf is configuration .cnf
      ' see deployment diagram
      [tcnf]-[dashed,#red,thickness=3]l->[test]:<color:red>//included//
      [tcnf]-[dashed,#green,thickness=3]->[start_testcnf]:<color:green>//execution//
      [tcnf]-[hidden]u->[end_testcnf]
      ' Left to right from test  is test.test
      [test]-[dashed,#green,thickness=3]->[start_test]:<color:green>//execution//
      [test]-[hidden]d->[start_test]
      ' Below test.test is ms
      [ms]-[dashed,#green,thickness=3]->[start_ms]:<color:green>//execution//
      [ms]-[hidden]r->[start_ms]
      ' Interconnections
      '[start_test]<~~[#MediumBlue]u~[end_testcnf] :<color:blue>Configuration file included into test
      '[start_test]<~~[#MediumBlue]u~[end_ms] :included
      ' left to right
      '[start_test]->[start_ms] 


  }


```

## Tricks plantuml
https://crashedmind.github.io/PlantUMLHitchhikersGuide/layout/layout.html
https://crashedmind.github.io/PlantUMLHitchhikersGuide/color/color.html