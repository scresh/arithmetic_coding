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

    def get_symbols_probabilities(self):
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
    def optimize_symbols_probabilities(symbol_probabilities, stock_floor):
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

            self.optimize_symbols_probabilities(symbol_probabilities, stock_floor)
            probabilities_sum = self.get_probabilities_sum(symbol_probabilities)

        return symbol_probabilities

    def get_optimal_quantized_probabilities(self):
        symbol_probabilities = self.get_symbols_probabilities()
        symbol_probabilities = self.get_floor_quantized_probabilities(symbol_probabilities)
        symbol_probabilities = self.get_optimized_probabilities(symbol_probabilities)

        return symbol_probabilities

    def get_symbols_dict(self):
        pairs = self.get_optimal_quantized_probabilities()

        recent_range_stop = Fraction(0, 1)
        symbols_dict = {}

        for symbol, probability in pairs:
            symbol_range_start = recent_range_stop
            symbol_range_delta = probability

            symbols_dict[symbol] = (symbol_range_start, symbol_range_delta)
            recent_range_stop = symbol_range_start + symbol_range_delta

        return symbols_dict

    def encode(self):
        content_md5 = md5(self.content).hexdigest()
        print(f'Input file MD5 sum: {content_md5}')
        symbols_dict = self.get_symbols_dict()

        current_range_start = Fraction(0, 1)
        current_range_delta = Fraction(1, 1)

        for c in tqdm(self.content, desc='Encoding'):
            symbol_range_start, symbol_range_delta = symbols_dict[c]

            current_range_start += (current_range_delta * symbol_range_start)
            current_range_delta *= symbol_range_delta

        return current_range_start, len(self.content), symbols_dict
