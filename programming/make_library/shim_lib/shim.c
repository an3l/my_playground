/**
 * Our implementation of rand() instead of libc
 * 
 * To invoke it: LD_PRELOAD=./shim.so ./main 
 */
#define _GNU_SOURCE // has to be enabled to use RTLD_NEXT handle
#include <dlfcn.h>

int rand()
{
  /*
    Using original rand() using dlsym() with handle RTLD_NEXT
    There is a RTLD_DEFAULT also 
    See usage of dladdr()
  */
  int (*my_rand)()= dlsym(RTLD_NEXT, "rand");
  return my_rand() % 100;
}
