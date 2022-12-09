# Coding Challenges

## Hash me if you can (2)

> You have 2 seconds to hash this message using sha512 algorithm. Send the answer back using http://challenges.ringzer0team.com:10013/?r=[your_response]

Crawl the message from the website, hash it and send it to the endpoint.  
[hash-me-if-you-can.py](./hash-me-if-you-can.py)

**Flag**: `FLAG-mukgu5g2w932t2kx1nqnhhlhy4`

## Hash me reloaded (3)

> You have 2 seconds to hash this message using sha512 algorithm. Send the answer back using http://challenges.ringzer0team.com:10013/?r=[your_response]

Crawl the message from the website. The message is binary string. Each character is 8 byte.  
Decode it, hash it and send it to the endpoint.  
[hash-me-if-you-can.py](./hash-me-if-you-can.py)

**Flag**: `FLAG-jz145p93ei75buh1kpx9bul9xl`

# Crytographie

## Some martian message (1)

> SYNTPrfneVfPbbyOhgAbgFrpher

It's encrypted with caesar cipher with `k = 13`  
[some-martian-message](./some-martian-message.py)

**Flag**: `FLAGCesarIsCoolButNotSecure`

## You're drunk

> Ayowe awxewr nwaalfw die tiy rgw fklf ua xgixiklrw! Tiy lew qwkxinw.

It's a simple substitution cipher that can be broken with [frequency analysis](https://www.dcode.fr/monoalphabetic-substitution).  
SUPER SECRET MESSAGE FOR YOU THE GLAG IS CHOCOLATE! YOU ARE WELCOME.

**Flag**: `CHOCOLATE`

## File recovery

The flag is encrypted with RSA. The private key is PEM encoded.  
```bash
$ openssl pkeyutl -decrypt -inkey private.pem -in flag.enc
FLAG-vOAM5ZcReMNzJqOfxLauakHx
```

**Flag**: `FLAG-vOAM5ZcReMNzJqOfxLauakHx`


