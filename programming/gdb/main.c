#include "stdint.h"
#include "stdio.h"
#include "assert.h"
#include "stdlib.h"

#pragma pack(1) // don't introduce the padding
typedef struct
{
  int8_t h; // 1 byte
  int16_t seconds; //2 bytes
  int32_t micros; // 4 bytes

} anel_time;

/* Assertions ssert.h
// Can be removed:
// To exclude from release build: gcc -DNDEBUG main.c
// How to use them: https://ptolemy.berkeley.edu/~johnr/tutorials/assertions.html
// https://en.wikipedia.org/wiki/Assert.h
*/
void testAssertion(int *s)
{
  assert(s != NULL); // if false print error
}
/* segfault - access memmory (r/w)
core dumped
design - code - debug in cycles
Test driven development - test before the code
sizeof() is a operator
size of pointer - 64bits -8 bytes
*/
void trackSegFault()
{
  int *p= NULL;
  *p= 12; 
}

void testHeapCOrruption()
{
  char p;
  char str[10];
  printf("Test1: ");
  gets(str);
  printf("Str: %s\n", str);
  printf("Test2: \n");
  // Never use gets - buffer overflow error
  // can be returned by compiler at any time
  // Safer fgets(str, 10, stdin) or scanf()
  gets(p);
  printf("Str: %c\n", p);
  /*
  char *buff=malloc(1); // allocate only 1 byte
  *buff= "12345678"; // store value > 256
  */
}


/*
  Condition in gdb:
    b main.c:72 if (i > 10)
*/
void testConditionGDB(const char *file)
{
  char *buff= malloc(10*sizeof(char));
  FILE *f= fopen(file, "r");
  assert(f != NULL);
  char c;
  uint8_t i=0;
  while((c= fgetc(f)) != EOF)
  {
    printf("%c", c);
    buff[i++]=c;
  }
  fclose(f);
  //printf("Buff: %s", buff);
  free(buff);
}


/*
  Debug fork() and exec()
  Gdb can follow just one process at the time (parent, child)
    set follow-fork-mode child # or parent
  Exec is replacing the current process
    set follow-exec-mode new # or same
*/
void debugFork()
{

}


/*
  strace - system trace: process request from OS,man syscalls
  ltrace - library trace:process calls from existing library 
*/

int main(int argc, char const *argv[])
{
  anel_time t={.h=1, .seconds= 0x123, .micros= 0x12345};
  printf("size of time: %lu\n", sizeof(t));

  // Assertions
  //testAssertion(NULL);
  //trackSegFault();
  //testHeapCOrruption(); // buffer overflow with gets
  //testConditionGDB(argv[1]);

  return 0;
}
