from unittest import TestCase, main
from platemap.lib.util import (
    check_barcode_assigned, convert_from_id, convert_to_id, get_count)


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

if __name__ == '__main__':
    main()
