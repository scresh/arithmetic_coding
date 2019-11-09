import math


class FileWriter:
    def __init__(self, filename):
        self.file = open(filename, 'wb+')

    @staticmethod
    def _get_normalized_fraction(fraction, precision):
        max_number = 2 ** (8 * precision)
        return int(fraction * max_number)

    @staticmethod
    def _get_precision(number):
        return math.ceil(math.log2(number + 1) / 8)

    def _write_int(self, number_int, precision):
        number_bytes = number_int.to_bytes(precision, byteorder='big')
        self.file.write(number_bytes)

    def _write_symbols(self, symbols_ranges):
        symbol_count = len(symbols_ranges)
        self._write_int(symbol_count - 1, 1)

        for symbol in symbols_ranges.keys():
            self._write_int(symbol, 1)

    def _write_ranges_start(self, symbols_dict):
        ranges_start = [x[0] for x in symbols_dict.values()]
        symbol_range_precision = self._get_precision((1 - ranges_start[-1]).denominator)
        self._write_int(symbol_range_precision, 1)

        for range_start in ranges_start:
            range_start_normalized = self._get_normalized_fraction(range_start, symbol_range_precision)
            self._write_int(range_start_normalized, symbol_range_precision)

    def _write_content_length(self, content_length):
        content_length_precision = self._get_precision(content_length)
        self._write_int(content_length_precision, 1)
        self._write_int(content_length, content_length_precision)

    def _write_content_fraction(self, content_fraction):
        numerator = content_fraction.numerator
        numerator_precision = self._get_precision(numerator) + 1
        numerator_precision_precision = self._get_precision(numerator_precision)
        numerator_normalized = self._get_normalized_fraction(content_fraction, numerator_precision)

        self._write_int(numerator_precision_precision, 1)
        self._write_int(numerator_precision, numerator_precision_precision)
        self._write_int(numerator_normalized, numerator_precision)

    def write(self, content_fraction, content_length, symbols_dict):
        self._write_symbols(symbols_dict)
        self._write_ranges_start(symbols_dict)
        self._write_content_length(content_length)
        self._write_content_fraction(content_fraction)
        self.file.close()
