#include "stdio.h"
#include "stdlib.h"
#include <readline/readline.h>
#include <readline/history.h>
/* A static variable for holding the line. */
static char *line_read = (char *)NULL;

/* Read a string, and return a pointer to it.
   Returns NULL on EOF. */
char *
rl_gets ()
{
  /* If the buffer has already been allocated,
     return the memory to the free pool. */
  if (line_read)
    {
      free (line_read);
      line_read = (char *)NULL;
    }

  /* Get a line from the user. */
  line_read = readline ("anel2> ");

  /* If the line has any text in it,
     save it on the history. */
  if (line_read && *line_read)
    add_history (line_read);

  return (line_read);
}


  
/* Invert the case of the COUNT following characters. */
int
invert_case_line (count, key)
     int count, key;
{
  register int start, end, i, direction;

  start = rl_point;

  if (rl_point >= rl_end)
    return (0);

  if (count < 0)
    {
      direction = -1;
      count = -count;
    }
  else
    direction = 1;
      
  /* Find the end of the range to modify. */
  end = start + (count * direction);

  /* Force it to be within range. */
  if (end > rl_end)
    end = rl_end;
  else if (end < 0)
    end = 0;

  if (start == end)
    return (0);

  if (start > end)
    {
      int temp = start;
      start = end;
      end = temp;
    }

  /* Tell readline that we are modifying the line,
     so it will save the undo information. */
  rl_modifying (start, end);

  for (i = start; i != end; i++)
    {
      if (_rl_uppercase_p (rl_line_buffer[i]))
        rl_line_buffer[i] = _rl_to_lower (rl_line_buffer[i]);
      else if (_rl_lowercase_p (rl_line_buffer[i]))
        rl_line_buffer[i] = _rl_to_upper (rl_line_buffer[i]);
    }
  /* Move point to on top of the last character changed. */
  rl_point = (direction == 1) ? end - 1 : start;
  return (0);
}


int main()
{
  printf("%s \n", readline("anel> "));
  printf("%s \n", rl_gets ());
  int tmp=0;
  char *in;
  while(tmp<10)
  {
    in=readline("Enter> ");
    add_history(in);
    printf("%s \n", in);

    rl_redisplay();
    free(in);
    tmp++;
  }
	return 0;
}
