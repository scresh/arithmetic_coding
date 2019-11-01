import math


class FileWriter:
    def __init__(self, filename):
        self.file = open(filename, 'wb+')

    @staticmethod
    def get_normalized_fraction(fraction, precision):
        max_number = 2 ** (8 * precision)
        return int(fraction * max_number)

    @staticmethod
    def get_precision(number):
        return math.ceil(math.log2(number + 1) / 8)

    def write_int(self, number_int, precision):
        number_bytes = number_int.to_bytes(precision, byteorder='big')
        self.file.write(number_bytes)

    def write(self, content_fraction, length, symbols_ranges):
        symbol_count = len(symbols_ranges)
        self.write_int(symbol_count - 1, 1)

        for symbol in symbols_ranges.keys():
            self.write_int(symbol, 1)

        ranges_start = [x[0] for x in symbols_ranges.values()]
        symbol_range_precision = self.get_precision((1 - ranges_start[-1]).denominator)
        self.write_int(symbol_range_precision, 1)

        for range_start in ranges_start:
            range_start_normalized = self.get_normalized_fraction(range_start, symbol_range_precision)
            self.write_int(range_start_normalized, symbol_range_precision)

        length_precision = self.get_precision(length)
        self.write_int(length_precision, 1)
        self.write_int(length, length_precision)

        numerator = content_fraction.numerator
        numerator_precision = self.get_precision(numerator) + 1
        numerator_precision_precision = self.get_precision(numerator_precision)
        numerator_normalized = self.get_normalized_fraction(content_fraction, numerator_precision)

        self.write_int(numerator_precision_precision, 1)
        self.write_int(numerator_precision, numerator_precision_precision)
        self.write_int(numerator_normalized, numerator_precision)
        self.file.close()
