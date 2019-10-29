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
            pairs.append([symbol, symbol_probability])

        pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

        return pairs

    @staticmethod
    def get_floor_quantized_probability(probability):
        floor_exponent = abs(math.floor(math.log2(probability)))
        return Fraction(1, 2**floor_exponent)

    def get_floor_quantized_probabilities(self, symbol_probabilities):
        pairs = []

        for symbol, symbol_probability in symbol_probabilities:
            floor_quantized_probability = self.get_floor_quantized_probability(symbol_probability)
            pairs.append([symbol, floor_quantized_probability])

        return pairs

    @staticmethod
    def get_probabilities_sum(symbol_probabilities):
        return sum([x[1] for x in symbol_probabilities])

    def optimize_probabilities(self, symbol_probabilities):
        probabilities_sum = self.get_probabilities_sum(symbol_probabilities)

        while probabilities_sum < 1:
            stock = Fraction(1, 1) - probabilities_sum
            stock_floor = self.get_floor_quantized_probability(stock)

            double_candidate = [*filter(lambda x: x[1] <= stock_floor, symbol_probabilities)][0]
            double_candidate_index = symbol_probabilities.index(double_candidate)
            symbol_probabilities[double_candidate_index][1] *= 2
            probabilities_sum = self.get_probabilities_sum(symbol_probabilities)

        return symbol_probabilities

    def get_optimal_quantized_probabilities(self):
        symbol_probabilities = self.get_symbol_probabilities()
        symbol_probabilities = self.get_floor_quantized_probabilities(symbol_probabilities)
        symbol_probabilities = self.optimize_probabilities(symbol_probabilities)

        return symbol_probabilities

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
