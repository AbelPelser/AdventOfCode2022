import unittest

from puzzles.Day15.day15 import part1, part2
from test.TestConfig import TestConfig


class Day15Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 5838453)

    def test_part2(self):
        self.assertEqual(part2(), 12_413_999_391_794)
