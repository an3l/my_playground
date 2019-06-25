### Getting started with Mariadb

For getting started see the link [get-code-build-test](https://mariadb.org/get-involved/getting-started-for-developers/get-code-build-test/)

#### Out of tree builds
* Create builds

  Create new directory 
  `
  ../builds/build-mariadb-${version}
  `, which means that the source area isn't polluted with build artefacts and that we can have a different` build-mariadb-$version-mainbranch` there as a comparison of behaviour of the latest upstream without recompiling.
 In source directory run `git clean -dffx`.
  
  * `git worktree`

    Use `git worktree` to have a source directory per major version. This should reduce some of the compiling as you switch between versions. The code is shared. From source (`main working tree`) `./server` use `git worktree add ../mariadb-server-10.1` to create a new `linked working tree`. It is checked out as a new branch (`mariadb-server-10.1`) in this repository without builds.
    
  *Note<sub>1</sub>*: If you delete a branch from linked working tree you will delete it from main working tree.
  
  *Note<sub>2</sub>*: When you run `git remove ../mariadb-server-10.1` still the branch will be visible in main tree ? Delete it with `git branch -d mariadb-server-10.1` after deleting the work tree. 
  
  From build directory (`./builds/build-mariadb-10.1`) run `cmake` to configure the files (as a source directory one can use linked work tree directory (created by `git worktree add`) or main work tree directory):
  
  `cmake ../../mariadb-server-10.1 -DCONC_WITH_{UNITTEST,SSL}=OFF -DWITH_EMBEDDED_SERVER=OFF -DWITH_UNIT_TESTS=OFF -DCMAKE_BUILD_TYPE=Debug -DPLUGIN_{ARCHIVE,TOKUDB,MROONGA,OQGRAPH,ROCKSDB,CONNECT,SPIDER,SPHINX}=NO -DWITH_SAFEMALLOC=OFF -DWITH_SSL=bundled -G Ninja`
  The same goes for other branches, so from your build directories run:
  `cmake ../../mariadb-server-10.2`
  `cmake ../../mariadb-server-10.3`
  `cmake ../../mariadb-server-10.4`
  To build the files, from build directory run `ninja` or `make`.
  
  * Start the server from build directory without use of `~/.my.cnf`
  
    The easiest way is to create alias in `~/.bashrc`:
  
     `alias mariadblocal=
'mkdir /tmp/datadir && scripts/mysql_install_db --no-defaults --srcdir=${OLDPWD} --builddir=${PWD} 
--datadir=/tmp/datadir --log-bin=/tmp/datadir/mysqlbin --verbose; sql/mysqld --no-defaults 
--datadir=/tmp/datadir --lc-messages-dir=${PWD}/sql/share --verbose'`
 Source your file `source ~/.bashrc` and see your aliases `alias`. To remove them use `unaliase <name>` or remote it from `.bashrc`.
  After that navigate to your build directory and make sure to have `$OLDPWD` set either your linkend worktree, or main tree:
    ```bash
    anel@ubuntu:~/workspace/mariadb/builds/build-10.1$ cd ../../mariadb-server-10.1/
    anel@ubuntu:~/workspace/mariadb/mariadb-server-10.1$ cd -
    /home/anel/workspace/mariadb/builds/build-10.1
    ```
    Delete `/tmp/datadir` and run from build directory : `mariadblocal` and server should install system tables and start the server
  
  ### My current remotes and branches
  
  upstreamssh/bb-10.2-anel
  upstreamssh/bb-10.2-anel-MDEV19205
  upstreamssh/bb-10.4-anel-fix-typo
  upstreamssh/bb-anel-10.2-MDEV19679
  upstreamssh/bb-anel-10.3-refactor-store_schema_params



  upstream/bb-10.2-anel-MDEV19205
  upstream/bb-10.3-anel-MDEV18323
  upstream/bb-10.3-anel-check-constraint
  upstream/bb-10.4-anel-fix-typo
  upstream/bb-anel-10.2-MDEV19679
  upstream/bb-anel-10.3-refactor-store_schema_params
  upstream/bb-anel-MDEV-17429
  upstream/bb-anel-check_constraing
  upstream/bb-anel-json-v2
  upstream/bb-anel-json-v2-10.3-recursion
  upstream/bb-anel-json-v2-alter_force-10.3

