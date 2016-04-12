# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import TestCase, main
from datetime import datetime
from io import StringIO

import platemap as pm


@pm.util.rollback_tests()
class TestSample(TestCase):
    def setUp(self):
        self.sample1 = pm.sample.Sample(1)
        self.sample3 = pm.sample.Sample(3)

    def test_types(self):
        obs = pm.sample.Sample.types()
        exp = ['oral', 'skin', 'stool']
        self.assertEqual(obs, exp)

    def test_locations(self):
        obs = pm.sample.Sample.locations()
        exp = ['the freezer', 'the other freezer']
        self.assertEqual(obs, exp)

    def test_from_file(self):
        file = StringIO('sample_name\tother_col\ntest1\tval1\ntest2\tval2\n')
        self.assertEqual(len(pm.sample.Sample.search(sample_type='test')), 0)
        obs = pm.sample.Sample.from_file(file, 'test', 'freezer',
                                         'Sample Set 1', pm.person.Person(1))
        self.assertEqual(len(pm.sample.Sample.search(sample_type='test')), 2)
        self.assertEqual(obs, 2)

    def test_from_file_comma_sep(self):
        file = StringIO('sample_name,other_col\ntest1,val1\ntest2,val2\n')
        self.assertEqual(len(pm.sample.Sample.search(sample_type='test')), 0)
        pm.sample.Sample.from_file(file, 'test', 'freezer', 'Sample Set 1',
                                   pm.person.Person(1), sep=',')
        self.assertEqual(len(pm.sample.Sample.search(sample_type='test')), 2)

    def test_from_file_barcodes(self):
        file = StringIO('sample_name\tother\tbarcode\ntest1\t1\t000000008\n'
                        'test2\t2\t000000009\n')
        self.assertEqual(len(pm.sample.Sample.search(sample_type='test')), 0)
        pm.sample.Sample.from_file(file, 'test', 'freezer', 'Sample Set 1',
                                   pm.person.Person(1))
        self.assertEqual(len(pm.sample.Sample.search(sample_type='test')), 2)
        self.assertEqual(len(pm.sample.Sample.search(barcode='000000008')), 1)
        self.assertEqual(len(pm.sample.Sample.search(barcode='000000009')), 1)

    def test_search(self):
        obs = pm.sample.Sample.search(name='Sample 1')
        exp = [pm.sample.Sample(1)]
        self.assertEqual(obs, exp)

        obs = pm.sample.Sample.search(biomass_remaining=True)
        exp = [pm.sample.Sample(1), pm.sample.Sample(4), pm.sample.Sample(5)]
        self.assertEqual(obs, exp)

        obs = pm.sample.Sample.search(sample_type='stool')
        exp = [pm.sample.Sample(1), pm.sample.Sample(2)]
        self.assertEqual(obs, exp)

        obs = pm.sample.Sample.search(barcode='000000002')
        exp = [pm.sample.Sample(2)]
        self.assertEqual(obs, exp)

        obs = pm.sample.Sample.search(barcode='000000010')
        exp = []
        self.assertEqual(obs, exp)

        obs = pm.sample.Sample.search(project='Project 2')
        exp = [pm.sample.Sample(4), pm.sample.Sample(5), pm.sample.Sample(2)]
        self.assertEqual(obs, exp)

        obs = pm.sample.Sample.search(sample_set='Sample Set 2')
        exp = [pm.sample.Sample(5), pm.sample.Sample(4)]
        self.assertEqual(obs, exp)

        # TODO: finish these tests as objects are made
        # pm.sample.Sample.search(primer_set=)
        # pm.sample.Sample.search(protocol=)

    def test_search_no_parameters(self):
        with self.assertRaises(pm.exceptions.DeveloperError):
            pm.sample.Sample.search()

    def test_create(self):
        obs = pm.sample.Sample.create(
            'test sample', 'test', 'in the mail', 'Sample Set 1',
            pm.person.Person(3))

        self.assertEqual(obs.name, 'test sample')
        self.assertEqual(obs.sample_type, 'test')
        self.assertEqual(obs.location, 'in the mail')
        self.assertEqual(obs.sample_set, 'Sample Set 1')
        self.assertEqual(obs.created_by, pm.person.Person(3))
        self.assertEqual(obs.last_scanned_by, pm.person.Person(3))
        self.assertEqual(obs.projects, ['Project 1'])
        self.assertEqual(obs.barcode, None)
        self.assertTrue(isinstance(obs.created_on, datetime))
        self.assertTrue(isinstance(obs.last_scanned, datetime))

    def test_create_with_barcode(self):
        obs = pm.sample.Sample.create(
            'test sample', 'test', 'in the mail', 'Sample Set 1',
            pm.person.Person(3), barcode='000000006')

        self.assertEqual(obs.name, 'test sample')
        self.assertEqual(obs.sample_type, 'test')
        self.assertEqual(obs.location, 'in the mail')
        self.assertEqual(obs.sample_set, 'Sample Set 1')
        self.assertEqual(obs.created_by, pm.person.Person(3))
        self.assertEqual(obs.last_scanned_by, pm.person.Person(3))
        self.assertEqual(obs.projects, ['Project 1'])
        self.assertEqual(obs.barcode, '000000006')
        self.assertTrue(pm.util.check_barcode_assigned('000000006'))
        self.assertTrue(isinstance(obs.created_on, datetime))
        self.assertTrue(isinstance(obs.last_scanned, datetime))

    def test_create_preassigned_barcode(self):
        obs = pm.sample.Sample.create(
            'test sample', 'test', 'in the mail', 'Sample Set 3',
            pm.person.Person(3), barcode='000000004')

        self.assertEqual(obs.name, 'test sample')
        self.assertEqual(obs.sample_type, 'test')
        self.assertEqual(obs.location, 'in the mail')
        self.assertEqual(obs.sample_set, 'Sample Set 3')
        self.assertEqual(obs.created_by, pm.person.Person(3))
        self.assertEqual(obs.last_scanned_by, pm.person.Person(3))
        self.assertEqual(obs.projects, ['Project 3'])
        self.assertEqual(obs.barcode, '000000004')
        self.assertTrue(pm.util.check_barcode_assigned('000000004'))
        self.assertTrue(isinstance(obs.created_on, datetime))
        self.assertTrue(isinstance(obs.last_scanned, datetime))

    def test_create_with_projects(self):
        obs = pm.sample.Sample.create(
            'test sample', 'test', 'in the mail', 'Sample Set 1',
            pm.person.Person(3), projects=['Project 1', 'Project 2'])

        self.assertEqual(obs.name, 'test sample')
        self.assertEqual(obs.sample_type, 'test')
        self.assertEqual(obs.location, 'in the mail')
        self.assertEqual(obs.sample_set, 'Sample Set 1')
        self.assertEqual(obs.created_by, pm.person.Person(3))
        self.assertEqual(obs.last_scanned_by, pm.person.Person(3))
        self.assertEqual(obs.projects, ['Project 1', 'Project 2'])
        self.assertEqual(obs.barcode, None)
        self.assertTrue(isinstance(obs.created_on, datetime))
        self.assertTrue(isinstance(obs.last_scanned, datetime))

    def test_create_used_barcode(self):
        with self.assertRaises(pm.exceptions.AssignError):
            pm.sample.Sample.create(
                'test sample new', 'test', 'in the mail', 'Sample Set 1',
                pm.person.Person(3), barcode='000000003')

    def test_create_mismatched_barcode_sample_set(self):
        with self.assertRaises(ValueError):
            pm.sample.Sample.create(
                'test sample new', 'test', 'in the mail', 'Sample Set 2',
                pm.person.Person(3), barcode='000000004')

    def test_create_sample_exists(self):
        with self.assertRaises(pm.exceptions.DuplicateError):
            pm.sample.Sample.create(
                'Sample 1', 'test', 'in the mail', 'Sample Set 1',
                pm.person.Person(3))

    def test_exists(self):
        self.assertTrue(
            pm.sample.Sample.exists('Sample 1', 'Sample Set 1'))

    def test_exists_no_exists(self):
        self.assertFalse(
            pm.sample.Sample.exists('NOEXISTS', 'Sample Set 1'))
        self.assertFalse(
            pm.sample.Sample.exists('Test Sample 1', 'NOEXISTS'))

    def test_delete(self):
        pass

    def test_delete_no_exists(self):
        pass

    def test_name(self):
        self.assertEqual(self.sample1.name, 'Sample 1')

    def test_barcode(self):
        self.assertEqual(self.sample1.barcode, '000000001')

    def test_barcode_none(self):
        self.assertEqual(self.sample3.barcode, None)

    def test_add_barcode(self):
        self.assertEqual(self.sample3.barcode, None)
        self.sample3.barcode = '000000010'
        self.assertEqual(self.sample3.barcode, '000000010')

    def test_add_barcode_already_used_barcode(self):
        with self.assertRaises(ValueError):
            self.sample3.barcode = '000000001'

    def test_add_barcode_already_assigned_to_sample(self):
        with self.assertRaises(pm.exceptions.AssignError):
            self.sample1.barcode = '000000010'

    def test_projects(self):
        self.assertEqual(self.sample1.projects, ['Project 1'])
        self.assertEqual(pm.sample.Sample(2).projects, ['Project 1',
                                                        'Project 2'])

    def test_sample_type(self):
        self.assertEqual(self.sample1.sample_type, 'stool')

    def test_sample_type_setter(self):
        self.sample1.sample_type = 'test type'
        self.assertEqual(self.sample1.sample_type, 'test type')

    def test_sample_location(self):
        self.assertEqual(self.sample1.location, 'the freezer')
        self.assertEqual(self.sample3.location, 'the other freezer')

    def test_sample_location_setter(self):
        self.sample1.location = 'NEW TEST PLACE!'
        self.assertEqual(self.sample1.location, 'NEW TEST PLACE!')

    def test_biomass_remaining(self):
        self.assertTrue(self.sample1.biomass_remaining)
        self.assertFalse(self.sample3.biomass_remaining)

    def test_biomass_remaining_setter(self):
        self.sample1.biomass_remaining = False
        self.assertFalse(self.sample1.biomass_remaining)

    def test_created_on(self):
        self.assertEqual(self.sample1.created_on, datetime(2016, 2, 22, 8, 52))

    def test_created_by(self):
        self.assertEqual(self.sample1.created_by, pm.person.Person(1))

    def test_last_scanned(self):
        self.assertEqual(self.sample1.created_on, datetime(2016, 2, 22, 8, 52))

    def test_last_scanned_by(self):
        self.assertEqual(self.sample1.created_by, pm.person.Person(1))

    def test_plates(self):
        self.assertEqual(
            self.sample1.plates, [pm.plate.Plate('000000003')])

    def test_add_project(self):
        obs = pm.sample.Sample.search(project='Project 2')
        exp = [pm.sample.Sample(4), pm.sample.Sample(5), pm.sample.Sample(2)]
        self.assertEqual(obs, exp)

        self.sample3.add_project('Project 2')
        obs = pm.sample.Sample.search(project='Project 2')
        exp = [pm.sample.Sample(4), pm.sample.Sample(5), pm.sample.Sample(2),
               pm.sample.Sample(3)]
        self.assertEqual(obs, exp)

    def test_add_project_already_in(self):
        sample = pm.sample.Sample(2)
        obs = pm.sample.Sample.search(project='Project 2')
        exp = [pm.sample.Sample(4), pm.sample.Sample(5), pm.sample.Sample(2)]
        self.assertEqual(obs, exp)

        #
        sample.add_project('Project 2')
        obs = pm.sample.Sample.search(project='Project 2')
        exp = [pm.sample.Sample(4), pm.sample.Sample(5), pm.sample.Sample(2)]
        self.assertEqual(obs, exp)

    def test_remove_project(self):
        obs = pm.sample.Sample.search(project='Project 1')
        exp = [pm.sample.Sample(1), pm.sample.Sample(2), pm.sample.Sample(3)]
        self.assertEqual(obs, exp)

        self.sample1.remove_project('Project 1')
        obs = pm.sample.Sample.search(project='Project 1')
        exp = [pm.sample.Sample(2), pm.sample.Sample(3)]
        self.assertEqual(obs, exp)

    def test_remove_project_failure(self):
        with self.assertRaises(LookupError):
            self.sample1.remove_project('Project NOEXIST')

        # make sure removing from project it isn't in doesn't raise errors
        self.sample1.remove_project('Project 3')

    def test_protocols(self):
        pass

    def test_pools(self):
        pass

    def test_runs(self):
        pass


if __name__ == "__main__":
    main()
