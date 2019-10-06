#!/usr/bin/env python3
# Krishna Penukonda - 1001781
import subprocess
import sys
import argparse
import string


def main(filein, fileout, types):
    with open(filein, mode='rb') as fin:
        inp = fin.read()
    found = False
    for key in range(255):
        key = -key
        out = bytearray([(i + key) % 256 for i in inp])
        with open('temp', mode='wb') as temp:
            temp.write(out)
        result = subprocess.check_output(['file', 'temp'], encoding='utf8')
        if result:
            result = result.lower()
            for t in types:
                t = t.lower()
                if t in result:
                    if found:
                        print("Warning: multiple matches. Output may not be as expected.")
                    print("Found match '{}' using key={}".format(t, -key))
                    found = True
                    with open(fileout, mode='wb') as fout:
                        fout.write(out)
    if not found:
        print("No recognisable file type could be decrypted :(")


if __name__=="__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein', help='input file', required=True)
    parser.add_argument('-o', dest='fileout', help='output file', required=True)
    parser.add_argument('-t', dest='types', help='filetypes to accept as decrypted', nargs='*', default=['png'])

    # parse our arguments
    args = parser.parse_args()
    filein=args.filein
    fileout=args.fileout
    types = args.types

    main(filein, fileout, types)
