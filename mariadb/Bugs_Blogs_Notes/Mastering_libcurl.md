# Mastering curl 
- Daniel Stenberg
- Learn more about curl API
  - mastering libcurl 1 and 2 (november 2023)  < current_learning
    https://www.youtube.com/watch?v=ZQXv5v9xocU
    https://www.youtube.com/watch?v=9KqnXsSxqGA
  - Libcurl under the hood
    https://www.youtube.com/watch?v=T7Pv5lQ1dAc
    
- Generic
  - https://www.youtube.com/watch?v=V5vZWHP-RqU 
- 8.4.0
  - https://www.youtube.com/watch?v=-j-_nKmq2aE
  - https://www.youtube.com/watch?v=xZpyXA9_7qg



##  Part 1
- **GITHUB**
  - https://github.com/bagder/mastering-libcurl

- About project
httpget (1996) -> urlget(1997) -> curl (1998) -> 
libcurl(2000) (client URL or see URL)
  - same tarball - both CLI tool and library
    - curl - cli tool for client-side 
    - libcurl - library for client-side internet transfers (upload/download/both) with URLs (endpoint)
- https://curl.se/libcurl/
- Mailinglist curl-library (lists.haxx.se/mailman/listinfo/)
  - Or discussions in GitHub
- 101 OS, lot of features

- Install libcurl development package
  - libcurl4-openssl-dev # or libcurl4-gnutls-dev
  - Or build it
    - Configure/cmake (./configure --with-openssl && make -sj && make install)
    - MSVC (name /f Makefile.vc mode=dll WITH_SSL=dll)

- Third party libraries are needed by many features:
  - TLS, SSH, LDAP, RTMP, HTTP compression (gzip, brotli, zstd), HTTP/2,HTTP/3, Async name resolving without threads, Auth-kerberos, SASL
- Target requirements
  - smallets TLS 100kB minimal curl build
  - smallest run-time memory requirement for libcurl: 20kB
  
- API & ABI
  - Compatiblity
    - same api on all platforms
    - always upgrade to the next version without breakage
    - cannot downgrade
    - optinos and functinos are documented
    - Release 2000 - libcurl 7.1(2000) - Last 8.4.0 (2023))
- Header: curl/curl.h
- Compile: gcc mycode.c -lcurl (library is in the system default directory)
- Documentation: https://everything.curl.dev/
- Architecture
  - C89
  - a) curl <-> b) public API (90 functions) <-> c) application
  - a) curl consists of backends that c) doesn't know:
    - content encoding (zlib, brotli, zstd) - compressions
    - resolver - resolve hostname into IP (solutions: sync, threaded, c-ares resolvers) 
    - IDN - international domain names (libidn2, winidn)
    - SSH - libssh, libssh2, wolfssh (sftp, ssftp)
    - TLS - (imaps, pop3s, https) - 12 backends 
    - HTTP - built-in (http2, nghttp2) or hyper
    - HTTP/3 - quiche, msh3, nghttp3
- non-blocking
  - Eveything is non-blocking (with small exceptions)
  - parallel name resolves
  - parallel connection establishments at same time
  - parallel TLS handshakes
  - parallel transfers
  - with different latencies and bandwidths
  - in a single thread
- API fundamentals
  - 1. Opaque handlers - we need functions to use handlers
  - 2. URLS - we need url
  - 3. callbacks focus - data provided via callbacks or actions are callback based

- libcurl does "Basic transfer by default"
  - it is doing bare minimum
  - enable all bells if you need
  - API is protocol agnostic
  - From basic change behavior by setting options
  
- **global init**
  - We should do in application **curl_global_init (CURL_GLOBAL_DEFAULT)**
    - In past it was needed more. It might work without, but is encouraged to use it.
  - And a global cleanup **curl_global_cleanup()**
 
- **easy handle**
  - We want transfer; `CURL *handle` - easy handle (interaface) - opaque hanlde
    - Compare to FILE *
    - Should be reused as handle - second transfer faster
    - **curl_easy_init()**
    - **curl_easy_cleanup()**
- **easy options**
  - Easy handle needs options set to know what to do for transfer
    - Options are:
      - sticky - when set, they will there set
      - independent 
      - order-independent
      - Options set copy data when setting strings  - when we set url it will copy data in its own memory
      - **CURLOPT_URL** - only mandatory option - endpoint
      - If not set other option, it will try to **download** URL
    - Options controls lot of things
      - timeouts, name resolve alternatives, connectivity, protocol version selection, TLS, authenticatoin, proxies, how to receive data.
    - Sets option with **curl_easy_setopt (handle, option, parameter)**
      - Parameter type depends on the option
      - `varargs` - compiler doesn't check 3.option type and doesn't tell you if you are right, crashes in runtime
      - Might want extra typecasts
      - Return error code
      - `CURLOPT_VERBOSE,` - only in xbcloud.cc
- **curl_easy_perform**
  - Transfer is performed using easy handle for sync transfers 
    - **blocking call** - do entire transfer and then return 
      - Performs to the end, either fails, or success
       - You can set timeout, but is done as fast as possible
       - You can limit how long time to allow to spend
    - everything internally is non-blocking
    - It may be file is big or server is slow - may be hours
    - Stores cached info in the easy handle 
      - stores metadata
    - This will by default put on stdout
    - For every chunk of data curl can receive it will call the callback
      - We don't know how many time it might be called
      - Don't assume the size returned we can get small/big chunks (there is maximum size)
      - If repeat the transfer, it might appear with different sizes
        - Depends on network conditions , conditions on server size, local connections, machine conditions

- **curl_easy_cleanup()**
  - Kills and frees all resources associated with easy handle
  - **curl_easy_reset()** clear all settings to factory default and set new options
    - allows caching to survive
- **callbacks**
  - provide function pointer to curl (*FUNC)
  - all callback options end with `_function`
  - provide custom pointer to pass to function (*data)
  - **write callback**
    - When curl gets data, it wants to store it and calls the write callback, write it somewhere
    - `CURLOPT_WRITEFUNCTION` it has protopye - based on `fwrite`
      - `ptr` - points to data that arrives
      - `size` - always 1 (can be ignored)
      - `nmemb` - size of data in number of bytes (total is nmemb*size)
      - `userdata` - pointer we set with `CURLOPT_WRITEDATA`
      
- **multi handle**
  - Many transfer at the same time
  - "super handle"  for holding one or more easy handles (that is a single transfer)
  - All transfers are performed in parallel - in a non-blocking manner
  - Can be added/removed from the multi handle at any time
  - **CURLM *handle= curl_multi_init()** < it is in `./extra/mariabackup/xbcloud.cc` and `./libmariadb/plugins/io/remote_io.`
  - **curl_multi_add_handle()**
 
 - **caches**
   - Store data to make it faster for next time
   - Associated with `curl_easy_perform` - caches in the easy handle
   - DNS cache, 
   - connection pool - keeps connections alive
   - TLS sesssion-ID cache - fastest TLS handshake in subsequent connection to the same host again
   - CA store cache - no need to reparse it
   - cookies, Alt-svc data, HSTS data - per single handle in multi handles
- **curl_multi_socket_action**
  - variation of multi interface
  - event based API flavor - trigger events based on changes of socket
  - Above 100 transfers  scales better
  - Uses event libraries and interface with them - I have this socket and want to do something 

- Verbose
  - CURLOPT_ERRORBUFFER - more detailed information about error (char curl_errbuf[CURL_ERROR_SIZE];). check buff and if not **curl_easy_strerror(res)**
  - CURLOPT_VERBOSE  - may be 
  - CURLOPT_DEBUGFUNCTION - instead to send to stderr
  - curl_global_trace
  - CURLINFO_XFER_ID - what transfer is happening curl_easy_getinfo
  - CURLINFO_CONN_ID - curl_easy_getinfo 
  - curl_version() - pointer
  
- Connecting
  - resolve name
  - happy eyeballs - connection IPV4 and IPV6 at same time picking the first
  - Select IPv4
- Persistent connections
  - repeated transfers
  - client <-> example.com (con1), when transfer completed will store connection in connection pool if still alive (someone removed them)
  - client <-> curle.se (con2) - stores that too in connection pool
  - client <-> example.com (con3) -  con1 in the pool - reused
  - CURLOPT_MAXCONNECTS - N connections
  - kept up to a maximum age: CURLOPT_MAXAGE_CONN - 180 (2 mins)
  - reuse is done per name, not per IP - skips resolving part
  - works for all supported protocols
  - CURLOPT_FRESH_CONNECT - opt-out reuse - this new transfer don't try to reuse old connectoin
  - CURLOPT_FORBID_REUSE - make next transfer not reusable, close it afterwards.
  - CURLOPT_TCP_KEEPALIVE - TCP keepalive - ping-pong
- Connections: name tricks
  - Pre-populate DNS cache :CURLOPT_RESOLVE - provide name to IP address lookup
    - **curl_slist_append()** is used
    - When we have lab and we don't want to connect  but redirect
  - Host + port "redirect" : CURLOPT_CONNECT_TO
    - Experimental thing
    - Maybe we get certificate error `CURLOPT_SSL_VERIFYHOST`
  - 
  
- **Connections: network interface**
  - `CURLOPT_INTERFACE` - if we want our traffic to go to specific network interface
  - 
##  Part 2


  members of RESTDEF:
  curl_inited = true,
  Tdp = 0x0,
  Http = 0x7fffd4014a20 "http://jsonplaceholder.typicode.com/users",
  Uri = 0x0,
  Fn = 0x7fffd4014a08 "users.json"
}

  members of RESTDEF:
  curl_inited = true,
  Tdp = 0x0,
  Http = 0x7fffd4014a20 "http://jsonplaceholder.typicode.com/users",
  Uri = 0x0,
  Fn = 0x7fffeae762a0 "/dev/shm/var_auto_O7Pg/mysqld.1/data/test/users.json"
}


    

  
