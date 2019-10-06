#!/usr/bin/env python3
# Student ID: 1001781
# Name: Krishna Penukonda
from pwn import remote


# Determined by comparing the relative frequencies of characters in 
# a large corpus of text and the ciphertext.
# The map was then manually tweaked by searching for valid 
# words in the decrypted text.
MAPPING =  {
'2': ' ', 'O': 'e', '.': 't', 'I': 'a', 'c': 'o', 't': 'h',
'\x0c': 'r', 'K': 'n', '|': 'd', '>': 'i', 'E': 's', '-': 'l',
';': 'w', '\t': '\n', ' ': 'g', 'p': ',', 'F': 'u', 'Y': 'c',
'_': 'm', "'": 'y', 'e': 'f', 'X': 'p', 'W': '.', '<': 'b',
'V': 'k', '3': '"', 's': 'v', 'u': '-', 'R': "j", 'v': "'",
'f': '?', '{': 'q', '\n': ":"
}
# Convert to integer representation
MAPPING = {list(k.encode('utf8'))[0]: list(v.encode('utf8'))[0] for k, v in MAPPING.items()}


def sol1():
    with remote(URL, PORT) as conn:
        message = conn.recvuntil('-Pad')
        conn.sendline("1")
        conn.recvuntil(':')
        challenge = conn.recvline()

        # Decrypt the challenge here
        decrypter = MAPPING
        solution = bytes([decrypter[c] for c in challenge])
        print(solution.decode('utf8')[:200], '...\n')
        conn.send(solution)
        message = conn.recvline()
        message = conn.recvline()
        if b'Congratulations' in message:
            print(message)


def XOR(a, b):
    r = b''
    for x, y in zip(a, b):
        r += (x ^ y).to_bytes(1, 'big')
    return r


def sol2():
    # First connection to retrieve original message
    with remote(URL, PORT) as conn:
        conn.recvuntil('-Pad')  # receive TCP stream until end of menu
        conn.sendline("2")  # select challenge 2
        conn.recvuntil(':')
        challenge = conn.recvline()
        conn.send(challenge)
        conn.recvline()
        message = conn.recvline()

    # Determine OTP from ciphertext and plaintext
    key = XOR(challenge, message)

    # Encrypt modified message using calculated key
    with remote(URL, PORT) as conn:
        conn.recvuntil('-Pad')  # receive TCP stream until end of menu
        conn.sendline("2")  # select challenge 2
        conn.recvuntil(':')
        challenge = conn.recvline()
        solution = XOR(b"Student ID 1001781 gets 4 points\n", key)
        conn.send(solution)
        conn.recvline()
        message = conn.recvline()
        print(message)


if __name__ == "__main__":
    # NOTE: UPPERCASE names for constants is a (nice) Python convention
    URL = '34.239.117.115'
    PORT = 1337

    print("\n============ Challenge 1 ============\n")
    sol1()
    print("\n============ Challenge 2 ============\n")
    sol2()
