
#include "stdio.h"
#include <stdlib.h> 
#include <sys/types.h> 
#include <unistd.h> 
#include "wait.h" // wait() <sys/wait.h>

/*
 https://www.geeksforgeeks.org/zombie-and-orphan-processes-in-c/
 https://www.geeksforgeeks.org/zombie-processes-prevention/
 A C program to demonstrate Zombie Process.  
 Child becomes Zombie as parent is sleeping 
 when child process exits. 
*/
void createZombie()
{
  // Fork returns process id 
  // in parent process 
  pid_t child_pid = fork(); 

  // Parent process
  if (child_pid > 0)
      sleep(1); 

  // Child process 
  else        
      exit(0); 
}


/*
// A C program to demonstrate Orphan Process.  
// Parent process finishes execution while the 
// child process is running. The child process 
// becomes orphan. 
*/
void createOrphan()
{
    // Create a child process       
  int pid = fork(); 

  if (pid > 0) 
      printf("in parent process pid %d", getpid()); 

  // Note that pid is 0 in child process 
  // and negative if fork() fails 
  else if (pid == 0) 
  { 
      sleep(2); 
      printf("in child process %d", getpid()); 
  } 
}

/*
 not exist in process table
 with "wait/waitpid" from parent, child process is reaped
 OS is free to remove process from process list
   anel      24671  0.0  0.0   4512   820 pts/1    S+   20:44   0:00 ./a.out
   anel      24672  0.0  0.0      0     0 pts/1    Z+   20:44   0:00 [a.out] <defunct>
  
*/
void testZombies()
{
  if(fork() == 0)
  {
    printf("child\n");
  }
  else
  {
    // wait that process finishes (wait.h)
    wait(NULL);
    printf("Parent; \n");
    sleep(5);
  }
  
}
int main()
{ 
  //createOrphan();
  testZombies();

  return 0; 
} 
