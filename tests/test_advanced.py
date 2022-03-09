# -*- coding: utf-8 -*-

from .context import wamr

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    # TBD: not sure what kind of test cases should be here
    def test_case_1(self):
        self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
