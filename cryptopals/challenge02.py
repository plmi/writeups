#!/usr/bin/env python3

import binascii

def xor_on_bytes(hex_string_1: str, hex_string_2: str) -> bytes:
  byte_array_1: bytes = bytes.fromhex(hex_string_1)
  byte_array_2: bytes = bytes.fromhex(hex_string_2)
  return bytes(a ^ b for (a, b) in zip(byte_array_1, byte_array_2))

def xor_on_integers(hex_string_1: str, hex_string_2: str) -> bytes:
  number_1: int = int(hex_string_1, 16)
  number_2: int = int(hex_string_2, 16)
  return binascii.unhexlify(hex(number_1 ^ number_2)[2:])

def main():
  hex_string_1: str = '1c0111001f010100061a024b53535009181c'
  hex_string_2: str = '686974207468652062756c6c277320657965'
  xor_result: bytes = xor_on_integers(hex_string_1, hex_string_2)
  expected: str = '746865206b696420646f6e277420706c6179'
  assert binascii.hexlify(xor_result).decode() == expected, 'result doesn\'t match expected value'

if __name__ == "__main__":
  main()
