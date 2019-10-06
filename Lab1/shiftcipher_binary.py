#!/usr/bin/env python3
# Krishna Penukonda - 1001781
import sys
import argparse
import string


# validate CLI inputs
def validate_mode(mode):
    return mode.lower()


def validate_key(key):
    key = int(key)
    assert 0 <= key < 255
    return key


def main(filein, fileout, key, mode):
    with open(filein, mode='rb') as fin:
        inp = fin.read()
    if mode == 'd':
        key = -key
    out = bytearray([(i + key) % 256 for i in inp])
    with open(fileout, mode='wb') as fout:
        fout.write(out)


if __name__=="__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein', help='input file', required=True)
    parser.add_argument('-o', dest='fileout', help='output file', required=True)
    parser.add_argument('-k', dest='key', help='cipher key', required=True, type=validate_key)
    parser.add_argument('-m', dest='mode', help='cipher mode', choices=['e', 'E', 'd', 'D'], required=True, type=validate_mode)

    # parse our arguments
    args = parser.parse_args()
    filein=args.filein
    fileout=args.fileout
    key = args.key
    mode = args.mode

    main(filein, fileout, key, mode)
