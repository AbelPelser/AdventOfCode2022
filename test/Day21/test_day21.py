import unittest

from puzzles.Day21.day21 import part1, part2
from test.TestConfig import TestConfig


class Day21Test(TestConfig, unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(), 286698846151845)

    def test_part2(self):
        self.assertEqual(part2(), 3759566892641)