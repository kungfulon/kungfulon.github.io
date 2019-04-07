#!/usr/bin/env python2

from pwn import *
from unicorn import *
from unicorn.x86_const import *

context.log_level = "error"

b = ELF("./999")
ins = ""
alp = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

with open("./999", "rb") as f:
    ins = f.read()

# emulator constants
prog = 0x400000
state_addr = 0x8C1620
key_addr = 0x900000
stack = 0x7fffff7ef000
stack_size = 0x800000

# state variables
key = []
patched_fn = set()

# emulator initialize
mu = Uc(UC_ARCH_X86, UC_MODE_64)
mu.mem_map(prog, 0x1000000)
mu.mem_map(stack, stack_size)
mu.mem_write(prog, ins)

# anti stack canaries
mu.mem_write(0x400BAB, "\x90" * 0xD)
mu.mem_write(0x400BF8, "\x90" * 0x14)

# brute force function
def brute(pfn, fn_len, key_idx, check_len):
    global key

    for i in range(0, check_len):
        for j in alp:
            mu.mem_write(key_addr + key_idx + i, j)
            end_addr = pfn + fn_len - 1
            mu.reg_write(UC_X86_REG_RSP, stack + stack_size - 1)
            mu.mem_write(state_addr + 0x18, p32(key_idx))
            mu.emu_start(pfn, end_addr)
            rip = mu.reg_read(UC_X86_REG_RIP)
            new_key_idx = u32(mu.mem_read(state_addr + 0x18, 4))

            if new_key_idx - key_idx > i + 1 or rip == end_addr:
                key[key_idx + i] = j
                break

# unlock function
def unlock(itr):
    global key

    base = 0x6CB0A0 + (itr << 11)
    key = list("\x00" * 128)

    for i in range(0, 64):
        pfn = u32(b.read(base, 4))
        fn_len = u32(b.read(base + 4, 4))
        xor_key = u32(b.read(base + 8, 4))
        key_idx = u32(b.read(base + 12, 4))
        check_len = u32(b.read(base + 16, 4))
        base += 20

        if pfn == 0:
            continue

        if pfn not in patched_fn:
            patched_fn.add(pfn)
            func = mu.mem_read(pfn, fn_len)
            xored_func = ""
            
            for j in range(0, fn_len):
                xored_func += p8(func[j] ^ xor_key)
            
            mu.mem_write(pfn, xored_func)

        state_dat = p32(pfn) + p32(fn_len) + p32(xor_key) + p32(0x0) + p64(key_addr) + p32(key_idx) + p32(check_len)

        for j in range(0, check_len):
            state_dat += b.read(base + j * 4, 4)

        base += check_len * 4
        mu.mem_write(state_addr, state_dat)
        brute(pfn, fn_len, key_idx, check_len)

    print ''.join(key).rstrip('\x00')
    sys.stdout.flush()

for i in range(0, 999):
    unlock(i)
