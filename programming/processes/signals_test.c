#define _XOPEN_SOURCE // sigaction

#include <stdio.h>
#include "unistd.h" // STDOUT_FILENO
#include "signal.h"

void handler(int num)
{
  // Functions in handler should be synch safe
  // signal handlers are running async
  
  write(STDOUT_FILENO, "\nNo break!\n",13); // 13 or STDINT
}

void segsegv(int num)
{
  write(STDOUT_FILENO, "\nSigSegv !\n", 20);
}

void testSignals();
void testSigactions();

int main(int argc, char const *argv[])
{
  //testSignals();
  testSigactions();
  return 0;
}

/*
* Newer preferred way to handle signals
*/
void testSigactions()
{
  struct sigaction sa; // defined with _XOPEN_SOURCE
  sa.sa_handler= handler;


  sigaction(SIGINT, &sa, NULL); // num_signal, new_act, old_act (NULL)
  sigaction(SIGTERM, &sa, NULL);
  while(1)
  {
    printf("No need to stop: %d \n", getpid());
    sleep(1);
  }
}

/*
* Classical way of handling signals
*/
void testSignals()
{
  // Register signal
  // SIGINT -> ctr+c
  // SIGTERM -> kill -TERM pid 
  // (not same as ctrl+d (kill -9 (-KILL)))
  // SIGKILL is an order not request, not working with handler
  // -STOP, -CONT, SIGUSR1,SIGUSER2 (user defined for communication)
  signal(SIGINT, handler);
  signal(SIGTERM, handler);
  signal(SIGSEGV, segsegv);
  int *p=0;
  *p= 10; // simulate sigfault, but with handler we can catch that also

  while(1)
  {
    printf("No need to stop: %d \n", getpid());
    sleep(1);
  }
}
