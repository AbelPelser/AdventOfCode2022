import sys
import unittest

from puzzles.Day2.day2 import part1, part2
from test.TestConfig import TestConfig


class Day2Test(TestConfig, unittest.TestCase):
    def test_day2_part1(self):
        import os
        print(os.getcwd(), file=sys.stderr)
        self.assertEqual(part1(), 496)

    def test_day2_part2(self):
        self.assertEqual(part2(), 847)
