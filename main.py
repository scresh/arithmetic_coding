from decoder import ArithmeticalDecoder
from encoder import ArithmeticEncoder
from reader import FileReader
from writer import FileWriter


def main():
    content = open('hamlet.txt', 'rb').read()
    ae = ArithmeticEncoder(content)
    content_fraction, length, symbols_ranges = ae.encode()

    fw = FileWriter('hamlet.ae')
    fw.write(content_fraction, length, symbols_ranges)

    fr = FileReader('hamlet.ae')
    content_fraction, length, symbols_ranges = fr.read()

    ad = ArithmeticalDecoder(content_fraction, length, symbols_ranges)
    decoded_content = ad.decode()

    open('HAMLET.txt', 'wb').write(decoded_content)


if __name__ == '__main__':
    main()
