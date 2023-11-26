## Level 1

Send an HTTP request using curl
```bash
$ curl http://127.0.0.1:80
pwn.college{oXv4envQ8zPzx591dynW1XVOUkP.dhjNyMDLwIDNyQzW}
```

## Level 2

Send an HTTP request using nc
```bash
$ echo -ne "GET / HTTP/1.1\r\n\r\n" | nc 127.0.0.1 80
pwn.college{oi0aATQaMcqIMQrUOfM920DwrEg.dljNyMDLwIDNyQzW}
```

## Level 3

Send an HTTP request using python
```python
#!/usr/bin/env python3

import requests

print(requests.get('http://127.0.0.1/').text)

# pwn.college{wXdFcT-xgsPvXmrzyxtkpRLBVvn.dBzNyMDLwIDNyQzW
```

## Level 4

Set the host header in an HTTP request using curl

```bash
$ curl http://127.0.0.1 -H "Host: 723609f5c02cd654473f10ffd3f3a030"
pwn.college{cXNJqUMJaq1dFO7PZ_1yBVIgaV0.dFzNyMDLwIDNyQzW}
```

## Level 5

Set the host header in an HTTP request using nc
```bash
$ echo -ne "GET / HTTP/1.1\r\nHost: 5cc6781d436fd50c8067f521ca55b886\r\n\r\n" | nc 127.0.0.1 80
pwn.college{QS0hWS1wBRKU-50Bx3NJ5NTUJ0u.dJzNyMDLwIDNyQzW}
```

## Level 6

Set the host header in an HTTP request using python
```python
#!/usr/bin/env python3

import requests

headers: dict = {'Host': 'f2ee03a11e23ee717e97a3a0af6e1ea1'}
print(requests.get('http://127.0.0.1/', headers=headers).text)

#pwn.college{0hi1_uyK-W1QUxmhk-EAqKArawN.dNzNyMDLwIDNyQzW}
```

## Level 7

Set the path in an HTTP request using curl
```bash
$ curl http://127.0.0.1/10429fcc92340131062dd0f1d3e4396a
pwn.college{ITCFbNBDRHjM-_UTyH-a56QOGSn.dRzNyMDLwIDNyQzW}
```

## Level 8

Set the path in an HTTP request using nc
```bash
$ echo -ne "GET /b01ef656a0b53eca1b417dc8264014e5 HTTP/1.1\r\n\r\n" | nc 127.0.0.1 80
HTTP/1.1 200 OK
Server: Werkzeug/3.0.1 Python/3.8.10
Date: Sat, 25 Nov 2023 22:11:54 GMT
Content-Length: 58
Server: pwn.college
Connection: close

pwn.college{Qj5pC-jXHsY-yppFBFcMA7JJUGj.dVzNyMDLwIDNyQzW}
```

## Level 9

Set the path in an HTTP request using python
```python
#!/usr/bin/env python3

import requests

print(requests.get('http://127.0.0.1/8bc11e3eed03d0863ec3a15e6279914f').text)

# pwn.college{8ZTp0gHa5Wq_acxB3VTi-niFKRP.dZzNyMDLwIDNyQzW}
```

## Level 10

URL encode a path in an HTTP request using curl
```bash
$ curl "http://127.0.0.1/$(echo -n "0390a634 4170a681/3c4729de d26cb691" | sed 's/ /%20/g')"
pwn.college{8ihS4J_k4--fb-D-Jo99ke6skOM.ddzNyMDLwIDNyQzW}
```

## Level 11

URL encode a path in an HTTP request using nc
```bash
$ echo -ne "GET /629dd18c%20ce22ccfb/fab89b60%20f25eb2d6 HTTP/1.1\r\n\r\n" | nc 127.0.0.1 80
```

## Level 12

URL encode a path in an HTTP request using python
```python
#!/usr/bin/env python3

import requests

print(requests.get('http://127.0.0.1/8971ce42 eba8d8df/c191610a 53b0c04f').text)

# pwn.college{c1nEoBowak-sc22GCONJPRcQ_qb.dlzNyMDLwIDNyQzW}
```

## Level 13

Specify an argument in an HTTP request using curl
```bash
$ curl --get http://127.0.0.1 --data-urlencode "a=74373b81f7cd58a79b5fbfa68f9be6a1"
pwn.college{ITO3GaITFYxWtJr5UaK9h7JVKvs.dBDOyMDLwIDNyQzW}
```

## Level 14

Specify an argument in an HTTP request using nc
```bash
$ echo -ne "GET /?a=705f3e0b74e999f4ee37f0d441d012e4 HTTP/1.1\r\n\r\n" | nc 127.0.0.1 80
pwn.college{A7fWXPcbUUA2OKFsVupJeqseypa.dFDOyMDLwIDNyQzW}
```

## Level 15

Specify an argument in an HTTP request using python
```python
#!/usr/bin/env python3

import requests

params: dict = {'a': '8bc0b79c5917095f1e474cdd71121691'}
print(requests.get('http://127.0.0.1/', params=params).text)

# pwn.college{4_qPSdJQ2fsj_YIb2LuGNORkjY9.dJDOyMDLwIDNyQzW}
```

## Level 16

Specify multiple arguments in an HTTP request using curl
```bash
$ curl --get http://127.0.0.1 --data-urlencode "a=e0e799e60624ee26bcf3a670467b6da6" --data-urlencode "b=4610ee71 66c4767e&74e13244#5a391875"
pwn.college{Ac4X3ESMVHzqsNNrevqw_2jSYqW.dNDOyMDLwIDNyQzW}
```

## Level 17

Specify multiple arguments in an HTTP request using nc
```bash
$ b=$(perl -MURI::Escape -e 'print uri_escape($ARGV[0]);' "36e85582 c4cc2bd0&20cf4465#b89e4970")
$ echo -ne "GET /?a=df1901f96c156e2847bb6ba476f68ffd&b=$b HTTP/1.1\r\n\r\n" | nc 127.0.0.1 80
pwn.college{Qm0UEGmTfkmujBe9IYKkTSDeJHW.dRDOyMDLwIDNyQzW}
```

## Level 18

Specify multiple arguments in an HTTP request using python
```python
#!/usr/bin/env python3

import requests

params: dict = {'a': '4f7589d7c80f9988aba35562d68835b0', 'b': '48c0697d 746235e2&1acaa52f#f565401d'}
print(requests.get('http://127.0.0.1/', params=params).text)

# pwn.college{IscMFNSRBoibVRLw_w2qr-f3JIz.dVDOyMDLwIDNyQzW}
```

## Level 19

Include form data in an HTTP request using curl
```bash
$ curl http://127.0.0.1 --data-urlencode "a=d23f0dc7dca3b498318f20b2977f6b00"
pwn.college{U4ZJVncCYs02qI3JYToLNJrY_r1.dZDOyMDLwIDNyQzW}
```

## Level 20
Include form data in an HTTP request using nc
```bash
$ echo -ne "GET / HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 34\r\n\r\na=f8ae08b2d0f0373c18e5f89918bd6d9a" \
    | nc 127.0.0.1 80
pwn.college{AbkNqggyRt8Qx4UQUyM8y1kCyJS.ddDOyMDLwIDNyQzW}
```

## Level 21

Include form data in an HTTP request using python
```python
#!/usr/bin/env python3

import requests

data: dict = {'a': '8b97d9b8dba18c7c778f56fe11ffea30'}
print(requests.post('http://127.0.0.1/', data=data).text)

# pwn.college{IuEdehaPuk7jXdb1T4pzuUFelMR.dhDOyMDLwIDNyQzW}
```

## Level 22

Include form data with multiple fields in an HTTP request using curl
```bash
$ curl http://127.0.0.1 --data-urlencode "a=03654809ed180ee57ff9669017f00b4d" --data-urlencode "b=fe3cfdaf 01488a32&34239814#91ec4995"
pwn.college{YskVszShEgXLxCWkWO2LmC_Njer.dlDOyMDLwIDNyQzW}
```

## Level 23

Include form data with multiple fields in an HTTP request using nc
```bash
$ b=$(perl -MURI::Escape -e 'print uri_escape($ARGV[0]);' "c4eb82a4 b72af8bd&9d3d2f65#e5a1610f")
$ echo -ne "POST / HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 78\r\n\r\na=f411f84bf145e7ae53895d5ee5b39120&b=c4eb82a4%20b72af8bd%269d3d2f65%23e5a1610f" | nc 127.0.0.1 80
pwn.college{gWx1BCoiujZJm7xxJQSKQ4ztyUW.dBTOyMDLwIDNyQzW}
```

## Level 24

Include form data with multiple fields in an HTTP request using python
```python
#!/usr/bin/env python3

import requests

data: dict = {'a': '9a8ace6e1f19a309c7340654ab7f2423', 'b': 'e58c7edb be4b182d&2c1fb10e#89b29b53'}
print(requests.post('http://127.0.0.1/', data=data).text)

# pwn.college{QF4b1M-bGY5pxq-nXhUIurDngoK.dFTOyMDLwIDNyQzW}
```

## Level 25

Include json data in an HTTP request using curl
```bash
$ curl http://127.0.0.1 -H "Content-Type: application/json" -d '{"a":"c487a1e79f302472a97e101d1e49d14f"}'
pwn.college{ETLgTv1uAwmTIw5dZr3HmT8UNo-.dJTOyMDLwIDNyQzW}
```

## Level 26

Include json data in an HTTP request using nc
```bash
$ echo -ne 'POST / HTTP/1.1\r\nContent-Type: application/json\r\nContent-Length: 40\r\n\r\n{"a":"0ff725fbb0068d8faaf43866c2c0206a"}' \
    | nc 127.0.0.1 80
pwn.college{Et0Dlwyb7IJxRE90EYIAyzasHPo.dNTOyMDLwIDNyQzW}
```

## Level 27

Include json data in an HTTP request using python
```python
#!/usr/bin/env python3

import requests

json: dict = {'a': 'f5ebe636dedcc3a70b4e2966297cab1c'}
print(requests.post('http://127.0.0.1/', json=json).text)

# pwn.college{YLPnLjpTb6p0phX2oGv7j7BBMUf.dRTOyMDLwIDNyQzW}
```

## Level 28

Include complex json data in an HTTP request using curl

Create a json file `payload.json`.
```json
{
    "a": "eb92e6f38bbb6872652cd5dbcdfc6cf9",
    "b": {
        "c": "8d7414cd",
        "d": [
            "db416ec7",
            "aa1cf86b c7bc55ac&e1d48728#eb7625a0"
        ]
    }
}
```

Send `payload.json` with `curl`.
```bash
$ curl http://127.0.0.1 -d @./payload.json -H "Content-Type: application/json"
pwn.college{ga-iNynWzALncgI4PXHemENMMd8.dVTOyMDLwIDNyQzW}
```

## Level 29

Include complex json data in an HTTP request using nc

```bash
$ echo -ne 'POST / HTTP/1.1\r\nContent-Type: application/json\r\nContent-Length: 116\r\n\r\n{"a":"6143168d26ffbdec5791246d751e5228","b":{"c":"cb839a96","d":["d86b09f9","889f4f92 312fcf2a&a6bdc85d#e68f26b1"]}}' | nc 127.0.0.1 80
pwn.college{cLbarVgDpzm02m2osAxumHNclMn.dZTOyMDLwIDNyQzW}

# or
$ cat payload.json
{"a":"6143168d26ffbdec5791246d751e5228","b":{"c":"cb839a96","d":["d86b09f9","889f4f92 312fcf2a&a6bdc85d#e68f26b1"]}}
# trim newline of cat
$ json=$(cat payload.json | tr --delete '\n')
$ printf "POST / HTTP/1.1\r\nContent-Length: 116\r\nContent-Type: application/json\r\n\r\n%s" "$json" | nc 127.0.0.1 80
pwn.college{cLbarVgDpzm02m2osAxumHNclMn.dZTOyMDLwIDNyQzW}
```

## Level 30

Include complex json data in an HTTP request using python
```python
#!/usr/bin/env python3

import requests

json: dict = {
    'a': 'bac999e44efe40fd4be50b1c054bd0c9',
    'b': {
        'c': '6b3554b3',
        'd': ['c2abaef0','5d316970 b08a004e&fad7934d#0c4ca1d8']
    }
}
print(requests.post('http://127.0.0.1/', json=json).text)

# pwn.college{0Tn1Fk4J6nxYAObPOvWZd5RGHOq.ddTOyMDLwIDNyQzW}
```

## Level 31

Follow an HTTP redirect from HTTP response using curl
```bash
$ curl -L http://127.0.0.1
pwn.college{AKReOyCTppb2k3vwNooTVRthSNy.dhTOyMDLwIDNyQzW}
```

## Level 32

Follow an HTTP redirect from HTTP response using nc
```bash
#!/bin/bash

HOST="127.0.0.1"
PORT="80"
LOCATION_HEADER_VALUE=$(echo -ne "GET / HTTP/1.1\r\n\r\n" | nc "$HOST" "$PORT" | grep -oP "(?<= )\/[a-f0-9]{32}")
echo -ne "GET ${LOCATION_HEADER_VALUE} HTTP/1.1\r\n\r\n" | nc "$HOST" "$PORT"
```
```text
pwn.college{AoguBlNoIqRDDzac27_nUDoAG8F.dlTOyMDLwIDNyQzW}
```

## Level 33

Follow an HTTP redirect from HTTP response using python
```python
#!/usr/bin/env python3

import requests

json: dict = {
    'a': 'bac999e44efe40fd4be50b1c054bd0c9',
    'b': {
        'c': '6b3554b3',
        'd': ['c2abaef0','5d316970 b08a004e&fad7934d#0c4ca1d8']
    }
}
print(requests.post('http://127.0.0.1/', json=json).text)

# pwn.college{gxzoh4sa3njVzqF_tf6vajjNfxH.dBDMzMDLwIDNyQzW}
```

## Level 34

Include a cookie from HTTP response using curl
```bash
$ curl -c cookie.txt http://127.0.0.1 && curl -b cookie.txt http://127.0.0.1
pwn.college{4DmW6HP21EXcwV5mgalfyNGFjnb.dFDMzMDLwIDNyQzW}
```

## Level 35

```bash
#!/bin/bash

COOKIE=$(echo -ne "GET / HTTP/1.1\r\n\r\n" | nc 127.0.0.1 80 | grep -oE "cookie=[a-f0-9]{32}")
echo -ne "GET / HTTP/1.1\r\nCookie: ${COOKIE}\r\n\r\n" | nc 127.0.0.1 80
```
```text
pwn.college{g2UI5sTRzg5HnVu4NHGdJmZEeQZ.dJDMzMDLwIDNyQzW}
```
