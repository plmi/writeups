# Forgotten Secret (100)

## Description:
```
Last month we hired a new junior DevOps Enginner to migrate all our services into containers. He was super hyped about Docker and in such a hurry, that he forgot about best practices. You want to use one of our images? Sure, no problem. Just download image file, run "docker load < image" and you are ready to go!

Hint: Don't run it, try to inspect it!
```

## Writeup

The docker image is a `.tar` file.
```bash
$ mv image{,.tar}
$ tar -xf image.tar
```

In the root folder of the image there is a json file containing a stripped command history and some environment variables.
```
"Env": [
  "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  "SECRET_KEY=58703273357638792F423F4528482B4D6251655468566D597133743677397A24"
],

"created_by": "/bin/sh -c chmod 600 /root/.ssh/id_rsa"
"created_by": "/bin/sh -c chmod 600 /home/alice/cipher.bin"
```

By listing the content of each folder the necessary files can be quickly identified:
```bash
$ find . -type f -name "*.tar" -exec echo {} \; -exec tar -tvf {} \;
```

This private key can not directly be used to decrypt `cipher.bin` because it is in a non-standard OpenSSH format that is not compatible to OpenSSL! ([The OpenSSH Private Key Format](https://coolaj86.com/articles/the-openssh-private-key-format/)). The key must be converted first with the secret key found in the json.
```bash
$ ssh-keygen -f id_rsa -m pem -p
```

Now the cipher can be decrypted:
```bash
$ openssl rsautl -decrypt -in cipher.bin -out flag.txt -inkey id_rsa
```

Flag: `dctf{k33p_y0r_k3ys_s4f3}`

### References
* https://www.thedigitalcatonline.com/blog/2018/04/25/rsa-keys/
* https://coolaj86.com/articles/the-openssh-private-key-format/
* https://coolaj86.com/articles/openssh-vs-openssl-key-formats/
* https://gist.github.com/mingfang/4aba327add0807fa5e7f#gistcomment-3224467



