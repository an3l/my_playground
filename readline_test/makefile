all: read
	echo Finished!
# $@ -> target, $< -> first dependent
read: readline_anel.o
	gcc $< -o $@ -lreadline -g

readline_anel.o: readline_anel.c
	gcc -c $< 

#phony(artifical) target doesn't represent a file
clean:
	rm readline_anel.o read
