# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import TestCase, main
from datetime import datetime

import platemap as pm


@pm.util.rollback_tests()
class TestWebHelpers(TestCase):
    def test_get_extraction_plates(self):
        obs = pm.webhelp.get_extraction_plates()
        exp = [['000000003', 'Test plate 1', 2, datetime(2016, 2, 28, 0, 0)]]
        self.assertEqual(obs, exp)


if __name__ == '__main__':
    main()
