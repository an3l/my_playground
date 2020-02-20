#include "stdio.h"
 #include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "unistd.h"
#include "errno.h"
#include "string.h"


int main(int argc, char const *argv[])
{
  /*Usage check*/
  if(argc < 2)
  {
    printf("Usage: %s <filename>\n", argv[0]);
    return 1;
  }
  int fd= open(argv[1], O_RDONLY);
  if (fd == -1)
  {
    // errno -> global variable
    // maybe better to specify macros for handling the errors (for open, read)
    fprintf(stdout, "Error num: %d\nError: %s\n", errno, strerror(errno)); //strerror string.h
    return 1;
  }
  char c;
  while (read(fd, &c, 1) > 0)
  {
    //fputc(c,stdout);
    fprintf(stdout, "%c", c);
  }
  close(fd);

  return 0;
}
