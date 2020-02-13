#include <stdio.h>
#include <stdlib.h>
// For system calls:
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h> //read
#include <sys/mman.h> //mmap
#include <ctype.h>
//#include <fstab.h> //fstab
/*
* File I/O
* fopen() vs open()
*/
void fileio1()
{
  // Pointer handle to FILE struct
  FILE *fr= fopen("my_text_read.txt", "a+");
  FILE *fw= fopen("my_text_write.txt", "w");
  // f can be handled with funcs: fopen, fread,fwrite,fprintf,fscanf,feof, fclose
  if (fr == NULL || fw == NULL)
  {
    fprintf(stderr, "Cannot open fr, fw \n");
    exit(EXIT_FAILURE);
  }
  // change . to !
  char c;
  while ((c=fgetc(fr)) != EOF)
  {
    if(c=='.')
      c='!';
    fputc(c, fw);
  }

  fclose(fr);
  fclose(fw);
}

/**
 * system call open() - posix compliant os
 * instead of mode string ("r") we have mode flags
 * O_cREATE, O_RDONLY,...
 * returns file descriptor (int) as a track of open files 
 * using I/O system calls read/write instead of fgetc, fputc
 * Test: clang sharedmem_mmap.c && ./a.out && time ./a.out 
 * Conclusion: using systemcall is slower than using library call (fopen)
 * Reason: buffering I/O of fopen
 * 1 byte at a time -> lot of context swithches, producing a lot of system calls of kernel
 * in open(). fopen() may wait and push all characters to disk(read/write larger chunks better)
 * For devices -> buffering not desirable.
 * https://www.youtube.com/watch?v=BQJBe4IbsvQ
 */
void fileio2()
{
  int fd_read= open("my_text_read.txt", O_RDONLY);
  int fd_write= open("my_text_write.txt", O_WRONLY);
  if (fd_read == -1 || fd_write == -1)
  {
    perror("Cannot read file!\n");
    exit(EXIT_FAILURE);
  }
  ssize_t num_bytes;
  char c;
  while((num_bytes= read(fd_read, &c, sizeof(c))) > 0)
  {
    if(c == '.')
     c='?';
    write(fd_write, &c, sizeof(c));
  }
  close(fd_read);
  close(fd_write);
}

/**
 * mmap -> processes using memory from os.
 * virtual memory: lack of ram
 * memory manager takes some ram and copies it to swap space on hdd
 * use mmap to request block of memory and to be filled with data from file
 * https://www.youtube.com/watch?v=m7E9piHcfr4
 */

/**
 * stat somefile.txt
 * stat(filename, struct stat *), fstat(fd,...)
 * https://www.youtube.com/watch?v=FT2A2HQbTkU
 * For using fopen() => fseek, ftell ?
 * When having fopen(), which returns File * and to use fstat with fd
 * we will use int fd= fileno(File *)
 */

void readFileFromMem()
{
  // use open with flags (access modes) and 
  // mode (user has read/write permissions S_IRUSR-stat.h)
  int fd= open("my_text_read.txt",O_RDONLY, S_IRUSR|S_IWUSR);
  struct stat fs; //get file status man 2 stat
  if (fstat(fd, &fs) == -1)
  {
    perror("Get file statusf fstat failed!\n");
    exit(EXIT_SUCCESS);
  }
  write(STDOUT_FILENO, "File size %ld", fs.st_size);

  char *file_in_memory= mmap(NULL, fs.st_size, PROT_READ, MAP_PRIVATE, fd, 0); // 0 is offset for the file

  for (int i=0; i<fs.st_size; i++)
  {
    printf("%c", file_in_memory[i]);
  }
  printf("\n");
  munmap(file_in_memory, fs.st_size);
  close(fd);
}

void writeFileFromMem()
{
  // use open with flags (access modes) and 
  // mode (user has read/write permissions S_IRUSR-stat.h)
  int fd= open("my_text_read.txt",O_RDWR, S_IRUSR|S_IWUSR);
  struct stat fs; //get file status man 2 stat
  if (fstat(fd, &fs) == -1)
  {
    perror("Get file statusf fstat failed!\n");
    exit(EXIT_SUCCESS);
  }
  write(STDOUT_FILENO, "File size %ld", fs.st_size);

  // MAP_SHARED -> changes done in memory without this wouldn't be changed to file on disk
  char *file_in_memory= mmap(NULL, fs.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0); // 0 is offset for the file

  for (int i=0; i<fs.st_size; i++)
  {
    if (i%3 == 0)
      file_in_memory[i]=toupper(file_in_memory[i]);
    printf("%c", file_in_memory[i]);
  }
  printf("\n");

  munmap(file_in_memory, fs.st_size);
  close(fd);
}
void sharedMem()
{
  //readFileFromMem();
  writeFileFromMem();
}


/**
 * ltrace, strace
 * https://www.youtube.com/watch?v=2AmP7Pse4U0
 */

int main(int argc, char const *argv[])
{
  //fileio1();
  //fileio2();
  sharedMem();
  return 0;
}
