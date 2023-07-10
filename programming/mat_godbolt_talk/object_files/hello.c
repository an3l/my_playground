#include "stdio.h"

extern const char *getMessage();
void greet()
{
  printf("%s\n", getMessage());
}
int main()
{
  greet();
}

