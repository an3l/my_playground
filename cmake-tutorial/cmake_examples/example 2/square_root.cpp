// Literature: https://cmake.org/cmake-tutorial/

// A simple program that computes the square root of a number
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <math.h>
#ifdef USE_MYMATH
#include "MathFunctions.h"
#endif
#include "TutorialConfig.h"
 
int main (int argc, char *argv[])
{
  if (argc < 2)
    {
    fprintf(stdout,"%s Version %d.%d\n",
            argv[0],
            Tutorial_VERSION_MAJOR,
            Tutorial_VERSION_MINOR);
	const char *source_dir1="@PROJECT_SOURCE_DIR@";
	printf("Source dir: %s \nBinary dir: %s\nProject version: %s\n",
	        PROJECT_SOURCE_DIR, PROJECT_BINARY_DIR, PROJECT_VERSION);
    fprintf(stdout,"Usage: %s number\n",argv[0]);
	
    return 1;
    }
  double inputValue = atof(argv[1]);
  #ifdef USE_MYMATH
  double outputValue = mysqrt(inputValue);
  #else
  double outputValue = sqrt(inputValue);
  #endif
  fprintf(stdout,"The square root of %g is %g\n",
          inputValue, outputValue);
  return 0;
}