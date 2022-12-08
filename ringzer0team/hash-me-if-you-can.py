#!/usr/bin/env python3

import hashlib
import requests
from bs4 import BeautifulSoup

response = requests.get('http://challenges.ringzer0team.com:10013/')
soup = BeautifulSoup(response.text, 'html.parser')
div_element = soup.select_one('.message')
message: str = div_element.text.split()[4]
hexdigest: str = hashlib.sha512(message.encode('utf-8')).hexdigest()
params = { 'r': hexdigest }
response = requests.get('http://challenges.ringzer0team.com:10013/', params=params)
print(response.text)
