CC=clang
CCFLAGS= -Wall -g
BINS= bufferoverrun
all: $(BINS)

%.out: %.c
	$(CC) $(CCFLAGS) $@ $^

clean:
	rm -f $(BINS)
