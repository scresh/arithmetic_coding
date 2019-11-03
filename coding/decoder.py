from fractions import Fraction
from tqdm import trange
from hashlib import md5


class ArithmeticalDecoder:
    def __init__(self, content_fraction, content_length, pairs_dict):
        self.content_fraction = content_fraction
        self.content_length = content_length
        self.pairs_dict = pairs_dict

    def get_new_pair(self, current_range):
        current_range_start, current_range_end = current_range
        current_range_delta = current_range_end - current_range_start

        for symbol, symbol_range in self.pairs_dict.items():
            symbol_range_start, symbol_range_end = symbol_range

            new_range_start = current_range_start + (current_range_delta * symbol_range_start)
            new_range_end = current_range_start + (current_range_delta * symbol_range_end)

            if new_range_start <= self.content_fraction < new_range_end:
                return symbol, (new_range_start, new_range_end)

    def decode(self):
        content = bytearray()
        current_range = (Fraction(0, 1), Fraction(1, 1))

        for _ in trange(self.content_length, desc='Decoding'):
            new_symbol, new_range = self.get_new_pair(current_range)

            content.append(new_symbol)
            current_range = new_range

        content_md5 = md5(content).hexdigest()
        print(f'Input file MD5 sum: {content_md5}')

        return content
