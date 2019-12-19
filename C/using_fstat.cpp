#include <iostream>
//#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define handle_error(msg)\
        do { perror(msg); exit(EXIT_FAILURE); } while(0)

int main(int argc, char *argv[])
{
  std::cout<<"There were: "<<argc<<" number of parameters\n";
  for (int i=0; i<argc; i++)
  {
    std::cout<<"argv["<<i<<"]: "<<argv[i]<<std::endl;
  }
  // Expecting input -> file -> argv[1]
  if(argc !=2)
  {
    fprintf(stderr, "%s file has to have 2 parameters", argv[0]);
    exit(EXIT_FAILURE);
  }
  
  int fd;
  // https://www.ibm.com/developerworks/community/blogs/58e72888-6340-46ac-b488-d31aa4058e9c/entry/understanding_linux_open_system_call?lang=en
  // defined in 
  if ((fd = open(argv[1], O_RDONLY)) == -1)
    handle_error("open\n");
  
  struct stat stat_buff;
  
  if(fstat(fd,&stat_buff) < 0)
    handle_error("cannot get the file status!\n");
 
  printf("Information for %s\n",argv[1]);
  printf("---------------------------\n");
  printf("File Size: \t\t%d bytes\n",stat_buff.st_size);
  printf("Number of Links: \t%d\n",stat_buff.st_nlink);
  printf("File inode: \t\t%d\n",stat_buff.st_ino);

  printf("File Permissions: \t");
  printf( (S_ISDIR(stat_buff.st_mode)) ? "d" : "-");
  printf( (stat_buff.st_mode & S_IRUSR) ? "r" : "-");
  printf( (stat_buff.st_mode & S_IWUSR) ? "w" : "-");
  printf( (stat_buff.st_mode & S_IXUSR) ? "x" : "-");
  printf( (stat_buff.st_mode & S_IRGRP) ? "r" : "-");
  printf( (stat_buff.st_mode & S_IWGRP) ? "w" : "-");
  printf( (stat_buff.st_mode & S_IXGRP) ? "x" : "-");
  printf( (stat_buff.st_mode & S_IROTH) ? "r" : "-");
  printf( (stat_buff.st_mode & S_IWOTH) ? "w" : "-");
  printf( (stat_buff.st_mode & S_IXOTH) ? "x" : "-");
  printf("\n\n");

  printf("The file %s a symbolic link\n\n", (S_ISLNK(stat_buff.st_mode)) ? "is" : "is not");

  return 0;
}