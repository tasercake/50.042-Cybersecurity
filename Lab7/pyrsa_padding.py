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



def generate_RSA(bits=1024):
    rsa = RSA.generate(bits)
    return rsa, rsa.publickey()


def encrypt_RSA(public_key_file, message):
    with open(public_key_file, 'r') as key:
        rsa = RSA.importKey(key.read())
    unpacked = unpack_bigint(message)
    cipher = square_multiply(unpacked, rsa.e, rsa.n)
    packed = bytes(pack_bigint(cipher))
    return packed


def decrypt_RSA(private_key_file, cipher):
    with open(private_key_file, 'r') as key:
        rsa = RSA.importKey(key.read())
    unpacked = unpack_bigint(cipher)
    message = square_multiply(unpacked, rsa.d, rsa.n)
    packed = bytes(pack_bigint(message))
    return packed


def sign_RSA(private_key_file, message):
    with open(private_key_file, 'r') as key:
        rsa = RSA.importKey(key.read())
    hashed = SHA256.new(data=message).digest()
    unpacked = unpack_bigint(hashed)
    signature = square_multiply(unpacked, rsa.d, rsa.n)
    packed = bytes(pack_bigint(signature))
    return packed


def verify_sign(public_key_file, sign, message):
    with open(public_key_file, 'r') as key:
        rsa = RSA.importKey(key.read())
    hashed = SHA256.new(data=message).digest()
    unpacked = unpack_bigint(sign)
    return hashed == bytes(pack_bigint(square_multiply(unpacked, rsa.e, rsa.n)))
