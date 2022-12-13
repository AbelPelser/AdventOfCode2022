import unittest

from puzzles.Day13.day13 import part1, part2
from test.TestConfig import TestConfig


class Day13Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 5808)

    def test_part2(self):
        self.assertEqual(part2(), 22713)