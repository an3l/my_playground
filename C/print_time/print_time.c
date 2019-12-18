#include <stdio.h>
#include "time.h"

void print_time()
{
  time_t now;
  
  time(&now); //  same as time_t next; next= time(NULL);
  // time_t *t; time_t next= time(t); // segmentation fault
  printf("Today is: %s", ctime(&now));
}