from fractions import Fraction


class FileReader:
    def __init__(self, filename):
        self.file = open(filename, 'rb')

    def _read_int(self, precision):
        return int.from_bytes(self.file.read(precision), byteorder='big')

    def _read_symbols(self):
        symbol_count = self._read_int(1) + 1
        symbols = [self._read_int(1) for _ in range(symbol_count)]
        return symbols

    def _read_ranges(self, symbol_count):
        symbol_range_precision = self._read_int(1)
        denominator = 2 ** (8 * symbol_range_precision)

        numerators = [self._read_int(symbol_range_precision) for _ in range(symbol_count)]
        ranges = [Fraction(numerator, denominator) for numerator in numerators] + [Fraction(1, 1)]
        return ranges

    def _read_content_length(self):
        content_length_precision = self._read_int(1)
        content_length = self._read_int(content_length_precision)
        return content_length

    def _read_content_fraction(self):
        numerator_precision_precision = self._read_int(1)
        numerator_precision = self._read_int(numerator_precision_precision)
        numerator_normalized = self._read_int(numerator_precision)

        content_fraction = Fraction(numerator_normalized, 2 ** (8 * numerator_precision))
        return content_fraction

    @staticmethod
    def get_symbols_ranges(symbols, ranges):
        symbol_count = len(symbols)
        symbol_ranges = {symbols[i]: (ranges[i], ranges[i + 1]) for i in range(symbol_count)}
        return symbol_ranges

    def read(self):
        symbols = self._read_symbols()
        ranges = self._read_ranges(symbol_count=len(symbols))
        symbols_ranges = self.get_symbols_ranges(symbols, ranges)
        content_length = self._read_content_length()
        content_fraction = self._read_content_fraction()
        self.file.close()

        return content_fraction, content_length, symbols_ranges
