import unittest

from puzzles.Day6.day6 import part1, part2
from test.TestConfig import TestConfig


class Day6Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), None)

    def test_part2(self):
        self.assertEqual(part2(), None)