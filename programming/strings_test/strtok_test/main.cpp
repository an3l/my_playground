#include "stdio.h"
#include "string.h" //strtok

/**
 * Test 1
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
  But using `strdup(const char*)` will work! testStrtok2()
  */
  
  char c1[100]= "anel: husakovic, melisa: husakovic, hey";
  char *original_str= c1;
  const char *del= ":";
  printf("Before tok [\\0 not inserted in place of delimiter]\n: %s\n", c1);
  char *tok= strtok(c1, del);
  printf("Original pointer is also changed: %s\n,Working string: %s\nTokenize: %s\n", original_str, c1, tok);
  
}

/**
 * Test 2
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

/**
 * Test 3
 * char*=strdup(const char*)
 * Not handling empty tokens
 */
void testStrtok2()
{
  char *original, *token;
  original= strdup("Anel, Husakovic,,,Melisa, Husakovic!");
  token= strtok(original, ",");
  int num=1;
  while(token!=NULL)
  {
    printf("-- Token|%s|; Num of token: %d --\n", token, num++);
    // Cumbersome 2. call of strtok
    token= strtok(NULL, ",");
  }
}

/**
 * Strtok() is using static variables for original string and is thread unsafe
 * Using: strtok_r(), strsep (ansi compliant - portable), not handling emtpy token
 * strtok_r is using 3.arg as a pointer to rest of string
 * Different handling of empty delimiter
 * strsep() may not be portable, but is handling empty token as null.
 */
void testThreadSafe()
{
  char *original, *original2, *token, *save_ptr;
  original= strdup("Anel, Husakovic,,,Melisa, Husakovic!");
  save_ptr= original;
  int num=1;
  printf("Using strtok_r: \n");
  while((token= strtok_r(save_ptr, ",", &save_ptr))!=NULL)
  {
    printf("-- Token|%s|; Num of token: %d --\n", token, num++);
  }

  original2= strdup("Anel, Husakovic,,,Melisa, Husakovic!");
  printf("Using strsep: \n");
  num=1;
  while((token= strsep(&original2, ","))!=NULL)
  {
    printf("-- Token|%s|; Num of token: %d --\n", token, num++);
  }
  
}

int main(int argc, char const *argv[])
{
  //testStrtok2();
  testThreadSafe();
  return 0;
}
