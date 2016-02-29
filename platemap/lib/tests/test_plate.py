# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import TestCase, main

import platemap as pm


@pm.util.rollback_tests()
class TestPlate(TestCase):
    def setUp(self):
        self.plate = pm.plate.Plate('000000003')

    def test_plates(self):
        obs = pm.plate.Plate.plates()
        exp = [pm.plate.Plate('000000003')]
        self.assertEqual(obs, exp)

    def test_plates_finalized(self):
        obs = pm.plate.Plate.plates(finalized=True)
        self.assertEqual(obs, [])

        pm.plate.Plate('000000003').finalize()
        obs = pm.plate.Plate.plates(finalized=True)
        exp = [pm.plate.Plate('000000003')]
        self.assertEqual(obs, exp)

    def test_create(self):
        self.assertFalse(pm.util.check_barcode_assigned('000000009'))
        obs = pm.plate.Plate.create('000000009', 'new test plate',
                                    pm.person.Person(1), 8, 12)

        self.assertEqual(obs.id, '000000009')
        self.assertEqual(obs.name, 'new test plate')
        self.assertEqual(obs.shape, (8, 12))
        self.assertTrue(pm.util.check_barcode_assigned('000000009'))

    def test_create_used_barcode(self):
        with self.assertRaises(pm.exceptions.DeveloperError):
            pm.plate.Plate.create('000000001', 'bad plate',
                                  pm.person.Person(1), 8, 12)

    def test_create_plate_exists(self):
        with self.assertRaises(pm.exceptions.DuplicateError):
            pm.plate.Plate.create('000000003', 'bad plate',
                                  pm.person.Person(1), 8, 12)

    def test_delete(self):
        pass

    def test_exists(self):
        obs = pm.plate.Plate.exists('000000003')
        self.assertTrue(obs)

    def test_exists_no_exists(self):
        # Barcode asigned but not in plate table
        obs = pm.plate.Plate.exists('000000001')
        self.assertFalse(obs)

        # Completely unused barcode
        obs = pm.plate.Plate.exists('000000008')
        self.assertFalse(obs)

    def test_check_finalized(self):
        self.plate.finalize()
        with self.assertRaises(pm.exceptions.EditError):
            self.plate._check_finalized()

    def test_setitem(self):
        samp1 = pm.sample.Sample(1)
        samp2 = pm.sample.Sample(2)

        self.assertEqual(self.plate[1, 1], samp1)
        self.plate[1, 1] = samp2
        self.assertEqual(self.plate[1, 1], samp2)
        self.plate[1, 1] = None
        self.assertEqual(self.plate[1, 1], None)

        self.assertEqual(self.plate[7, 11], None)
        self.plate[7, 11] = samp1
        self.assertEqual(self.plate[7, 11], samp1)

    def test_setitem_outside_plate(self):
        samp = pm.sample.Sample(1)

        with self.assertRaises(IndexError):
            self.plate[-1, 0] = samp

        with self.assertRaises(IndexError):
            self.plate[0, -1] = samp

        with self.assertRaises(IndexError):
            self.plate[9, 12] = samp

        with self.assertRaises(IndexError):
            self.plate[8, 13] = samp

    def test_setitem_finalized(self):
        self.plate.finalize()
        samp = pm.sample.Sample(1)

        with self.assertRaises(pm.exceptions.EditError):
            self.plate[0, 0] = samp

    def test_getitem(self):
        samp1 = pm.sample.Sample(1)
        samp3 = pm.sample.Sample(3)

        self.assertEqual(self.plate[0, 0], None)
        self.assertEqual(self.plate[1, 1], samp1)
        self.assertEqual(self.plate[2, 3], samp3)
        self.assertEqual(self.plate[7, 11], None)

    def test_getitem_outside_plate(self):
        with self.assertRaises(IndexError):
            self.plate[-1, 0]

        with self.assertRaises(IndexError):
            self.plate[0, -1]

        with self.assertRaises(IndexError):
            self.plate[7, 12]

        with self.assertRaises(IndexError):
            self.plate[8, 11]

    def test_name(self):
        self.assertEqual(self.plate.name, 'Test plate 1')

    def test_finalized(self):
        self.assertEqual(self.plate.finalized, False)

    def test_shape(self):
        self.assertEqual(self.plate.shape, (8, 12))

    def test_samples(self):
        obs = self.plate.samples
        exp = [pm.sample.Sample(1), pm.sample.Sample(2), pm.sample.Sample(3)]
        self.assertEqual(obs, exp)

    def test_platemap(self):
        obs = self.plate.platemap
        exp = [[None, None, None, None, None, None, None, None, None, None,
                None, None],
               [None, pm.sample.Sample(1), pm.sample.Sample(2), None, None,
                None, None, None, None, None, None, None],
               [None, None, None, pm.sample.Sample(3), None, None, None, None,
                None, None, None, None],
               [None, None, None, None, None, None, None, None, None, None,
                None, None],
               [None, None, None, None, None, None, None, None, None, None,
                None, None],
               [None, None, None, None, None, None, None, None, None, None,
                None, None],
               [None, None, None, None, None, None, None, None, None, None,
                None, None],
               [None, None, None, None, None, None, None, None, None, None,
                None, None]]
        self.assertEqual(obs, exp)

    def test_to_html(self):
        obs = self.plate.to_html()
        exp = ('<table class="plate"><tr><th></th><th>1</th><th>2</th><th>3'
               '</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9'
               '</th><th>10</th><th>11</th><th>12</th></tr><tr><th>A</th></tr>'
               '<tr><th>B</th><td>Sample 1</td><td>Sample 2</td></tr><tr><th>'
               'C</th><td>Sample 3</td></tr><tr><th>D</th></tr><tr><th>E</th>'
               '</tr><tr><th>F</th></tr><tr><th>G</th></tr><tr><th>H</th>'
               '</tr></table>')
        self.assertEqual(obs, exp)

    def test_finalize(self):
        self.assertEqual(self.plate.finalized, False)
        self.plate.finalize()
        self.assertEqual(self.plate.finalized, True)


if __name__ == "__main__":
    main()
