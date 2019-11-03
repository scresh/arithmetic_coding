from fractions import Fraction
from tqdm import tqdm
from hashlib import md5
import math


class ArithmeticEncoder:
    def __init__(self, content):
        self.content = content

    def get_symbol_probability(self, symbol):
        content_len = len(self.content)
        symbol_count = self.content.count(symbol)
        symbol_probability = Fraction(symbol_count, content_len)
        return symbol_probability

    def get_symbol_probabilities(self):
        symbols = [*set(self.content)]
        pairs = [[s, self.get_symbol_probability(s)] for s in symbols]
        pairs = sorted(pairs, key=lambda x: x[1], reverse=True)
        return pairs

    @staticmethod
    def get_floor_quantized_probability(probability):
        floor_exponent = abs(math.floor(math.log2(probability)))
        return Fraction(1, 2**floor_exponent)

    def get_floor_quantized_probabilities(self, symbol_probabilities):
        pairs = [[s, self.get_floor_quantized_probability(p)] for s, p in symbol_probabilities]
        return pairs

    @staticmethod
    def get_probabilities_sum(symbol_probabilities):
        return sum([x[1] for x in symbol_probabilities])

    @staticmethod
    def optimize_symbol_probabilities(symbol_probabilities, stock_floor):
        for i in range(len(symbol_probabilities)):
            probability = symbol_probabilities[i][1]
            if probability <= stock_floor:
                symbol_probabilities[i][1] *= 2
                break

    def get_optimized_probabilities(self, symbol_probabilities):
        probabilities_sum = self.get_probabilities_sum(symbol_probabilities)

        while probabilities_sum < 1.0:
            stock = Fraction(1, 1) - probabilities_sum
            stock_floor = self.get_floor_quantized_probability(stock)

            self.optimize_symbol_probabilities(symbol_probabilities, stock_floor)
            probabilities_sum = self.get_probabilities_sum(symbol_probabilities)

        return symbol_probabilities

    def get_optimal_quantized_probabilities(self):
        symbol_probabilities = self.get_symbol_probabilities()
        symbol_probabilities = self.get_floor_quantized_probabilities(symbol_probabilities)
        symbol_probabilities = self.get_optimized_probabilities(symbol_probabilities)

        return symbol_probabilities

    def get_symbols_ranges(self):
        pairs = self.get_optimal_quantized_probabilities()

        recent_range = Fraction(0, 1)
        symbol_ranges = {}

        for pair in pairs:
            symbol, probability = pair

            range_start = recent_range
            range_end = range_start + probability
            recent_range = range_end

            symbol_ranges[symbol] = (range_start, range_end)

        return symbol_ranges

    def encode(self):
        content_md5 = md5(self.content).hexdigest()
        print(f'Input file MD5 sum: {content_md5}')
        symbols_ranges = self.get_symbols_ranges()

        current_range = (Fraction(0, 1), Fraction(1, 1))

        for c in tqdm(self.content, desc='Encoding'):
            symbol_range_start, symbol_range_stop = symbols_ranges[c]

            current_range_start, current_range_end = current_range
            current_range_delta = current_range_end - current_range_start

            new_range_start = current_range_start + (current_range_delta * symbol_range_start)
            new_range_stop = current_range_start + (current_range_delta * symbol_range_stop)

            current_range = (new_range_start, new_range_stop)

        return current_range[0], len(self.content), symbols_ranges

