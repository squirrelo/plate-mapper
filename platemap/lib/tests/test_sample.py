from unittest import TestCase, main
from datetime import datetime

import platemap.lib


class TestSample(TestCase):
    @platemap.lib.util.rollback_transaction
    def setUp(self):
        self.sample = platemap.lib.Sample(1)

    @platemap.lib.util.rollback_transaction
    def test_search(self):
        obs = platemap.lib.Sample.search(biomass_remaining=True)
        exp = [platemap.lib.Sample(1), platemap.lib.Sample(3),
               platemap.lib.Sample(4)]
        self.assertEqual(obs, exp)

        obs = platemap.lib.Sample.search(sample_type='stool')
        exp = [platemap.lib.Sample(1), platemap.lib.Sample(2)]
        self.assertEqual(obs, exp)

        obs = platemap.lib.Sample.search(barcode='000000002')
        exp = [platemap.lib.Sample(2)]
        self.assertEqual(obs, exp)

        obs = platemap.lib.Sample.search(barcode='000000010')
        exp = []
        self.assertEqual(obs, exp)

        # TODO: finish these tests as objects are made
        # platemap.lib.Sample.search(project=)
        # platemap.lib.Sample.search(primer_set=)
        # platemap.lib.Sample.search(protocol=)

    @platemap.lib.util.rollback_transaction
    def test_search_no_parameters(self):
        with self.assertRaises(platemap.lib.exceptions.DeveloperError):
            platemap.lib.Sample.search()

    @platemap.lib.util.rollback_transaction
    def test_create(self):
        new_id = platemap.lib.util.get_count('sample') + 1
        start = datetime.now()
        platemap.lib.Sample.create(
            'test sample', 'test', 'in the mail', 'Sample Set 1',
            platemap.lib.person.Person(3))
        end = datetime.now()

        obs = platemap.lib.Sample(new_id)
        self.assertEqual(obs.name, 'test sample')
        self.assertEqual(obs.sample_type, 'test')
        self.assertEqual(obs.location, 'in the mail')
        self.assertEqual(obs.sample_set, 'Sample Set 1')
        self.assertEqual(obs.created_by, 'Third test person')
        self.assertEqual(obs.last_scanned_by, 'Third test person')
        self.assertTrue(start < obs.created_on < end)
        self.assertTrue(start < obs.last_scanned_on < end)
        self.assertEqual(obs.projects, None)
        self.assertEqual(obs.barcode, None)

    @platemap.lib.util.rollback_transaction
    def test_create_with_barcode(self):
        new_id = platemap.lib.util.get_count('sample') + 1
        start = datetime.now()
        platemap.lib.Sample.create(
            'test sample', 'test', 'in the mail', 'Sample Set 1',
            platemap.lib.person.Person(3), barcode='000000006')
        end = datetime.now()

        obs = platemap.lib.Sample(new_id)
        self.assertEqual(obs.name, 'test sample')
        self.assertEqual(obs.sample_type, 'test')
        self.assertEqual(obs.location, 'in the mail')
        self.assertEqual(obs.sample_set, 'Sample Set 1')
        self.assertEqual(obs.created_by, 'Third test person')
        self.assertEqual(obs.last_scanned_by, 'Third test person')
        self.assertTrue(start < obs.created_on < end)
        self.assertTrue(start < obs.last_scanned_on < end)
        self.assertEqual(obs.projects, None)
        self.assertEqual(obs.barcode, '000000006')
        self.assertTrue(platemap.lib.util.check_barcode_assigned('000000006'))

    @platemap.lib.util.rollback_transaction
    def test_create_with_projects(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_create_used_barcode(self):
        with self.assertRaises(ValueError):
            platemap.lib.Sample.create(
                'test sample', 'test', 'in the mail', 'Sample Set 1',
                platemap.lib.person.Person(3), barcode='000000001')

    @platemap.lib.util.rollback_transaction
    def test_exists(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_exists_no_exists(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_delete(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_delete_no_exists(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_name(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_barcode(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_barcode_none(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_add_barcode(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_add_barcode_already_used_barcode(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_add_barcode_already_assigned_to_sample(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_projects(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_sample_type(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_sample_location(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_biomass_remaining(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_created_on(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_created_by(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_last_scanned(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_last_scanned_by(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_plates(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_protocols(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_pools(self):
        pass

    @platemap.lib.util.rollback_transaction
    def test_runs(self):
        pass


if __name__ == "__main__":
    main()
