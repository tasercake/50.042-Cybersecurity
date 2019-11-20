#!/usr/bin/env python3
"""
50.042 FCS Lab 7
Year 2019

Krishna Penukonda - 1001781
"""
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode, b64encode
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
import argparse
import sys
import pyrsa
import pyrsa_sq_mul


if __name__ == "__main__":
    with open("mykey.pem.pub", 'r') as key:
        alice_public = RSA.importKey(key.read())
	print("")
