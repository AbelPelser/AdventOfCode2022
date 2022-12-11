import unittest

from puzzles.Day24.day24 import part1, part2
from test.TestConfig import TestConfig


class Day24Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), None)

    def test_part2(self):
        self.assertEqual(part2(), None)