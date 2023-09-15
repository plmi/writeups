#!/usr/bin/env python3

import string
import binascii

def all_printable_bytes(value: bytes) -> bool:
  return not any(chr(char) not in string.printable for char in value)

def xor(hex_string: str, key: int) -> bytes:
  if not all(value in string.hexdigits for value in hex_string):
    raise ValueError('not a valid hex string')

  bytes_value: bytes = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
  # iterating over bytes will return integers
  return bytes(value ^ key for value in bytes_value)

def main():
  hex_string: str = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
  for key in range(0, 256):
    result: bytes = xor(hex_string, key)
    if all_printable_bytes(result):
      print(f'key {key}: {result}')

if __name__ == "__main__":
  main()
