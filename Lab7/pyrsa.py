#!/usr/bin/env python3
"""
50.042 FCS Lab 7
Year 2019

Krishna Penukonda - 1001781
"""
from random import randint
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode, b64encode
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from pyrsa_sq_mul import pack_bigint, unpack_bigint


def generate_RSA(bits=1024):
    print("Generating a new RSA keypair...")
    rsa = RSA.generate(bits)
    print("Done!")
    return rsa, rsa.publickey()


def encrypt_RSA(public_key_file, message):
    with open(public_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    cipher = b64encode(PKCS1_OAEP.new(rsa).encrypt(message))
    return cipher


def decrypt_RSA(private_key_file, cipher):
    with open(private_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    message = PKCS1_OAEP.new(rsa).decrypt(b64decode(cipher))
    return message


def sign_RSA(private_key_file, message):
    with open(private_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    hashed = SHA256.new(data=message)
    signature = b64encode(PKCS1_PSS.new(rsa).sign(hashed))
    return signature


def verify_sign(public_key_file, sign, message):
    with open(public_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    hashed = SHA256.new(data=message)
    return PKCS1_PSS.new(rsa).verify(hashed, b64decode(sign))


def save_key(key, filename, **kwargs):
    print(f"Saving key '{key}' to '{filename}'...")
    with open(filename, 'wb') as f:
        f.write(key.exportKey(**kwargs))
    print("Saved!")


def multiply_encrypted(public_key_file, c1, c2):
    with open(public_key_file, "r") as key:
        rsa = RSA.importKey(key.read())
    return b64encode(pack_bigint(unpack_bigint(b64decode(c1)) * unpack_bigint(b64decode(c2)) % rsa.n))


if __name__ == "__main__":
    public_key_file = "newkey.pem.pub"
    private_key_file = "newkey.pem.priv"

    print("========================\nPADDED RSA PROTOCOL DEMO\n========================")
    private_key, public_key = generate_RSA()
    save_key(public_key, public_key_file)
    save_key(private_key, private_key_file)
    print("\n=========== Padded Encryption & Decryption ===========")
    with open("mydata.txt", "r") as message:
        message = message.read().encode('utf8')
        print(f"Original message:\n{message}\n")
    encrypted = encrypt_RSA(public_key_file, message)
    print(f"Encrypted:\n{encrypted}\n")
    decrypted = decrypt_RSA(private_key_file, encrypted)
    print(f"Decrypted:\n{decrypted}\n")
    print("\n=========== Padded Signature Verification ===========")
    print(f"Original message:\n{message}\n")
    signature = sign_RSA(private_key_file, message)
    print(f"Signature:\n{signature}\n")
    verification = verify_sign(public_key_file, signature, message)
    print(f"Signature verfied:\n{verification}\n")

    print("============================\nPADDED RSA ENCRYPTION ATTACK\n============================")
    print("=========== Padded RSA Encryption Attack ===========")
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