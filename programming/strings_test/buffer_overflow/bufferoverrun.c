#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFERSIZE 10

/**
 * Buffer overflow using `strcpy()`
 * ./bufferoverrun  password message
 * Usings strings utility we can inspect chars and test them as password
 * Looking into assembler code: objdump -s
 * Symbol table; objdump -t
 * 0000000000601052 g     O .data	000000000000000a              pass
 * 0000000000601048 g     O .data	000000000000000a              buffer
 * Difference in addresses is A(10) bytes
 * So going above of 10 bytes will override password:
 * ./bufferoverrun anel 1234567890anel
 */
 
char buffer[BUFFERSIZE]= "message";
char pass[BUFFERSIZE]= "password";
void reverseStrings(char *str)
{
  int N= strlen(str); // without 0 char
  printf("%d\n", N);
  char *strnew= malloc(N*sizeof(char)+1);
  /*
  for (int i=0; i<N; i++)
  {
    strnew[N-i-1]=str[i];
    printf("i: %d--%c %c\n",i, str[i], str[N-i]);
  }
  */
  for(int i=0; i<N/2; i++)
  {
    strnew[i]= str[N-i-1];
    strnew[N-i-1]=str[i];
  }
  strnew[N+1]=0;
  printf("Str: %s, reverse: %s \n", str, strnew);
}
int main(int argc, char const *argv[])
{
  reverseStrings(pass);

  if (argc  < 3)
  {
    fprintf(stderr, "usage: %s <pass> <sstring to print> \n", argv[0]);
    exit(EXIT_FAILURE);
  }

  strcpy(buffer, argv[2]); // argv[1] is not controlled
  if (strcmp(argv[1], pass) == 0)
  {
    fprintf(stdout, "password checks out!\nMSG: %s\n", buffer);
  }
  else
  {
    fprintf(stderr, "password error !\n");
  }


  
  return 0;
}
