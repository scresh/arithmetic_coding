#!/usr/bin/env python

import argparse
from coding.encoder import ArithmeticEncoder
from coding.decoder import ArithmeticalDecoder
from file_operations.reader import FileReader
from file_operations.writer import FileWriter


def compress(file_in, file_out):
    with open(file_in, 'rb') as f:
        content = f.read()

    ae = ArithmeticEncoder(content)
    content_fraction, length, symbols_ranges = ae.encode()

    fw = FileWriter(file_out)
    fw.write(content_fraction, length, symbols_ranges)


def decompress(file_in, file_out):
    fr = FileReader(file_in)
    content_fraction, length, symbols_ranges = fr.read()

    ad = ArithmeticalDecoder(content_fraction, length, symbols_ranges)
    decoded_content = ad.decode()

    with open(file_out, 'wb') as f:
        f.write(decoded_content)


def main():
    action_dict = dict(compress=compress, decompress=decompress)
    parser = argparse.ArgumentParser(description='Compress/Decompress files using arithmetic coding algorithm.')
    parser.add_argument('action', choices=action_dict.keys())
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()

    action = args.action
    params = [args.input, args.output]
    action_dict[action](*params)


if __name__ == '__main__':
    main()
