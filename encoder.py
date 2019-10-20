from fractions import Fraction


class ArithmeticEncoder:
    def __init__(self, content):
        self.content = content

    def get_symbols_ranges(self):
        content_len = len(self.content)
        symbols = [*set(self.content)]

        pairs = []

        for symbol in symbols:
            symbol_count = self.content.count(symbol)
            symbol_probability = Fraction(symbol_count, content_len)
            pairs.append((symbol, symbol_probability))

        pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

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
