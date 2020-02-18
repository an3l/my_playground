#include <stdio.h>
#include "stdlib.h" 

/**
 * Shim piece of code between program and library that use it.
 * Intercept calls
 * https://www.youtube.com/watch?v=5HuM_eVjFJo
 * 
 * rand() is in libc:
 * our program is linking to libc in runtime and making a call 
 * of rand(), and libc is giving back random number
 * 
 * Nice links:
 * https://www.win.tue.nl/~aeb/linux/lk/lk-3.html
 * Linux kernel:
 * https://www.win.tue.nl/~aeb/linux/lk/lk.html
 */

int main(int argc, char const *argv[])
{
  for (int i=0; i<5; i++)
  {
    printf("%d: %d\n", i, rand());
  }
  return 0;
}
