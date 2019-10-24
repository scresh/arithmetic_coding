from decoder import ArithmeticalDecoder
from encoder import ArithmeticEncoder


def main():
    # 1.  TODO: Add numba support
    # 2.  TODO: Replace with open('hamlet.txt').read()

    paragraph = 'ACBDEABCDABCACA'
    ae = ArithmeticEncoder(paragraph)
    lower_range, length, symbols_ranges = ae.encode()
    print(paragraph)

    print()
    print('\n'.join(str(lower_range).split('/')))
    print()
    print(symbols_ranges)

    ad = ArithmeticalDecoder(lower_range, length, symbols_ranges)
    decoded_content = ad.decode()
    print(decoded_content)


if __name__ == '__main__':
    main()
