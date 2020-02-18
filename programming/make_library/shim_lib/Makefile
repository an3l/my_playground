CC= clang
CCLFAGS= -Wall -g
BINS= main shim.so

all: $(BINS)

%.so: %.c
	$(CC) $(CCLFAGS) -fPIC -shared -ldl -o $@ $^

%: %.c
	$(CC) $(CCLFAGS) -o $@ $^

clean:
	rm -f $(BINS)
