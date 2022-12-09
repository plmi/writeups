#!/usr/bin/env python3

def decrypt_character(character: chr, k: int) -> chr:
  if character.isupper():
    return chr((ord(character) - ord('A') + k) % 26 + ord('A'))
  return chr((ord(character) - ord('a') + k) % 26 + ord('a'))

def rotate(message: str, k: int) -> str:
  plaintext: str = ''
  for i in range(len(message)):
    plaintext += decrypt_character(message[i], k)
  return plaintext

message: str = 'SYNTPrfneVfPbbyOhgAbgFrpher'

for i in range(26):
  print(f'{i}: {rotate(message, i)}')
