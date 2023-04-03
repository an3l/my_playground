


# Used by anonymous user
processlist_anonymous processlist_reg_user set_default_role_invalid init_connect grant2 enforce_storage_engine lock_multi 

# Used by delete_anonymous user ^^^ above + below
rpl_temporary

./mysql-test/include/grant_cache.inc



--echo # Test of anonymous user connection
--echo --------------------------------------------------------------
--source include/add_anonymous_users.inc
connect(con1,localhost,'',,test);
SELECT CURRENT_ROLE;
SET role test_role;
SELECT CURRENT_ROLE;
# user cannot set subset role, since it is not granted explicitly
--error ER_INVALID_ROLE
SET role new_role;
--error ER_PASSWORD_ANONYMOUS_USER
set default role test_role for ''@localhost;
