#include "stdio.h"
#include <unistd.h> //read
#include "fcntl.h" // open, O_RDONLY
#include <ctype.h> // toupper
#include <wait.h> // wait
#include <stdlib.h> //exit
#include <string.h> // strlen()
/*
* Using pipes instead of files/sockets -> files are slow (on disk)
* ./a.out > output.txt or ./a.out 2> error.txt
* connect stdout/stderr of one process to stdin of another process
* named pipes: mkfifo mypip  (p-pipe)
* prw-r--r-- 1 anel anel    0 Feb 11 23:16 mypipe
* test -> ps aux > mypipe (CTRL+Z) -> bg/fg (dump data to pipe, block till someone receive data)
* grep Chrome < mypipe - process receiving the input from pipe
*/

/**
 * To test the function:
 * Create pipe: mypipe, feed data: ps > mypipe (CTLR+Z to stopp)
 * Test bg process: bg => ps>mypipe&
 * ./a.out => should list output of ps
 */
void testProcesses_with1pipe_not_working()
{
  // Have p1 takes string send to p2
  // p2 concatanete and send to p1
  if (fork() == 0)
  {
    int fd= open("mypipe", O_RDWR);
    char *ptr="Anel";
    write(fd, ptr, 4);
    close(fd);
  }
  else
  {
    wait(NULL);
    int fd= open("mypipe", O_RDONLY);
    char *str;
    read(fd, str, 4);
    printf("Got from child: %s", str);
  }
  
}

void speakingProcessess()
{
  // man pipe
  int pipefd[2];
  // pipefd[0]- read end of pipe
  // pipefd[1]- write end of pipe
  // Let's have main -> writing data, child ->reading data
  if (pipe(pipefd)==-1)
  {
    //write(STDOUT_FILENO, "Cannot create a pipe", 20);
    perror("Pipe error");
    exit(EXIT_FAILURE);
  }
  pid_t pid;
  pid= fork();
  if(pid == -1)
  {
    fprintf(stderr, "Error generating PID\n");
    exit(EXIT_FAILURE);
  }
  if (pid == 0)
  {
    close(pipefd[1]); // close write end of pipe, no need
    char buff;
    char *buff1= malloc(100*sizeof(char));
    int i=0;
    while(read(pipefd[0], &buff, 1))
    {
      //write(STDOUT_FILENO, &buff, 1); // works
      buff1[i++]=buff;
    }
    buff1[i]='\0';
    write(STDOUT_FILENO, buff1, strlen(buff1));
    write(STDOUT_FILENO, "\n", 1);
    close(pipefd[0]); // finish reading
    exit(EXIT_SUCCESS);
  }
  else
  {
    char *a= "Anel Husakovic";
    close(pipefd[0]); // close read-end of pipe
    write(pipefd[1], a, strlen(a));
    close(pipefd[1]); // finish writing - must go
    wait(NULL);
    exit(EXIT_SUCCESS);
  }

}
void workWithPipe()
{
  
  int fd= open("mypipe", O_RDONLY);
  char c;

  // read 1 byte from file
  while(read(fd, &c, 1)> 0)
  {
    printf("%c", toupper(c));
  }
  close(fd);
}
int main(int argc, char const *argv[])
{
  //fprintf(stdout, "Hello world\n");
  //fprintf(stderr, "Hi error\n");

  //workWithPipe();
  speakingProcessess();
  return 0;
}
