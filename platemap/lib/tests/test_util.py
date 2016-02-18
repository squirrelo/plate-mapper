from unittest import TestCase, main
from platemap.lib.util import (
    # check_barcode_assigned, convert_from_id, convert_to_id, get_count,
    rollback_transaction)
from platemap.lib.sql_connection import TRN


class TestUtil(TestCase):

    def test_convert_to_id(self):
        raise NotImplementedError()

    def test_convert_to_id_no_exist(self):
        raise NotImplementedError()

    def test_convert_from_id(self):
        raise NotImplementedError()

    def test_convert_from_id_no_exist(self):
        raise NotImplementedError()

    def test_get_count(self):
        raise NotImplementedError()

    def test_get_count_bad_table(self):
        raise NotImplementedError()

    def test_check_barcode_assigned(self):
        raise NotImplementedError()

    def test_check_barcode_assigned_no_exist(self):
        raise NotImplementedError()

    def test_check_barcode_assigned_assigned(self):
        raise NotImplementedError()

    def test_rollback_transaction(self):
        # Create decorated test function that adds a table
        @rollback_transaction
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
