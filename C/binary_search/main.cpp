#include <stdio.h> // we can use <cstdlib> instead // http://www.cplusplus.com/reference/cstdlib/
#include <iostream>
#if defined(ALGO_WITH_SQRT)
#include "math.h"
int search_algo(int *a, int n, int val)
{
  int num= sqrt(n);
  for (int i=0; i<n; i+=num)
  {
    if (a[i] == val) return val;
    return -1;
  }
  return -1;
}
#endif
/*
// Complexity is 0(m*n)
int search(int a[], int val)
{
  for (int i=0; i<10; i++)
  {
    printf("a[i]=%d, val=%d \n", a[i], val);
    if (a[i] == val) return val;
  }
  
  return -1;
}
*/
// Binary search // complexity 0(log(n)) - halfing values
int binary_search(int a[], int n, int val)
{
  // We know a is sorted array, and we know dimension
  int start=0, stop=n-1, interval;
  while(start<stop)
  {
    interval=(start+stop)/2;
    printf ("start: %d, stop: %d, Interval: %d, a[i]: %d, val: %d \n",\
              start, stop, interval, a[interval], val);
    
    if(a[interval]<val)
    {
      start= interval+1;
    }
    else
    {
      stop= interval;
    }
    if (a[start] == val) return val;
  }
  return -1;

}
// function shall 
int compareFcn(const void *a,const void *b)
{
  return (*(int *)a - *(int *)b);
}
void use_bsearch(int *a, int val)
{
  // http://www.cplusplus.com/reference/cstdlib/bsearch/
  int *found_item;
  found_item= (int*) bsearch((int *)&val, (int *)a, 10, sizeof(int), compareFcn);
  if (found_item != NULL)
    printf("Found %d\n", *found_item);
  else
    printf("Item not found!\n");
  

}
int main()
{
  // array a - from which we are looking values has to be sorted
  int a[10]={20, 30, 31, 42, 55, 77, 88, 90, 93, 112};
  // array b - values we are looking for 
  int b[3]={20, 88, 112};
  int val;
  for (auto i=0; i<3; i++)
  {
    // val= search(a, b[i]);
    val= binary_search(a, 10, b[i]);
    if(val == -1) printf("Not Found! \n");
    else printf("Found %d\n", b[i]);
    #if defined(ALGO_WITH_SQRT)
    printf("Imamo algo! \n");
    #endif

    printf("\nTest built-in bsearch() in cstdlib: \n"); // works
    use_bsearch(a, b[i]);
  }

  // Let's test element of unsorted array
  int x[10]={10, 8, 9, 1, 2, 3, 5, 4, 7, 6};
  printf("\nTest unsorted array of bsearch(): \n");
  qsort(x, 10, sizeof(int), compareFcn);
  use_bsearch(x, 9);
  // use bsearch()
  return 0;
}

