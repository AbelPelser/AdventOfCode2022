import unittest

from puzzles.Day17.day17 import part1, part2
from test.TestConfig import TestConfig


class Day17Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 3071)

    def test_part2(self):
        self.assertEqual(part2(), 1523615160362)