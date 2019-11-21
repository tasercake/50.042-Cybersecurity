#!/usr/bin/env python3
"""
50.042 FCS Lab 7
Year 2019

Krishna Penukonda - 1001781
"""
from random import randint
from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode
from pyrsa import encrypt_RSA, decrypt_RSA
from pyrsa_sq_mul import square_multiply, pack_bigint, unpack_bigint


def multiply_encrypted(public_key_file, c1, c2):
    with open(public_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    return b64encode(pack_bigint(unpack_bigint(b64decode(c1)) * unpack_bigint(b64decode(c2)) % rsa.n))


if __name__ == "__main__":
    public_key_file = "mykey.pem.pub"
    private_key_file = "mykey.pem.priv"

    print("============================\nPADDED RSA ENCRYPTION ATTACK\n============================")
    message = 100
    multiplier = 2
    print(f"Chosen Integer:\n{message}\n")
    print(f"Multiplier:\n{multiplier}\n")
    encrypted = encrypt_RSA(public_key_file, pack_bigint(message))
    print(f"Encrypted Integer:\n{encrypted}\n")
    encrypted_multiplier = encrypt_RSA(public_key_file, pack_bigint(multiplier))
    print(f"Encrypted Multiplier:\n{encrypted_multiplier}\n")
    result = multiply_encrypted(public_key_file, encrypted, encrypted_multiplier)
    print(f"Multiplication Result:\n{result}\n")
    decrypted = decrypt_RSA(private_key_file, result)
    print(f"Decrypted:\n{unpack_bigint(decrypted)}\n")

    # print("====================\nRSA SIGNATURE ATTACK\n====================")
    # with open(public_key_file, "r") as key:
    #     rsa_pub = RSA.importKey(key.read())
    # with open(private_key_file, "r") as key:
    #     rsa_priv = RSA.importKey(key.read())

    # sign = randint(0, 2 ** 1024 - 1)
    # print(f"Signature:\n{sign}\n")
    # newmsg = square_multiply(sign)
    # with open("message.txt", "r") as message:
    #     message = message.read().encode('utf8')
    # print(message)
