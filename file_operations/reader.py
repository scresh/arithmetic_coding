from fractions import Fraction


class FileReader:
    def __init__(self, filename):
        self.file = open(filename, 'rb')

    def _read_int(self, precision):
        return int.from_bytes(self.file.read(precision), byteorder='big')

    def read(self):
        symbol_count = self._read_int(1) + 1
        symbols = [self._read_int(1) for _ in range(symbol_count)]

        symbol_range_precision = self._read_int(1)
        denominator = 2 ** (8 * symbol_range_precision)

        numerators = [self._read_int(symbol_range_precision) for _ in range(symbol_count)]
        ranges = [Fraction(numerator, denominator) for numerator in numerators] + [Fraction(1, 1)]

        symbol_ranges = {symbols[i]: (ranges[i], ranges[i+1]) for i in range(symbol_count)}

        length_precision = self._read_int(1)
        length = self._read_int(length_precision)

        numerator_precision_precision = self._read_int(1)
        numerator_precision = self._read_int(numerator_precision_precision)
        numerator_normalized = self._read_int(numerator_precision)

        content_fraction = Fraction(numerator_normalized, 2 ** (8 * numerator_precision))

        self.file.close()
        return content_fraction, length, symbol_ranges
