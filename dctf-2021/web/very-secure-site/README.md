# Very Secure Site

## Description

> Some students have built their most secure website ever. Can you spot their mistake?  
> http://dctf1-chall-very-secure-site.westeurope.azurecontainer.io/

## Writeup

The website contains a login form together with a link to it's source code. The supplied login credentials are hashed with the tiger128,4 algorithm and compared against fixed hashes. The username must be equal to `51c3f5f5d8a8830bc5d8b7ebcb5717df` which is an [already known hash](https://md5calc.com/hash/tiger128-4/admin) for `admin`. The password's hash is unknown.

PHP does not require type definitions but a variable's type is determined by it's context. The hashes are compared with `==` instead of `===`. This will make PHP use a feature called "type juggling". It's a loose type comparison where PHP will do automatic type conversion to match the operands. Strings that match `/^0+[Ee][0-9]+$/` are interpreted as scientific notation. In this example, zero raised to any power is always zero. So any compared hash starting with "0e" will evaluate to true. A simple [bruteforce script](./brute.php) was used to find a proper hash.

Build and run the docker container:
```bash
$ docker build --no-cache -t dctf-php .
$ docker run -it --rm dctf-php
```

Here are some hashes valid hashes:
```
[+] f6z4ie:0e500199368235199063475958265410 
[+] gvyjav:0e905640747117230249363395340073
[+] oob7zq:0e904370080778016606795742408654 
[+] qql5qr:0e694925940712746493045498838403
[+] rlabzz:0e816070445316815890559202378514 
[+] r81jox:0e347004285688492273413478997415
```

Flag: `dctf{It's_magic._I_ain't_gotta_explain_shit.}`


## References
* https://www.php.net/manual/en/language.types.type-juggling.php
* https://www.darkreading.com/vulnerabilities---threats/php-hash-comparison-weakness-a-threat-to-websites-researcher-says-/d/d-id/1320353
* https://medium.com/swlh/php-type-juggling-vulnerabilities-3e28c4ed5c09
