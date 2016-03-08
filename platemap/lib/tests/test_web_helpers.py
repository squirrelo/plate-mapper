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
    def _count_lots(self):
        sql = "SELECT count(*) FROM barcodes.primer_set_lots"
        with pm.sql.TRN:
            pm.sql.TRN.add(sql)
            return pm.sql.TRN.execute_fetchlast()

    def test_get_extraction_plates(self):
        obs = pm.webhelp.get_extraction_plates()
        exp = [['000000003', 'Test plate 1', 2, datetime(2016, 2, 28, 0, 0)]]
        self.assertEqual(obs, exp)

    def test_check_create_primer_lot(self):
        count = self._count_lots()
        pm.webhelp.check_create_primer_lot(1, 'pr001', pm.person.Person(1))
        self.assertEqual(count, self._count_lots())

    def test_check_create_primer_lot_new(self):
        count = self._count_lots()
        pm.webhelp.check_create_primer_lot(1, 'NEW LOT', pm.person.Person(1))
        self.assertEqual(count + 1, self._count_lots())

    def test_get_primer_sets(self):
        obs = pm.webhelp.get_primer_sets()
        exp = [[1, 'Primer Set 1'], [2, 'Primer Set 2']]
        self.assertEqual(obs, exp)

    def test_get_lots_for_primer_set(self):
        obs = pm.webhelp.get_lots_for_primer_set(1)
        exp = ['pr001']
        self.assertEqual(obs, exp)

    def test_get_instruments(self):
        obs = pm.webhelp.get_instruments()
        exp = ['454 GS FLX+', '454 GS FLX Titanium', 'Illumina HiSeq 2500',
               'Illumina MiSeq']
        self.assertCountEqual(obs, exp)

    def test_get_finalized_pcr_protocols(self):
        obs = pm.webhelp.get_finalized_pcr_protocols()
        exp = [[4, 'Test plate 1 - 000000003 - 2016-02-28 00:00:00']]
        self.assertEqual(obs, exp)


if __name__ == '__main__':
    main()
