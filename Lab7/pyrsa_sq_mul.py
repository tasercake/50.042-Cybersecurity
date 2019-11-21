#!/usr/bin/env python3
"""
50.042 FCS Lab 7
Year 2019

Krishna Penukonda - 1001781
"""
from random import randint
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode


def square_multiply(a, x, n):
    y = 1
    for i in range(x.bit_length(), -1, -1):
        y = (y ** 2) % n
        if (x >> i) & 1:
            y = (a * y) % n
    return y


# function to convert long int to byte string
def pack_bigint(i):
    b = bytearray()
    while i:
        b.append(i & 0xFF)
        i >>= 8
    return b


# function to convert byte string to long int
def unpack_bigint(b):
    b = bytearray(b)
    return sum((1 << (bi * 8)) * bb for (bi, bb) in enumerate(b))


def generate_RSA(bits=1024):
    rsa = RSA.generate(bits)
    return rsa, rsa.publickey()


def encrypt_RSA(public_key_file, message):
    with open(public_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    unpacked = unpack_bigint(message)
    cipher = square_multiply(unpacked, rsa.e, rsa.n)
    packed = bytes(pack_bigint(cipher))
    packed = b64encode(packed)
    return packed


def decrypt_RSA(private_key_file, cipher):
    with open(private_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    cipher = b64decode(cipher)
    unpacked = unpack_bigint(cipher)
    message = square_multiply(unpacked, rsa.d, rsa.n)
    packed = bytes(pack_bigint(message))
    return packed

 
def sign_RSA(private_key_file, message):
    with open(private_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    hashed = SHA256.new(data=message).digest()
    unpacked = unpack_bigint(hashed)
    signature = square_multiply(unpacked, rsa.d, rsa.n)
    packed = bytes(pack_bigint(signature))
    packed = b64encode(packed)
    return packed


def verify_sign(public_key_file, sign, message):
    with open(public_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    hashed = SHA256.new(data=message).digest()
    unpacked = unpack_bigint(b64decode(sign))
    return hashed == bytes(pack_bigint(square_multiply(unpacked, rsa.e, rsa.n)))


def multiply_encrypted(public_key_file, c1, c2):
    with open(public_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    return b64encode(pack_bigint(unpack_bigint(b64decode(c1)) * unpack_bigint(b64decode(c2)) % rsa.n))


if __name__ == "__main__":
    public_key_file = "mykey.pem.pub"
    private_key_file = "mykey.pem.priv"

    print("==============================\nRSA PROTOCOL DEMO - NO PADDING\n==============================")
    with open("message.txt", "r") as message:
        message = message.read().encode('utf8')
    print("========== Encryption & Decryption ==========")
    print(f"Original:\n{message}\n")
    encrypted = encrypt_RSA(public_key_file, message)
    print(f"Encrypted:\n{encrypted}\n")
    decrypted = decrypt_RSA(private_key_file, encrypted)
    print(f"Decrypted:\n{decrypted}\n")
    print("========== Signature Verification ==========")
    print(f"Original:\n{message}\n")
    signature = sign_RSA(private_key_file, message)
    print(f"Signature:\n{signature}\n")
    verification = verify_sign(public_key_file, signature, message)
    print(f"Signature verfied:\n{verification}\n")

    print("==================================\nRSA ENCRYPTION ATTACK - NO PADDING\n==================================")
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

    print("==================================\nRSA SIGNATURE ATTACK - NO PADDING\n==================================")
    signature = randint(0, 2 ** 1024 - 1)
    print(f"Alice sends some message with (unhashed) Signature:\n{b64encode(pack_bigint(signature))}\n")
    with open(public_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    x = square_multiply(signature, rsa.e, rsa.n)
    print(f"Attacker computes a plausible message from Alice's Signature and Public Key:\n{b64encode(pack_bigint(x))}\n")
    print(f"Sending computed message and Alice's Signature to Bob...")
    x_prime = square_multiply(signature, rsa.e, rsa.n)
    print(f"Bob computes the digest from Alice's Signature using Alice's Public Key:\n{b64encode(pack_bigint(x_prime))}\n")
    print(f"Bob verifies the source of the message by comparing the computed digest to Alice's Signature:\n{x == x_prime}\n")

    print("========================================================================================================================")
    print("Note: This signature protocol attack only works if the signature is computed directly from the message (without hashing)")
