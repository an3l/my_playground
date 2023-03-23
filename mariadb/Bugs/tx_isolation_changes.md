## What should be done
1. JIRA and commit message should be updated with information about the link https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-20.html where additional variable transaction_read_only is also used @nikita can you please update specification.
Also update transaction_isolation as command line option along with configuration option in JIRA.

Also please link our KB in description 
https://mariadb.com/kb/en/server-system-variables/#tx_isolation
https://mariadb.com/kb/en/server-system-variables/#tx_read_only
Documentation doesn't say about current behavior of option tx_isolation/transaction_isolation but should say
and also about new changes that will be merged.
Additional update https://mariadb.com/kb/en/set-transaction/

2. Please squash commits and write `MDEV-21921:` instead of `[MDEV-21921]`

3. There is no test file with configuration for both variables, please add.


Usage of IS.variables

thd->tx_isolation? sql/sys_var.incl do we need - no we don't.
