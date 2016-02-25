from unittest import TestCase, main

import platemap as pm


@pm.util.rollback_tests()
class TestPlate(TestCase):
    def setUp(self):
        self.plate = pm.plate.Plate('000000003')

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

    def test_setitem(self):
        samp = pm.sample.Sample(1)
        self.assertEqual(self.plate[0, 0], None)
        self.plate[0, 0] = samp
        self.assertEqual(self.plate[0, 0], samp)

        self.assertEqual(self.plate[8, 12], None)
        self.plate[0, 0] = samp
        self.assertEqual(self.plate[8, 12], samp)

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

    def test_getitem(self):
        pass

    def test_name(self):
        pass

    def test_finalized(self):
        pass

    def test_shape(self):
        pass

    def test_samples(self):
        pass

    def test_platemap(self):
        pass

    def test_to_html(self):
        pass


if __name__ == "__main__":
    main()
