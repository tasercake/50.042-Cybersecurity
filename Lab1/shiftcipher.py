#!/usr/bin/env python3
# Krishna Penukonda - 1001781
import sys
import argparse
import string


def validate_mode(mode):
    assert isinstance(mode, str)
    return mode.lower()


def validate_key(key):
    key = int(key)
    assert key < len(string.printable)
    return key


def main(filein, fileout, key, mode):
    chars = string.printable
    with open(filein, mode='r', encoding='utf-8', newline='\n') as fin:
        strin = fin.read()

    if mode == 'd':
        key = -key
    indices = [chars.index(char) for char in strin]
    new_indices = [(i + key) % len(chars) for i in indices]

    with open(fileout, mode='w', encoding='utf-8', newline='\n') as fout:
        fout.write(''.join([chars[i] for i in new_indices]))
    # fin_b = open(filein, mode='rb')  # binary read mode
    # fout_b = open(fileout, mode='wb')  # binary write mode


# our main function
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
