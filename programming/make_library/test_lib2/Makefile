CC= clang
CCFLAGS= -Wall -g -ldl
CCSHARED= -fPIC -shared
BINS= libfunc1.so libfunc2.so main.out

all: $(BINS)

#libfunc1.so: libfun1.c
#	$(CC) $(CCFLAGS) $(CCSHARED) -o $@ $^

#libfunc2.so: libfunc2.c
#	$(CC) $(CCFLAGS) $(CCSHARED) -o $@ $^

%.so: %.c
	$(CC) $(CCFLAGS) $(CCSHARED) -o $@ $^

# Left is main.c
%.out: %.c
	$(CC) $(CCFLAGS) -o $@ $^

clean:
	rm $(BINS)
	rm *.so
