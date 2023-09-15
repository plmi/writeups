# Writeup: Wintermute

## Host Discovery

We do a regular `ping sweep` scan to get the machine's IP address:
```bash
$ nmap -sn -PE -n --disable-arp-ping 192.168.10.0/24
192.168.10.108
$ export ip='192.168.10.108'
```

## Scanning
After that we scan the machine for top 1000 ports:
```bash
$ nmap -Pn -n -sS -oA nmap/1000_tcp --reason $ip
PORT     STATE SERVICE
25/tcp   open  smtp
80/tcp   open  http
3000/tcp open  ppp
```

## Enumeration

### Port 80
Even though privoting is not needed yet we can train it here already. We do some local port forwarding. Here is my current setup:
```bash
# Ubuntu (Host) --> Kali (smooth) --> Straylight
```
I want to connect to `Straylight:80` from my host's browser through the Kali box.
We create a listener on port 8888. We send our traffic through the SSH tunnel to our target Kali machine who will then forward it to the Straylight box:
```bash
$ ssh -L 8888:192.168.10.108:80 root@smooth
# Ubuntu:8888 -- SSH Tunnel --> Kali --> Straylight:80
```
We now can access the webserver's index page via `http://localhost:8888`.


### Port 3000

We see some kind of dashboard running. 
```text
ntopng Community 2.4.180512
```
The source mentions default credentials `admin:admin` which work.  
There seems to be a service listening on port `6379` (redis cache) which is either blocked by a firewall or is not listening on all interfaces.
