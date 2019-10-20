from fractions import Fraction


class ArithmeticalDecoder:
    def __init__(self, lower_range, length, symbols_ranges):
        self.lower_range = lower_range
        self.length = length
        self.symbols_ranges = symbols_ranges

    def decode(self):
        content = ''
        current_range = (Fraction(0, 1), Fraction(1, 1))

        for _ in range(self.length):
            current_start_range, current_stop_range = current_range
            current_delta = current_stop_range - current_start_range

            try:
                symbol_range = [*filter(
                    lambda x:
                    x[1][0] * current_delta <= self.lower_range - current_start_range < x[1][1] * current_delta,
                    self.symbols_ranges)][0]
            except IndexError:
                return content

            symbol = symbol_range[0]

            symbol_start_range, symbol_stop_range = symbol_range[1]

            new_start_range = current_start_range + symbol_start_range * current_delta
            new_stop_range = current_start_range + symbol_stop_range * current_delta

            current_range = (new_start_range, new_stop_range)

            content += symbol

        return content
