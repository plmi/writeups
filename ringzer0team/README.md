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

# Crytography

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

## Public key recovery

> -----BEGIN RSA PRIVATE KEY-----  
> MIICXgIBAAKBgQDwkrxVrZ+KCl1cX27SHDI7EfgnFJZ0qTHUD6uEeSoZsiVkcu0/  
> XOPbz1RtpK7xxpKMSnH6uDc5On1IEw3A127wW4Y3Lqqwcuhgypd3Sf/bH3z4tC25  
> eqr5gA1sCwSaEw+yBxdnElBNOXxOQsST7aZGDyIUtmpouI1IXqxjrDx2SQIDAQAB  
> AoGBAOwd6PFitnpiz90w4XEhMX/elCOvRjh8M6bCNoKP9W1A9whO8GJHRnDgXio6  
> /2XXktBU5OfCVJk7uei6or4J9BvXRxQpn1GvOYRwwQa9E54GS0Yu1XxTPtnBlqKZ  
> KRbmVNpv7eZyZfYG+V+/f53cgu6M4U3SE+9VTlggfZ8iSqGBAkEA/XvFz7Nb7mIC  
> qzQpNmpKeN4PBVRJBXqHTj0FcqQ5POZTX6scgE3LrxVKSICmm6ungenPXQrdEQ27  
> yNQsfASFGQJBAPL2JsjakvTVUIe2JyP99CxF5WuK2e0y6N2sU3n9t0lde9DRFs1r  
> mhbIyIGZ0fIkuwZSOqVGb0K4W1KWypCd8LECQQCRKIIc8R9iIepZVGONb8z57mA3  
> sw6l/obhfPxTrEvC3js8e+a0atiLiOujHVlLqD8inFxNcd0q2OyCk05uLsBxAkEA  
> vWkRC3z7HExAn8xt7y1Ickt7c7+n7bfGuyphWbVmcpeis0SOVk8QrbqSNhdJCVGB  
> TIhGmBq1GnrHFzffa6b1wQJAR7d8hFRtp7uFx5GFFEpFIJvs/SlnXPvOIBmzBvjU  
> yGglag8za2A8ArHZwA1jXcFPawuJEmeZWo+5/MWp0j+yzQ==  
> -----END RSA PRIVATE KEY-----

The public key can be extracted from the private key.
```bash
$ openssl rsa -in pub.txt -pubout -out pub.pem
$ cat pub.pem
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDwkrxVrZ+KCl1cX27SHDI7Efgn
FJZ0qTHUD6uEeSoZsiVkcu0/XOPbz1RtpK7xxpKMSnH6uDc5On1IEw3A127wW4Y3
Lqqwcuhgypd3Sf/bH3z4tC25eqr5gA1sCwSaEw+yBxdnElBNOXxOQsST7aZGDyIU
tmpouI1IXqxjrDx2SQIDAQAB
-----END PUBLIC KEY-----

$ echo -n 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDwkrxVrZ+KCl1cX27SHDI7EfgnFJZ0qTHUD6uEeSoZsiVkcu0/XOPbz1RtpK7xxpKMSnH6uDc5On1IEw3A127wW4Y3Lqqwcuhgypd3Sf/bH3z4tC25eqr5gA1sCwSaEw+yBxdnElBNOXxOQsST7aZGDyIUtmpouI1IXqxjrDx2SQIDAQAB' | md5sum
42f51df8b6a2bafa824c179a38066e5d 
```

**Flag**: `FLAG-9869O2dQ43d1r116kfD0Sj5n`

## I Lost my password can you find it?

Group Policy Preferences / GPP can be used to set passwords for local accounts in an active directory environment, among other things. These passwords are stored in a way that any user or machine can retrieve them and decrypt them, resulting in privilege escalation or lateral movement for an attacker.

The password is encrypted with AES-256 in CBC mode. The key is public [1] [2].  
[recover-gpp.py](./recover-gpp.py)

[1] https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be  
[2] https://web.archive.org/web/20150221052902/https://blog.csnc.ch/2012/04/exploit-credentials-stored-in-windows-group-policy-preferences/

**Flag**: `LocalRoot!`

## Martian message part 3

> RU9CRC43aWdxNDsxaWtiNTFpYk9PMDs6NDFS

The message was XORed with `k = 3` and base64 encoded. `y = base64(x ^ 3)`  
[martian-message-3.py](./martian-message-3.py)

**Flag**: `FLAG-4jdr782jha62jaLL38972Q`
