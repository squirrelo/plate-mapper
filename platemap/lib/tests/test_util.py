# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import TestCase, main
from platemap.lib.util import (
    check_barcode_assigned, convert_from_id, convert_to_id, get_count,
    rollback_tests)


class TestUtil(TestCase):
    def test_convert_to_id(self):
        obs = convert_to_id('Project 2', 'project')
        self.assertEqual(obs, 2)

    def test_convert_to_id_no_exist(self):
        with self.assertRaises(LookupError):
            convert_to_id('NOTREALPROJECT', 'project')

        with self.assertRaises(ValueError):
            convert_to_id('Project 2', 'BADTABLE')

    def test_convert_from_id(self):
        obs = convert_from_id(2, 'project')
        self.assertEqual(obs, 'Project 2')

    def test_convert_from_id_no_exist(self):
        with self.assertRaises(LookupError):
            convert_from_id(12, 'project')

        with self.assertRaises(ValueError):
            convert_from_id(2, 'BADTABLE')

    def test_get_count(self):
        obs = get_count('project')
        self.assertEqual(obs, 3)

    def test_get_count_bad_table(self):
        with self.assertRaises(ValueError):
            get_count('BADTABLE')

    def test_check_barcode_assigned(self):
        obs = check_barcode_assigned('000000001')
        self.assertTrue(obs)

        obs = check_barcode_assigned('000000010')
        self.assertFalse(obs)

    def test_check_barcode_assigned_no_exist(self):
        with self.assertRaises(ValueError):
            check_barcode_assigned('100000001')

    def test_rollback_tests(self):
        @rollback_tests()
        class TestClass(TestCase):
            def testfunc():
                pass


if __name__ == '__main__':
    main()
