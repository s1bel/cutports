# 2024-11-13.001

import re
import itertools

DEFAULT_START_PORT = 0
DEFAULT_END_PORT = 65535


def group_consecutive_numbers(numbers):
    """Yield tuples of consecutive numbers in the input sequence.

    This function takes an iterable of numbers and yields tuples of
    consecutive numbers. The tuples contain the start and end of the
    sequence of consecutive numbers.

    Example:

    >>> list(group_consecutive_numbers([1, 2, 3, 4, 5, 6, 7, 8, 10]))
    [(1, 8), (10, 10)]
    """
    for _, group in itertools.groupby(enumerate(numbers), key=lambda pair: pair[1] - pair[0]):
        group_list = list(group)
        # The first element of the group contains the start of the sequence
        start = group_list[0][1]
        # The last element of the group contains the end of the sequence
        end = group_list[-1][1]
        yield start, end


def parse_ports_range(input_string):
    """Parses a string into a set of numbers representing a range of ports.

    If the input string is empty, it returns a set of numbers from
    DEFAULT_START_PORT to DEFAULT_END_PORT.

    Example:

    >>> parse_ports_range('1-10')
    {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    """
    if not input_string:
        return set(range(DEFAULT_START_PORT, DEFAULT_END_PORT + 1))

    # Check that the input string is a valid range of numbers
    try:
        start, end = input_string.split('-')
        if not start.isdigit() or not end.isdigit():
            raise ValueError("Начальный порт и конечный порт должны быть числами.")
        start = int(start)
        end = int(end)

        # Check that the start and end ports are within the valid range
        if start < DEFAULT_START_PORT:
            raise ValueError(f"Начальный порт должен быть больше {DEFAULT_START_PORT}.")
        if end > DEFAULT_END_PORT:
            raise ValueError(f"Конечный порт должен быть меньше {DEFAULT_END_PORT}.")
        if start >= end:
            raise ValueError("Начальный порт должен быть меньше конечного порта.")
    except ValueError as e:
        raise ValueError("Некорректный ввод. Введите диапазон портов в формате '1-10500'.") from e

    # Return a set of numbers representing the range of ports
    return set(range(start, end + 1))

def parse_cut_ports(input_string):
    """Parses a string of space or comma separated numbers and/or ranges into a set of numbers.

    Example:

    >>> parse_cut_ports('1,2,3,10-15')
    {1, 2, 3, 10, 11, 12, 13, 14, 15}

    The input string can contain any number of space or comma separated numbers and/or ranges.
    The numbers can be in any order.

    The function returns a set of numbers representing the parsed range of ports.
    """
    parts = re.split(r'[ ,]+', input_string)
    ports = set()

    for part in parts:
        # Check if the part is a range
        match = re.match(r'(\d+)-(\d+)', part)
        if match:
            first = int(match.group(1))
            last = int(match.group(2))
            # Check that the start of the range is not greater than the end of the range
            if first > last:
                raise ValueError("Некорректный ввод. Начальный порт в диапазоне не может быть больше конечного порта.")
            # Add the range to the set of ports
            ports.update(range(first, last + 1))
        else:
            # Check that the part is a number
            if part.isdigit():
                ports.add(int(part))
            else:
                # Raise an error if the part is not a number or a range
                raise ValueError("Некорректный ввод. Допускаются только числа и диапазоны.")

    return ports

def main():
    """Main entry point."""
    input_range = input(f"Введите начальный диапазон портов в формате '1-10500' (по-умолчанию {DEFAULT_START_PORT}-{DEFAULT_END_PORT}): ")
    cut_range = parse_ports_range(input_range)

    cutted_ports_range = input("Введите номера портов или диапазоны в формате '1-10500' через пробел или запятую: ")
    cut_ports = parse_cut_ports(cutted_ports_range)

    result_set = list(cut_range - cut_ports)
    print(repr(','.join(['%d' % s if s == e else '%d-%d' % (s, e) for (s, e) in group_consecutive_numbers(result_set)])))


if __name__ == "__main__":
    main()

