import unittest

from puzzles.Day19.day19 import part1, part2
from test.TestConfig import TestConfig


class Day19Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 1413)

    def test_part2(self):
        self.assertEqual(part2(), 21080)