CC= clang
CCFLAGS= -Wall -g
CSHARED= -fPIC -shared
# Create bins for all rule
BINS= libstatic.a libmylib.so librarytest runtime_test test_static

all: $(BINS)
# Run binary
all_old: librarytest

####### Library rules  #######

# Generate object code \
$@ = mycode.o, $^ = dependencies, $< first dependency (mylib.c)\
Here will be generated: mylib.h.gch, mylib.o\
Rule has to be called <mylib>[.o] not other name
mylib.o: mylib.c mylib.h
	$(CC) $(CCFLAGS) -c mylib.c

# Creating shared library-> link with libc (-lc)\
has to be called with lib prefix <lib>mylib.so
libmylib.so: mylib.c mylib.h
	$(CC) $(CCFLAGS) $(CSHARED) -o $@ $< -lc

# Create static library\
r-replace, create, index?
libstatic.a: mylib.o
	ar rcs $@ $<


####### Executable rules  #######
librarytest:test_mylib.c mylib.o
	$(CC) $(CCFLAGS) -o $@ $^

# This rule is compiled with shared lib\
Not object files, just tell compiler -L to look for library in this directory\
https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html#Link-Options
runtime_test:test_mylib.c
	$(CC) $(CCFLAGS) -o $@ $^ -L. -lmylib

#Test static libstatic.a
test_static: test_mylib.c
	$(CC) $(CCFLAGS) -o $@ $^ -L. -lstatic

####### Cleaning  #######
clean:
	rm *.o $(BINS)
# If *.so doesn't exist create it
clean_old:
	rm *.o *.so librarytest


####### Notes  #######
#1. libmycode.so instead of mycode -> name matters
#2. Not working after compiling, workaround:\
$ LD_LIBRARY_PATH="/home/anel/my_playground/programming/processes/make_library/;LD_LIBRARY_PATH" ./runtime_test "Anela"

#3. Search for ld paths and copy libmycode.so there (worked for /usr/lib (to copy), but not for other paths):\
$ ld --verbose | grep SEARCH_DIR| tr -s ' ;' \\012 \
SEARCH_DIR("=/usr/local/lib/x86_64-linux-gnu") \
SEARCH_DIR("=/lib/x86_64-linux-gnu")\
SEARCH_DIR("=/usr/lib/x86_64-linux-gnu")\
SEARCH_DIR("=/usr/lib/x86_64-linux-gnu64")\
SEARCH_DIR("=/usr/local/lib64")\
SEARCH_DIR("=/lib64")\
SEARCH_DIR("=/usr/lib64")\
SEARCH_DIR("=/usr/local/lib")\
SEARCH_DIR("=/lib")\
SEARCH_DIR("=/usr/lib")\
SEARCH_DIR("=/usr/x86_64-linux-gnu/lib64")\
SEARCH_DIR("=/usr/x86_64-linux-gnu/lib"\

# Shared library -> reverse function is undefined section and 0 addresses
# objdump -t librarytest | grep reverse \
0000000000400590 g     F .text	0000000000000099              reverse \
$ objdump -t runtime_test | grep reverse\
0000000000000000       F *UND*	0000000000000000              reverse\

