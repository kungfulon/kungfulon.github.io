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
  scanf("%lu", size);
  
  magic = (unsigned long *)malloc(size[0]);
  
  if (magic)
  {
    printf("Magic:%p\n", magic);
    
    for (i = 0; i <= 2; ++i)
    {
      write(1, "offset:", 7uLL);
      scanf("%lu", &offset);
      write(1, "value:", 6uLL);
      scanf("%lu", &value);
      magic[offset] = value;
    }
  }
  
  _exit(0);
}
