#include <iostream>

struct Foo
{
  static int cnt;
  Foo() {cnt++;}
  ~Foo() {--cnt;}
};

int Foo::cnt; // defining static variable

Foo global;

int main()
{
  std::cout<<"Number of foos = "<<Foo::cnt<<" \n";
}

