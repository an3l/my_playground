#include "stdlib.h"
#include "string.h"
//#include "stdio.h"
/**
 * Reverse the string 
 */
char *reverse(char *source)
{
  int len= strlen(source);
  //printf("Len: %d", len);
  char temp;
  //char* result= (char*) malloc(len*sizeof(char));
  for (int i=0; i<len/2; i++)
  {
    temp= source[i];
    //printf("S:%c,%c", source[i], source[len-i-1]);
    source[i]= source[len - i-1];
    source[len - i-1]= temp;
    //printf("R: %c, %c\n", source[i], source[len-i-1]);
  }
  return source;
}
