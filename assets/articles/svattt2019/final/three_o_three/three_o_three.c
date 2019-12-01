#include <unistd.h>
#include <stdio.h>

int main()
{
  int i;
  unsigned long size;
  unsigned long offset;
  unsigned long value;
  unsigned long *magic;

  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  
  write(1, "Size:", 5);
  scanf("%lu", &size);
  
  magic = (unsigned long *)malloc(size);
  
  if (magic)
  {
    printf("Magic:%p\n", magic);
    
    for (i = 0; i < 3; ++i)
    {
      write(1, "offset:", 7);
      scanf("%lu", &offset);
      write(1, "value:", 6);
      scanf("%lu", &value);
      magic[offset] = value;
    }
  }
  
  _exit(0);
}
