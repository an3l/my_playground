#include "stdio.h"

// Stack overflow
// ulimit -n
int count=0;

void foo()
{
  char data[1024*1024];
  printf("%d\n", count++);
  foo();
}
int main()
{
  foo();
  return 0;
}
