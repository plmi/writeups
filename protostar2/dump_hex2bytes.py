#!/usr/bin/env python3

import struct

data = struct.pack('<I', 0x61626364)
data = ''.join('\\x{:02X}'.format(a) for a in data)
print(data)
