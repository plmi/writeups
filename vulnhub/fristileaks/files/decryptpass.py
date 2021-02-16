#!/usr/bin/env python3
import base64
import codecs
import sys

def decodeString(str):
    de13 = codecs.decode(str, 'rot13')
    rev13 = de13[::-1]
    return base64.b64decode(rev13).decode()

enc = sys.argv[1]
print(decodeString(enc))
