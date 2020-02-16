#include "stdio.h"
#include "stdlib.h"
#include "string.h"
/**
 * strcpy(dest, src) copying string with null terminated
 * strncpy(dest, src, n) without '\0' it will copy n with no null termination
 */

/**
 * #pragma pack(1) // disable compiler padding of struct packaging
 * packaginig to 1 byte (without padding)
 * if something is not good with memcpy(dest, src, num_of_elements)?!
 */
typedef struct node
{
  unsigned int val: 1;
  unsigned int size: 10;
  struct node *next;
}node_t;

void testMemcpy()
{
  node_t n1={.val=2, .size=3, .next=NULL};
  // node_t n2=n1;// copy values with assignments->ok
  // creating an object -> ok
  node_t n2;
  memcpy(&n2, &n1, sizeof(node_t));
  printf("n2= %d, %d, %p\n", n2.val, n2.size, n2.next);

  // creating an pointre -> ok
  node_t *n3= malloc(sizeof(node_t));
  memcpy(n3, &n1, sizeof(node_t));
  printf("n3= %d, %d, %p\n", n3->val, n3->size, n3->next);
  free(n3);

  node_t *n4= malloc(sizeof(node_t));
  // char[]
  char buffer[100];
  memset(buffer, 0xFC, 100);
  memcpy(buffer+10, &n1, sizeof(node_t));
  //n4=(node_t *)(buffer+10);
  printf("Char n3= %d, %d, %p\n", n4->val, n4->size, n4->next);
  free(n3);
 
}

void testMe(const char *src)
{
  char *dest= malloc(100*sizeof(char));
  strcpy(dest, src);
  memcpy(dest, "xY", 2);
  printf("Dest: %s, src: %s\n", dest, src);
}

int main(int argc, char const *argv[])
{
  //const char *src= "Anel Husakovic!";
  //testMe(src);
  testMemcpy();
  return 0;
}
