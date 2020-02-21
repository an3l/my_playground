#define _GNU_SOURCE // MAP_ANONYMOUS

#include "stdio.h" // NULL
#include "stdlib.h" //malloc
#include <unistd.h> //brk(), sbrk()
#include <stdint.h> // u_int8_t
#include <sys/mman.h>

/*
  Memory layout:
  - top: stack -> grow bellow
  - empty space
  - libraries
  - empty space
  - heap (grows up), globals, code
  - Top of heap -> program break (bringer of seg fault)
  - PB can be expanded/shrinked -> brk(*addrs)
*/
void testMemory();
void testPB();
void test_mmap();

int main(int argc, char const *argv[])
{
  // testMemory(); // strace ./a.out
  //testPB();
  test_mmap();
  return 0;
}

void test_mmap()
{
  const int PAGE_SIZE= 4096;
  // last parameters -> for memory mapped files
  // 1byte vs 4 byte(int)
  int* first= mmap(NULL, PAGE_SIZE, PROT_READ|PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  // blocks of memory are always going to be alligned to begging of page
  // here will be feedb000 (last 12 bits is 0)
  uint8_t* second= mmap((void*) 0xFEEDBEEF, PAGE_SIZE, PROT_READ|PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

  printf("First: %p \n", first);
  printf("Second: %p \n", second);
  int temp=0;
  for (int i=0; i<PAGE_SIZE/sizeof(first); i++)
  {
    first[i]=i;
    printf("%d_temp(%d)", first[i], temp);
    temp++;
  }
  printf("\nSizeof uint8_t: %ld\nSizeof int: %ld\n", sizeof(uint8_t),sizeof(int));
  printf("Size of memory page: %ld\nSize of physical memory: %ld\n", sysconf(_SC_PAGE_SIZE), sysconf(_SC_PHYS_PAGES));
}


void testPB()
{
  printf("Memory page size: %ld\n", sysconf (_SC_PAGESIZE));
  // current location of program break
  void *pb= sbrk(0);
  // Allocate memory and return the previous PB
  // Move up for 1 page (4k)
  void *add1= sbrk(4096);
  int *ptr= (int *)add1;
  ptr[0]=10; ptr[1]=12;
  printf("PB current: %p, After allocation: %p, value: %d\n",pb, add1, ptr[1]);
  //printf("%p - %d\n%p - %d\n", pb, *((int*)pb), add1, *((int *)add1)); // segfault derefence
  pb= sbrk(0); 
  // we shouldn't use memory outside PB: int *ptr= (int *) (pb + 1);
  printf("Changed PB for 4k\n"); // hex: 1000
  printf("PB current: %p, After allocation: %p\n",add1, pb);
}


void testMemory()
{
  for (int i=0; i<5; i++)
  {
    char *ptr= malloc(5*1024*1024);
    printf("Got memory! Address = %p, %x\n", ptr, *ptr);
  }
}
/*

char *ptr= malloc(50000); => brk()
brk(NULL)                               = 0x1a2a000
brk(0x1a4b000)                          = 0x1a4b000
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 1), ...}) = 0
write(1, "Got memory! Address = 0x1a2a260,"..., 35Got memory! Address = 0x1a2a260, 0
) = 35
write(1, "Got memory! Address = 0x1a369d0,"..., 35Got memory! Address = 0x1a369d0, 0
) = 35
brk(0x1a70000)                          = 0x1a70000
write(1, "Got memory! Address = 0x1a42d30,"..., 35Got memory! Address = 0x1a42d30, 0
) = 35
write(1, "Got memory! Address = 0x1a4f090,"..., 35Got memory! Address = 0x1a4f090, 0
) = 35
write(1, "Got memory! Address = 0x1a5b3f0,"..., 35Got memory! Address = 0x1a5b3f0, 0
) = 35

For 5MB => mmap
char *ptr= malloc(5*12024*1024);
brk(NULL)                               = 0x239b000
brk(0x23bc000)                          = 0x23bc000
mmap(NULL, 5246976, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f97eb548000
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 1), ...}) = 0
write(1, "Got memory! Address = 0x7f97eb54"..., 40Got memory! Address = 0x7f97eb548010, 0
) = 40
mmap(NULL, 5246976, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f97eb047000
write(1, "Got memory! Address = 0x7f97eb04"..., 40Got memory! Address = 0x7f97eb047010, 0
) = 40
mmap(NULL, 5246976, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f97eab46000
write(1, "Got memory! Address = 0x7f97eab4"..., 40Got memory! Address = 0x7f97eab46010, 0
) = 40
mmap(NULL, 5246976, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f97ea645000
write(1, "Got memory! Address = 0x7f97ea64"..., 40Got memory! Address = 0x7f97ea645010, 0
) = 40
mmap(NULL, 5246976, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f97ea144000
write(1, "Got memory! Address = 0x7f97ea14"..., 40Got memory! Address = 0x7f97ea144010, 0
) = 40
exit_group(0)
*/
