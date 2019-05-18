all: read

read: readline_anel.o
	gcc readline_anel.o -o read -lreadline -g

readline_anel.o: readline_anel.c
	gcc -c readline_anel.c 

#phony(artifical) target doesn't represent a file
clean:
	rm readline_anel.o read
