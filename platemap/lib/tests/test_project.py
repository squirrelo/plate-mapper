from unittest import TestCase, main
import platemap as pm


@pm.util.rollback_tests()
class TestProject(TestCase):
    def setUp(self):
        self.project = pm.project.Project(1)

    def test_create(self):
        obs = pm.project.Project.create(
            'NewTestProj', 'For testing', pm.person.Person(1), 'PI', 'contact',
            'NewSampleSet')

        self.assertEqual(obs.name, 'NewTestProj')
        self.assertEqual(obs.description, 'For testing')
        self.assertEqual(obs.pi, 'PI')
        self.assertEqual(obs.contact, 'contact')
        self.assertEqual(obs.samples, {})
        self.assertEqual(obs.sample_sets, ['NewSampleSet'])

    def test_create_barcodes(self):
        self.assertFalse(pm.util.check_barcode_assigned('000000005'))
        self.assertFalse(pm.util.check_barcode_assigned('000000006'))
        self.assertFalse(pm.util.check_barcode_assigned('000000007'))
        obs = pm.project.Project.create(
            'NewTestProj', 'For testing', pm.person.Person(1), 'PI', 'contact',
            'NewSampleSet', num_barcodes=2)

        self.assertTrue(pm.util.check_barcode_assigned('000000005'))
        self.assertTrue(pm.util.check_barcode_assigned('000000006'))
        self.assertFalse(pm.util.check_barcode_assigned('000000007'))

        self.assertEqual(obs.name, 'NewTestProj')
        self.assertEqual(obs.description, 'For testing')
        self.assertEqual(obs.pi, 'PI')
        self.assertEqual(obs.contact, 'contact')
        self.assertEqual(obs.samples, {})
        self.assertEqual(obs.sample_sets, ['NewSampleSet'])

    def test_create_error(self):
        with self.assertRaises(pm.exceptions.DuplicateError):
            pm.project.Project.create(
                'Project 1', 'For testing', pm.person.Person(1), 'PI',
                'contact', 'NewSampleSet')

        with self.assertRaises(ValueError):
            pm.project.Project.create(
                'newproj', 'For testing', pm.person.Person(1), 'PI',
                'contact', 'NewSampleSet', 50)
        self.assertFalse(pm.project.Project.exists('newproj'))

    def test_exists(self):
        self.assertTrue(pm.project.Project.exists('Project 1'))

    def test_exists_no_exist(self):
        self.assertFalse(pm.project.Project.exists('New Project For Test'))

    def test_delete(self):
        pass

    def test_get_name(self):
        self.assertEqual(self.project.name, 'Project 1')

    def test_get_samples(self):
        self.assertEqual(self.project.samples,
                         {'Sample Set 1': [pm.sample.Sample(1),
                                           pm.sample.Sample(2),
                                           pm.sample.Sample(3)]})

    def test_get_sample_sets(self):
        self.assertEqual(self.project.sample_sets, ['Sample Set 1'])

    def test_get_pi(self):
        self.assertEqual(self.project.pi, 'PI1')

    def test_set_pi(self):
        self.project.pi = 'New Test PI Person'
        self.assertEqual(self.project.pi, 'New Test PI Person')

    def test_get_contact(self):
        self.assertEqual(self.project.contact, 'contact1')

    def test_set_contact(self):
        self.project.contact = 'New Test Contact Person'
        self.assertEqual(self.project.contact, 'New Test Contact Person')

    def test_add_samples(self):
        self.assertEqual(self.project.samples,
                         {'Sample Set 1': [pm.sample.Sample(1),
                                           pm.sample.Sample(2),
                                           pm.sample.Sample(3)]})

        self.project.add_samples([pm.sample.Sample(4)])
        self.assertEqual(self.project.samples,
                         {'Sample Set 1': [pm.sample.Sample(1),
                                           pm.sample.Sample(2),
                                           pm.sample.Sample(3)],
                          'Sample Set 2': [pm.sample.Sample(4)]})

    def test_remove_samples(self):
        self.assertEqual(self.project.samples,
                         {'Sample Set 1': [pm.sample.Sample(1),
                                           pm.sample.Sample(2),
                                           pm.sample.Sample(3)]})
        self.project.remove_samples([pm.sample.Sample(2), pm.sample.Sample(3)])
        self.assertEqual(self.project.samples,
                         {'Sample Set 1': [pm.sample.Sample(1)]})

    def test_add_sample_set(self):
        self.project.add_sample_set('New Test Sample Set', pm.person.Person(1))
        self.assertEqual(self.project.sample_sets, ['Sample Set 1',
                                                    'New Test Sample Set'])

    def test_remove_sample_set(self):
        self.project.add_sample_set('New Test Sample Set', pm.person.Person(1))
        self.project.remove_sample_set('Sample Set 1')
        self.assertEqual(self.project.sample_sets, ['New Test Sample Set'])

    def test_remove_sample_set_not_zero(self):
        with self.assertRaises(pm.exceptions.EditError):
            self.project.remove_sample_set('Sample Set 1')

    def test_assign_barcodes(self):
        self.assertFalse(pm.util.check_barcode_assigned('000000005'))
        self.assertFalse(pm.util.check_barcode_assigned('000000006'))
        self.assertFalse(pm.util.check_barcode_assigned('000000007'))
        self.project.assign_barcodes(num_barcodes=2)

        self.assertTrue(pm.util.check_barcode_assigned('000000005'))
        self.assertTrue(pm.util.check_barcode_assigned('000000006'))
        self.assertFalse(pm.util.check_barcode_assigned('000000007'))

    def test_clear_barcodes(self):
        proj = pm.project.Project(3)
        self.assertTrue(pm.util.check_barcode_assigned('000000004'))
        proj.clear_barcodes()
        self.assertFalse(pm.util.check_barcode_assigned('000000004'))


if __name__ == "__main__":
    main()
