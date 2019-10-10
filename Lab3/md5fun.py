#!/usr/bin/env python3
"""
Krishna Penukonda
1001781

Timings:
- hash5.txt: Generation 70.3s; Lookup 4.6s (Found 15/15)
- salt6.txt: Generation 68.5; Lookup 3.76s (Found 9/15)
"""
import string
import hashlib
import argparse
from time import time
from pathlib import Path
from random import shuffle, choice
from functools import lru_cache
from itertools import product


def md5hash(msg):
    return hashlib.md5(msg).hexdigest()


def get_rainbow_table(candidates):
    table = {md5hash(c): c for c in candidates}
    return table


def get_candidates(charset):
    characters = list(charset)
    shuffle(characters)
    characters = ''.join(characters).encode('utf8')
    candidates = map(bytes, product(characters, repeat=5))
    return candidates


def main(args):
    hash_file = Path('hash5.txt')
    pass_file = Path('pass5.txt')
    charset = string.ascii_lowercase + string.digits
    with open(hash_file, 'r') as f:
        hashes = [h.strip() for h in f.readlines()]

    if pass_file.exists():
        print("Passwords already cracked! Loading from file...")
        with open(pass_file, 'r') as f:
            passwords = [l.strip() for l in f.readlines()]
    else:
        start = time()
        # Candidate password generator
        candidates = get_candidates(charset)
        # Compute rainbow table
        table = get_rainbow_table(candidates)
        print(f"Rainbow time: {time() - start}s")
        # Lookup passwords in generated rainbow table
        passwords = [table[h].decode('utf-8') for h in hashes]

        # Save passwords to file
        with open(pass_file, 'w') as f:
            for h, p in zip(hashes, passwords):
                f.write(f"{p}\n")
    for h, p in zip(hashes, passwords):
        print(f"{h} -> {p}")

    if args.salt:
        # Append random character to each password (salt)
        salted = [p + choice(charset) for p in passwords]
        # Save salted passwords
        salted_pass_file = Path('pass6.txt')
        with open(salted_pass_file, 'w') as f:
            for p in salted:
                f.write(f"{p}\n")
        # Hash salted passwords
        salted_hashed = [md5hash(p.encode('utf-8')) for p in salted]
        # Save hashsed salted passwords
        salted_hash_file = Path('salt6.txt')
        with open(salted_hash_file, 'w') as f:
            for p in salted_hashed:
                f.write(f"{p}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--salt', action='store_true')
    args = parser.parse_args()
    main(args)
