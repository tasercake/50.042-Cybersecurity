#!/usr/bin/env python3
import string
import hashlib
import argparse
from time import time
from random import shuffle
from functools import lru_cache
from itertools import product
from multiprocessing import Pool


def md5hash(msg):
    return msg, hashlib.md5(msg).hexdigest()


def get_rainbow_table(candidates):
    table = {}
    # table = {md5hash(c): c for c in candidates}
    pool = Pool()
    for c, h in pool.imap_unordered(md5hash, candidates, chunksize=1024):
        table[h] = c
    return table


def get_candidates():
    characters = list((string.ascii_lowercase + string.digits))
    shuffle(characters)
    characters = ''.join(characters).encode('utf8')
    candidates = map(bytes, product(characters, repeat=5))
    return candidates


def crack(md5):
    for c in get_candidates():
        h = hashlib.md5(c).hexdigest()
        if h == md5:
            return c
    print(f"No matching password for {md5}")


def main(args):
    with open(args.file, 'r') as file:
        hashes = [h.strip() for h in file.readlines()]
    start = time()    
    candidates = get_candidates()
    table = get_rainbow_table(candidates)
    print(f"Rainbow: {time() - start}s")

    start = time()
    messages = [table[h] for h in hashes]    
    print(messages)
    print(f"Lookup time: {time() - start}s")

    # pool = Pool()
    # messages = pool.imap(crack, hashes)
    # for i, m in enumerate(messages):
    #     elapsed = time() - start
    #     print(f"{i + 1}: Found hash({m}) at t={elapsed:.3f}s")
    # print(f"Cracked {len(hashes)} hashes in {elapsed:.3f}s")
    # print(dict(zip(messages, hashes)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    main(args)
