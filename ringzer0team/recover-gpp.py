#!/usr/bin/env python3

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

block_size: int = 32
password: str = base64.b64decode('PCXrmCkYWyRRx3bf+zqEydW9/trbFToMDx6fAvmeCDw=')
key: str = bytes.fromhex('4e9906e8fcb66cc9faf49310620ffee8f496e806cc057990209b09a433b66c1b')
iv: bytes = b'\x00' * 16
aes = AES.new(key, AES.MODE_CBC, iv)
plaintext: str = aes.decrypt(password).decode('ascii')

print(plaintext)
