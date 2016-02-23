from unittest import TestCase, main
from platemap.lib.util import (
    check_barcode_assigned, convert_from_id, convert_to_id, get_count,
    rollback_tests)
from platemap.lib.sql_connection import TRN


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
        # Create decorated test function that adds a table
        @rollback_tests()
        def testfunc():
            with TRN:
                sql = 'CREATE TABLE barcodes.rollback(test varchar NOT NULL)'
                TRN.add(sql)
                TRN.execute()

        # Make sure that table does not exist once function completes
        testfunc()
        with TRN:
            sql = """SELECT *
                     FROM information_schema.tables
                     WHERE table_schema = 'barcodes'"""
            TRN.add(sql)
            obs = TRN.execute_fetchflatten()
            self.assertNotIn('rollback', obs)


if __name__ == '__main__':
    main()
