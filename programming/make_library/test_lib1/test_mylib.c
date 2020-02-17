#include "stdio.h"
#include "mylib.h"

int main(int argc, char **argv)
{
  if (argc>0)
  {
    printf("  String: %s\n", argv[1]);
    printf("Reversed: %s\n", reverse(argv[1]));
  }  
  return 0;
}
