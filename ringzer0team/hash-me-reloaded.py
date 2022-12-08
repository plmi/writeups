#!/usr/bin/env python3

import requests
import hashlib
from bs4 import BeautifulSoup

url: str = 'http://challenges.ringzer0team.com:10014/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
div_element = soup.select_one('.message')
message: str = div_element.text.split()[4]
message = ''.join([chr(int(message[i:i+8], 2)) for i in range(0, len(message), 8)])
hexdigest: str = hashlib.sha512(message.encode('utf-8')).hexdigest()
response = requests.get(url, params={'r':hexdigest})
print(response.text)
