#define _GNU_SOURCE
#include "stdio.h"
#include <sys/stat.h>
#include "wait.h"
#include <unistd.h> //read
#include <sys/mman.h>
#include <stdint.h>

#define PAGESIZE 4096
int v= 5;
/*
https://www.youtube.com/watch?v=rPV6b8BUwxM&list=PL9IEJIKnBJjFNNfpY6fHjVzAwtgRYjhPw&index=8

Calling conventions and registers?
*/

int main(int argc, char const *argv[])
{
  /*But if we don't want to use pipes, files, or  we can use shared memory mmap()*/
  // If fd=-1 (no file in memory), we have to use anonymous
  uint8_t *shared_memory= mmap(NULL, PAGESIZE, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);
  // set 1.byte (val 0 - 255) of block
  *shared_memory= 34;
  // Child and parent have different memory
  if (fork() == 0)
  {
    v=10;
    *shared_memory= 100;
    // %i == %d auto detect the base
    printf("Val child: %d \nVal child shared: %i\n", v, *shared_memory);
  }
  else
  {
    wait(NULL);
    printf("Val parent: %d \nVal parent shared: %i\n", v, *shared_memory);
  }
   printf("End Val: %d \nVal shared: %i\n", v, *shared_memory);
  return 0;
}
