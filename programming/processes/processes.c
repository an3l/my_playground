#include "stdio.h"
#include "unistd.h" // posix api: fork, getpid, pipe, sleep
/**
 * Process is not the same as program.
 * Program may have multiple processes.
 */
#define MAX_BYTES 256
void childProcess()
{
    // Child process, cloning the process-> fork()
    // Identical copies of address space of parent and child
    char buff[MAX_BYTES];
  if(fork()==0)
  {
    printf("Hello world from child: %d\n", getpid());
  }
  else
  {
    for(int i=0; i<100; i++)
    {
      
      sprintf(buff, "This is from pid: %d, value %d \n", getpid(), i); // sprintf(str, format, args)
      // use write() instead of printf() to have unbuffered result ? when we don't know which process it belgongs to ?
      write(1, buff, strlen(buff));
    }

    printf("Hello world: %d\n", getpid());
  }
}

/**
 * execvp - execute new program on top of current process
 * run the program specified and replaces current process
 * execvp - v-vector, p -path(will look into PATH env variable)
 * execlpe - l-list, e- different set of ENV variables to new program.
 * argument list needs to be null terminated, to say there is no args.
 */
void execProcess()
{ 
  if(fork()==0)
  {
    printf("Hello world from child: %d\n", getpid());
    execl("/bin/ls","-la", "/home/anel", NULL);
    //execlp("ls","-la", "/home/anel", NULL);
    printf("This will never be called");
  }
  else
  {
    printf("Hello world: %d\n", getpid());
  }
}

/**
 * https://www.geeksforgeeks.org/fork-system-call/
 * http://www.csl.mtu.edu/cs4411.ck/www/NOTES/process/fork/create.html 
 */
void call_n_processes()
{
  printf("N-procesese \n");
  fork();
  fork();
  fork();
  printf("%d\n",getpid());
}

/*
* Different states and data are prevented for different processess
*/
void forkstates()
{
  int x=1;
  int a=0;
  if(fork() == 0) /*child process*/
  {
    printf("Child: --x = %d , address: %p\n", --x, &x);
    a= a + 5;
    printf("a: %d, &a: %p \n", a, &a);
  }
  else
  {
    printf("Parent: ++x = %d , address: %p\n", ++x, &x);
    a= a - 5;
    printf("a: %d, &a: %p \n", a, &a);
  }
}

/**
 *  
 */
void testForked()
{
  fork();
  fork() && fork() || fork(); // binary tree from link in example
  fork();

  printf("forked\n");
}
int main(int argc, char const *argv[])
{
  childProcess();
  //execProcess();
  //call_n_processes();
  //forkstates(); // virtual addresses are same ?! but physical addresses are different
  //testForked();
  return 0;
}
