#include "stdio.h"
#include <string.h>

/**
 * - use bless hex editor (hexed.it) based on hexdump -C <name> (offset, hex, data asci)
 * - compile with -g flag
 * - strings ./a.out
 * - readelf --sym ./a.out -> getting symbol table
 * - objdump -t a.out (.text is a **section** name where code goes)
 * - objdump -s a.out (all section requested -binary exe)
 *   + .rodata - static strings, readonly
 * - objdump -d a.out -> disassemble (start section calling main)
 * - readelf --segments a.out -> segments block of memory, section(logical subpieces)
 * - strip a.out - > removing debug information (-g), smaller binary
 */
int myglob= 1;

int main(int argc, char const *argv[])
{
  if (argc<=1) return 1;
  if (strcmp(argv[1], "FEEDBEEF") == 0)
  {
    printf("Good password \n");
    return 0;
  }
  {
    printf("Wrong password \n");
    return 1;
  }

  return 0;
}
