#!/usr/bin/env python3

import base64

plaintext: str = base64.b64decode('RU9CRC43aWdxNDsxaWtiNTFpYk9PMDs6NDFS'.encode()).decode()
for i in range(2**6):
  print(f'{i}: {"".join([chr(ord(character) ^ i) for character in plaintext])}')
