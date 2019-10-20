from decoder import ArithmeticalDecoder
from encoder import ArithmeticEncoder


def main():
    # TODO: Replace with open('hamlet.txt').read()
    paragraph = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the ' \
                'industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type ' \
                'and scrambled it to make a type specimen book. It has survived not only five centuries, but also the ' \
                'leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s ' \
                'with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop ' \
                'publishing software like Aldus PageMaker including versions of Lorem Ipsum. '

    ae = ArithmeticEncoder(paragraph)
    lower_range, length, symbols_ranges = ae.encode()
    print(paragraph)

    ad = ArithmeticalDecoder(lower_range, length, symbols_ranges)
    decoded_content = ad.decode()
    print(decoded_content)


if __name__ == '__main__':
    main()
