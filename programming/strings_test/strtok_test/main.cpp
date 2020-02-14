#include "stdio.h"
#include "string.h" //strtok

/**
 * Usage of trtok (tokenize)
 * Destructive for original string, inserting 0 bytes
 * thread unsafe, strtok_r
 */
void smallTest()
{
  /* not working
  In C: type is array of char
  In C++: type is constant array of char (not allowed to change the chars of strings, what strtok is doing)
  Using const_cast still not work
  char *c= const_cast<char *>("anel: husakovic, melisa: husakovic, hey");
  */
  
  char c1[100]= "anel: husakovic, melisa: husakovic, hey";
  char *original_str= c1;
  const char *del= ":";
  printf("Before tok [\\0 not inserted in place of delimiter]\n: %s\n", c1);
  char *tok= strtok(c1, del);
  printf("Original pointer is also changed: %s\n,Working string: %s\nTokenize: %s\n", original_str, c1, tok);
  
}

/**
 * Test2
 */
void testStrtok()
{
  char c1[100]= "anel: husakovic, melisa: husakovic, hey";
  char *tok;
  char *tmp= c1;
  int num=0; 
  printf("Original string: %s\n", c1);
  while((tok= strtok(tmp, ":")) != NULL)
  {
    printf("-- Token|%s|; Num of token: %d --\n", tok, num++);
    tmp= NULL; // because after 1. strtok, delimiter will be changed with NULL
  }
  printf("String: %s\nTokenize: %s\n", c1, tok);

}
int main(int argc, char const *argv[])
{
  testStrtok();
  return 0;
}
