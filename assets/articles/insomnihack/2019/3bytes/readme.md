# 3bytes

The program lets us write 3 bytes to arbitrary addresses.
The first thing that came to my mind is patching .GOT entry - but since the binary is PIE enabled, bruteforcing is not a clean solution.
After that I started auditing glibc code. The program call `exit(1337)`, so let's look at `exit` implementation in [`glibc/stdlib/exit.c`](https://code.woboq.org/userspace/glibc/stdlib/exit.c.html).

There's a list of exit function (`__exit_funcs`), but `PTR_DEMANGLE` prevented me from patching it easily.
After some hopeless debugging, I saw that `_dl_fini` is an exit function. Looking through its definition in [`glibc/elf/dl-fini.c`](https://code.woboq.org/userspace/glibc/elf/dl-fini.c.html), I saw two interesting call:

``` c
__rtld_lock_lock_recursive (GL(dl_load_lock));
// ...
__rtld_lock_unlock_recursive (GL(dl_load_lock));
```

Those `__rtld` macros are defined in [`glibc/sysdeps/generic/libc-lock.h`](https://github.molgen.mpg.de/git-mirror/glibc/blob/master/sysdeps/mach/hurd/libc-lock.h), and we can patch them!

Since `libc` will be mapped above `ld` in the virtual space, and the offset between them is constant for each environment, we can calculate the address easily.
We also have `Dockerfile` of this challenge, so build it and calculate the offset between `libc` and `ld`.
Finally, patch one of those pointer to `one_gadget` and boom, we'll get a shell.
We only need 3 bytes to do the patching, since the offset between `libc` and `ld` is relatively small (on the docker it's `0x3f1000`)
