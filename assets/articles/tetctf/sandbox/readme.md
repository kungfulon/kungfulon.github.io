`program` có sẵn lỗi stack overflow cơ bản, nhưng trước khi return nó close `stdin` và `stdout` => cần reverse shell.
`program` được link static => rop chain gọi `_dl_make_stack_executable` để sử dụng shellcode exploit cho đơn giản hơn.
Vấn đề là `program` bị `sandbox` dùng `ptrace` monitor syscall nên ta không thể lên shell hoặc mở file flag một cách thông thường.
Từ đây có 2 hướng giải quyết:

- Chuyển mode sang x86: Vì syscall number của x86 khác x64 nên ta có thể lợi dụng điều này để vượt syscall monitor. Push `(0x23 << 32) | ret_addr` rồi far return (`retf`), ta sẽ chuyển sang x86 mode. Lưu ý là khi về mode này thì miền địa chỉ sẽ là 32 bit nên ta cần chạy code ở vùng nhớ có địa chỉ nhỏ hơn `0xffffffff`. Truy xuất bộ nhớ cũng phải được thực hiện ở miền địa chỉ 32 bit, nên `sp` cũng phải nhro hơn `0xffffffff`. Đọc 32 bit shellcode vào section `.bss` (địa chỉ `0x6bb2e0`), gán `rsp` về đó, rồi nhảy đến đó là được. Đây là cách unintended, và cũng là cách đầu tiên mình làm trước khi khám phá ra cách tiếp theo.

- Kill `sandbox`: Trong hàm monitor syscall, ta thấy rằng nó không cấm `SYS_kill` và `SYS_getppid`. Gọi `SYS_getppid` lấy PID của `sandbox` rồi gọi `SYS_kill` để kill `sandbox`. Sau khi kill `sandbox`, ta có thể lên shell hoặc mở file flag bình thường. Đây là cách intended. Script exploit theo cách này ở file `poc.py`.

Flag của challenge là:

```
TetCTF{H4PPY->N3W->Y34R}
```
