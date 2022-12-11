from collections import defaultdict


def sorted_str(s):
    return ''.join(sorted(s))


def string_contains_as_set(a, b):
    return all([x in a for x in b])


def extract_letter_frequencies(string):
    letter_frequencies = defaultdict(int)
    for pattern in string:
        for c in pattern:
            letter_frequencies[c] += 1
    return letter_frequencies
