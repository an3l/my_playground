#include <iostream>
#include <string.h>


int main(int argc, char const *argv[], char **envir)
{
  /* code */
  while(*envir)
  {
    if(strncmp(*envir, "MYSQL_PWD",9) == 0)
    {
      std::cout<<*envir<<std::endl;
      char *p;
      if(p=strchr(*envir, '='))
      {
        size_t len1= p-*envir+1;
        size_t len2=strlen(*envir) - len1;
        std::cout<<p+1<<"\nLength of MYSQL_PWD=: "<<len1\
        <<"\nLength to be overwritten: "<<len2<<std::endl;
        char *t=strstr(*envir, p+1);
        memset(t, 'x', len2);
        std::cout<<*envir<<std::endl;
      }
    }
    *envir++;
  }
  return 0;
}
