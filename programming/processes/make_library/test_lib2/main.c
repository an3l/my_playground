#include <dlfcn.h>
#include <limits.h>
#include <stdlib.h> //atoi, realpath
#include "stdio.h" //perror

/**
 * Test realpath(char *path, char *resolvedPath)
 * How to load shared library
 * https://www.youtube.com/watch?v=_kIa4D7kQ8I
 */
void getPath(const char *arg)
{
  char *full_path= realpath(arg, NULL);
  printf("ABS PATH: %s \n", full_path);
}
int main(int argc, char const *argv[])
{
  //.test libname1.c int
  if (argc<3)
    return 1;


  const char *librarypath= argv[1];
  int num= atoi(argv[2]);
  /**
   * Open the library 
   * The  function  dlopen()  loads  the dynamic shared object (shared library)
       file named by the null-terminated string filename and  returns  an  opaque
       "handle"  for the loaded object.
  * lazy binding-> when needed 
   */
  void *my_handle;
  // It is expecting full path for library or to be specified via
  // LD_LIBRARY_PATH or to use -rpath (full path or relative -Wl,-rpath=$ORIGIN/../lib/)
  //my_handle= dlopen("/home/anel/my_playground/programming/processes/make_library/test_lib2/libfunc1.so", RTLD_LAZY);
  // Alternativly test realpath()
  //printf("Temp path: %s \n", argv[1]);
  //getPath(argv[1]);
  char *full_libpath= realpath(librarypath, NULL); // should be freeed (tested in valgrind)
  my_handle= dlopen(full_libpath, RTLD_LAZY);
  free(full_libpath);
  if (my_handle == NULL)
    perror("Cannot open library\n");
  
  dlerror(); // delete any error

  /**
   * Function pointer to library
   */
  int (*opfun)(int);
  char *(*opfun_name)();

  /**
   * Obtain address of a symbol of shared object
   */

  opfun= dlsym(my_handle, "do_operation");
  opfun_name= dlsym(my_handle, "libname");

  /**
   * Check for the errors
   */
  char *error;
  error= dlerror();
  if (error != NULL)
  {
    fprintf(stderr, "%s\n", error);
    exit(EXIT_FAILURE);
  }

  // Apply the function
  printf("Function: %s \nNum: %d ---> do_operation: %d\n", opfun_name(), num, opfun(num));

  /**
   * Close the library
   */
  dlclose(my_handle);
  exit(EXIT_SUCCESS);

  return 0;
}
