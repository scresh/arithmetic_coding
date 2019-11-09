from bisect import bisect_right
from tqdm import trange
from hashlib import md5
from termcolor import cprint


class ArithmeticalDecoder:
    def __init__(self, content_fraction, content_length, symbol_dict):
        self.content_fraction = content_fraction
        self.content_length = content_length
        self.symbols_dict = symbol_dict
        self.symbols = tuple(symbol_dict.keys())
        self.ranges_starts = tuple([x[0] for x in symbol_dict.values()])

    def get_new_symbol(self):
        symbol_index = bisect_right(self.ranges_starts, self.content_fraction) - 1
        symbol = self.symbols[symbol_index]
        symbol_range_start, symbol_range_delta = self.symbols_dict[symbol]

        self.content_fraction = (self.content_fraction - symbol_range_start) / symbol_range_delta
        return symbol

    def decode(self):
        content = bytearray()

        for _ in trange(self.content_length, desc='Decoding'):
            new_symbol = self.get_new_symbol()
            content.append(new_symbol)

        content_md5 = md5(content).hexdigest()
        cprint(f'Output file MD5 sum: {content_md5}', 'yellow')

        return content
