#include "stdio.h"
#include "stdlib.h"
#include <string.h> //memset
#include <unistd.h> //write, STDOUT

#define ONEkB 1<<10
#define ONEMB 1<<20
#define ONEGB 1<<30


/**
 * Allocated mem: 131069 GB 
 * Malloc refuesd afer: 131070 GB
 * If not used memory, OS will lie that it allocated enough
 */
void testLie()
{
  int count= 0;
  while (1)
  {
    if(malloc(ONEGB) == NULL)
    {
      printf("Malloc refuesd afer: %d GB \n", count++);
      exit(EXIT_FAILURE);
    }
    printf("Allocated mem: %d GB \n", count++);
  }
}


/**
 * We have to use malloc and memset()
 * Allocated mem: 14 GB 
 * Malloc refused afer: 15 GB 
 */
void useMalloc()
{
  int count= 0;
  
  while (1)
  {
    int *p = (int *) malloc(ONEGB);
    if(p == NULL)
    {
      printf("Malloc refuesd afer: %d GB \n", count++);
      exit(EXIT_FAILURE);
    }
    memset(p,1, ONEGB);
    printf("Allocated mem: %d GB \n", count++);
  }
}

/**
 * Try to allocate N blocks of ONEGB
 * Wrote to 13 Gb
 * Killed
 * Sneaky things will not work
 */
void allocateBlocks()
{
  int N= 100;
  char *blocks[N];
  for(int i=0; i<N; i++)
  {
    blocks[i]= (char *) malloc(ONEGB);
    if (blocks[i] == NULL)
    {
      perror("Cannot allocate \n");
      exit(EXIT_FAILURE);
    }
  }

  printf("Allocated: \n");
  for (int i=0; i<N; i++)
  {
    memset(blocks[i], 1, ONEGB); // write into buf
    printf("Wrote to %d Gb\n", i);
  }
}


int main(int argc, char const *argv[])
{
  // testLie();
  //useMalloc();
  allocateBlocks();
  return 0;
}
