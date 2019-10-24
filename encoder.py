from fractions import Fraction
import itertools as it
import math
from functools import reduce


class ArithmeticEncoder:
    def __init__(self, content):
        self.content = content

    def get_symbol_probabilities(self):
        content_len = len(self.content)
        symbols = [*set(self.content)]

        pairs = []

        for symbol in symbols:
            symbol_count = self.content.count(symbol)
            symbol_probability = Fraction(symbol_count, content_len)
            pairs.append((symbol, symbol_probability))

        pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

        return pairs

    @staticmethod
    def get_list_elements_product_denominator(input_list):
        return reduce((lambda x, y: x * y), input_list).denominator

    @staticmethod
    def get_quantized_floor_probability(probability):
        floor_exponent = abs(math.floor(math.log2(probability)))
        return Fraction(1, 2**floor_exponent)

    @staticmethod
    def get_quantized_ceil_probability(probability):
        ceil_exponent = abs(math.ceil(math.log2(probability)))
        return Fraction(1, 2**ceil_exponent)

    def get_optimal_quantized_probabilities(self):
        symbol_probabilities = self.get_symbol_probabilities()
        quantized_probability_pairs = []
        symbols = []

        for symbol, symbol_probability in symbol_probabilities:
            probability_floor = self.get_quantized_floor_probability(symbol_probability)
            probability_ceil = self.get_quantized_ceil_probability(symbol_probability)
            quantized_probability_pairs.append((probability_floor, probability_ceil))
            symbols.append(symbol)

        quantized_probabilities_cartesian_product = it.product(*quantized_probability_pairs)

        quantized_probabilities_cartesian_product = filter(
            lambda p: sum(p) <= Fraction(1, 1),
            quantized_probabilities_cartesian_product
        )

        optimal_quantized_probability = sorted(
            quantized_probabilities_cartesian_product,
            key=self.get_list_elements_product_denominator,
        )[0]

        return zip(symbols, optimal_quantized_probability)

    def get_symbols_ranges(self):
        pairs = self.get_optimal_quantized_probabilities()

        recent_range = Fraction(0, 1)
        symbol_ranges = {}

        for pair in pairs:
            symbol, probability = pair

            start_range = recent_range
            stop_range = start_range + probability
            recent_range = stop_range

            symbol_ranges[symbol] = (start_range, stop_range)

        return symbol_ranges

    def encode(self):
        symbols_ranges = self.get_symbols_ranges()

        current_range = (Fraction(0, 1), Fraction(1, 1))

        for c in self.content:
            symbol_start_range, symbol_stop_range = symbols_ranges[c]

            current_start_range, current_stop_range = current_range
            current_delta = current_stop_range - current_start_range

            new_start_range = current_start_range + symbol_start_range * current_delta
            new_stop_range = current_start_range + symbol_stop_range * current_delta

            current_range = (new_start_range, new_stop_range)

        symbols_ranges = sorted([x for x in symbols_ranges.items()], key=lambda x: x[0][0])
        return current_range[0], len(self.content), symbols_ranges
