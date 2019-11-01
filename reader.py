from fractions import Fraction


class FileReader:
    def __init__(self, filename):
        self.file = open(filename, 'rb')

    def read(self):
        symbol_count = int.from_bytes(self.file.read(1), byteorder='big') + 1

        symbols = []

        for _ in range(symbol_count):
            symbols.append(int.from_bytes(self.file.read(1), byteorder='big'))

        symbol_range_precision = int.from_bytes(self.file.read(1), byteorder='big')

        ranges_start = []
        for _ in range(symbol_count):
            range_start = Fraction(
                int.from_bytes(self.file.read(symbol_range_precision), byteorder='big'),
                2 ** (8 * symbol_range_precision)
            )
            ranges_start.append(range_start)

        ranges_start.append(Fraction(1, 1))

        symbol_ranges = {}

        for i in range(symbol_count):
            symbol = symbols[i]
            symbol_range_start = ranges_start[i]
            symbol_range_end = ranges_start[i+1]
            symbol_ranges[symbol] = (symbol_range_start, symbol_range_end)

        length_precision = int.from_bytes(self.file.read(1), byteorder='big')
        length = int.from_bytes(self.file.read(length_precision), byteorder='big')

        numerator_precision_precision = int.from_bytes(self.file.read(1), byteorder='big')
        numerator_precision = int.from_bytes(self.file.read(numerator_precision_precision), byteorder='big')
        numerator_normalized = int.from_bytes(self.file.read(numerator_precision), byteorder='big')

        content_fraction = Fraction(numerator_normalized, 2 ** (8 * numerator_precision))

        self.file.close()
        return content_fraction, length, symbol_ranges
