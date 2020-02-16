CC= gcc
CCFLAGS=-Wall -g
CCshared= -shared -fPIC
BINS= test
all: test
# do it with %.o: %.cpp

#Make sure that .a, .so have libprefix
main.o: main.c
	$(CC) $(CCFLAGS) -c $<

test: main.o
	$(CC) $(CCFLAGS) -o  $@ $<

clean:
	rm *.o *.so $(BINS)
