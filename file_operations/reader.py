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

    def _get_ranges_starts(self, symbol_count):
        precision = self._read_int(1)
        denominator = 2 ** (8 * precision)

        numerators = [self._read_int(precision) for _ in range(symbol_count)]
        ranges_starts = [Fraction(numerator, denominator) for numerator in numerators]
        return ranges_starts

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
    def _get_symbols_dict(symbols, ranges_starts):
        ranges_thresholds = ranges_starts + [Fraction(1, 1)]
        symbols_dict = {}

        for i in range(len(symbols)):
            symbol_range_start = ranges_thresholds[i]
            symbol_range_delta = ranges_thresholds[i + 1] - ranges_thresholds[i]
            symbols_dict[symbols[i]] = (symbol_range_start, symbol_range_delta)

        return symbols_dict

    def read(self):
        symbols = self._read_symbols()
        ranges_starts = self._get_ranges_starts(symbol_count=len(symbols))
        symbols_dict = self._get_symbols_dict(symbols, ranges_starts)
        content_length = self._read_content_length()
        content_fraction = self._read_content_fraction()
        self.file.close()

        return content_fraction, content_length, symbols_dict
