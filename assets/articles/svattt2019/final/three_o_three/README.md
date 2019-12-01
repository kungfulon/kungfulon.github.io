# Three-O-Three

This challenge is similar to HITCON CTF 2019 Qualifiers Trick Or Treat, except that the progam will use `%lu` to read offset & value that we enter.
After reading the (https://syedfarazabrar.com/2019-10-14-hitconctf-2019-trick-or-treat/)[writeup by Syed Faraz Abrar], we tried some approaches:

- Overwrite `__malloc_hook` or `__free_hook` with `one_gadget` - FAIL
- Overwrite `__malloc_hook` with `free` and overwrite `__free_hook` with `one_gadget` - FAIL
- Overwrite `__free_hook` with `system` but there are nothing we can run with numbers and `+` and `-` - FAIL

Then we remembered a challenge in InsomniHack 2019 that I have solved before: (https://nyancat0131.vpwn.io/article/7)[3bytes].
At first, we only overwrote `__rtld_lock_unlock_recursive` with `one_gadget`, but since the program call `_exit` and not `exit`, the exit routine was not executed.
Then we decided to overwrite `__malloc_hook` with `exit` and `__rtld_lock_unlock_recursive` with `one_gadget`.
This approach worked perfectly.
