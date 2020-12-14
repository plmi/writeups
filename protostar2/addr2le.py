#!/usr/bin/env python3

import struct
import sys

# converts address to little endian
# usage: ./addr2le.py 0x804842
# output: \x24\x84\x04\x08

address = int(sys.argv[1], 16)
data = struct.pack('<I', address)
data = ''.join('\\x{:02X}'.format(a) for a in data)
print(data)
