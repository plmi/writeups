#!/usr/bin/env python3

import base64
import string

def hex_to_base64(hex_string: str) -> bytes:
  if not all(value in string.hexdigits for value in hex_string):
    raise ValueError('not a valid hex string')

  value: bytes = bytes.fromhex(hex_string)
  return base64.b64encode(value)

def main():
  hex_string: str = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
  base64_value: str = hex_to_base64(hex_string)
  print(base64_value.decode('utf-8'))

if __name__ == "__main__":
  main()
