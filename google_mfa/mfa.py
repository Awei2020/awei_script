#!/usr/bin/env python
# -*- coding:utf-8 -*-

import base64
import hashlib
import hmac
import struct
import time


def g_code_3(token):
    key = base64.b32decode(token)
    pack = struct.pack(">Q", int(time.time()) // 30)
    sha = hmac.new(key, pack, hashlib.sha1).digest()
    o = sha[19] & 15

    pwd = str((struct.unpack(">I", sha[o:o + 4])[0] & 0x7fffffff) % 1000000)
    code = str(0) + str(pwd) if len(pwd) < 6 else pwd
    return code


if __name__ == '__main__':
    print(g_code_3('xxxxxxx'))
    input("Press Enter to exit...")
