# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (C) 2019 Intel Corporation.  All rights reserved.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#

from .context import wamr

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    # TBD: not sure what kind of test cases should be here
    def test_case_1(self):
        self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
