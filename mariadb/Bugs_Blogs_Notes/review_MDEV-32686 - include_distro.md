# MDEV-32686 crash information to include Distro information

  https://jira.mariadb.org/browse/MDEV-32686
  
  https://github.com/MariaDB/server/pull/2818


From https://github.com/which-distro/os-release 
"rolling-based" distro -> only 1 file
 
 
# Code review
1. open >=3  and handle error for opening the file - like unknown release

2. should check that `close()` is correct
```
if (close(fd) < 0)
{
  error.
}
```

3. `ssize_t` either you should check the error (-1)

4. no need to cast `size_t` for `len` ?
```
 void *memchr(const void *s, int c, size_t n);
```

5. writing differently
```
  len_orig= read(fd, buff, sizeof(buff));
  len= len_orig;
  for (size_t num_lines= 0; num_lines <= 2 & len>0; num_lines++, endline++)
  {
    if (num_lines == 0)
      endline= (char *) memchr(buff, '\n', len_orig);
    else
      endline= (char *) memchr(endline, '\n', len_orig);
    len= endline - buff;
  }
```
No- No check if `memchr` failed - not needed if buff is populated!, but that we don't know


# Commit message review
Maybe to rephrase and put on the beginning?
Its reasonable to support non-Windows filesystems could support
the path /etc/os-release.


"variable" 
To support Apple/FreeBSD kernel information its 'len' variables was
renamed to avoid conflicts and the shared 'buff' is used.

Relates to:
https://jira.mariadb.org/browse/MDEV-30613

Writing function
open()

- Adding implicit conversion

# Additional
1. [s]size_t
	- https://jameshfisher.com/2017/02/22/ssize_t/
	- `size_t` - size of allocated block in memory (max  - `SIZE_MAX`)
	- `ssize_t` - signed `size_t` (-1 - retuned by system calls for erros like `read(), write()`). 
	- `off_t` ? format `jd`
	- `lu` or `zu` format specifier for size_t
	- `zd` for ssize_t
2. read/write
  https://www.geeksforgeeks.org/input-output-system-calls-c-create-open-close-read-write/
3. void * and char*
	Casting to (char *) (not needed for this case, in general it is not allowed)
	```
	ssize_t read(int fd, void *buf, size_t count);

	```
	- since read() works on char values (bytes) 
	https://cplusplus.com/forum/general/284304/
	- see this
	https://stackoverflow.com/questions/48684711/why-read-in-c-needs-a-pointer-to-char
	```
	- the best type representing a byte was char or unsigned char. 
		Here you are reading serialized data into your structure instance,
		you are not reading characters, so char in this context means byte not character.
	- Since char also represents a character, 
		there is no implicit conversion from "all pointers" to char* ,
		while there is an implicit conversion from "all pointers" to void*,
		because void* represents a generic pointer and nothing else, thus it is much safer to allow.
	```
	- Because of implicit conversion
	https://en.cppreference.com/w/cpp/language/implicit_conversion
	https://www.quora.com/Can-we-use-char-instead-of-void-for-a-generic-pointer-in-C

4. memchr (string.h)
  https://en.cppreference.com/w/c/string/byte/memchr
	https://www.tutorialspoint.com/c_standard_library/c_function_memchr.htm

