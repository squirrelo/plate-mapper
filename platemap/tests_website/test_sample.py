# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import main
from io import StringIO

from requests_toolbelt import MultipartEncoder

from platemap.tests_website.tornado_test_base import TestHandlerBase
from platemap.lib.util import rollback_tests
import platemap as pm


@rollback_tests()
class TestSampleCreateHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/sample/add/')
        self.assertEqual(obs.code, 200)
        self.assertIn("source: [\'the freezer\', \'the other freezer\']",
                      obs.body.decode('utf-8'))

    def test_post_no_barcode(self):
        self.assertEqual(len(pm.sample.Sample.search(sample_type='nobc')), 0)
        obs = self.post('/sample/add/', {'sample': 'nobc',
                                         'barcode': '',
                                         'sample-set': 'Sample Set 1',
                                         'type': 'nobc',
                                         'location': 'the freezer'})
        self.assertEqual(obs.code, 200)
        self.assertIn('Created sample nobc',
                      obs.body.decode('utf-8'))

        search = pm.sample.Sample.search(sample_type='nobc')
        self.assertEqual(len(search), 1)
        self.assertEqual(search[0].barcode, None)

    def test_post_barcode(self):
        self.assertEqual(len(pm.sample.Sample.search(barcode='000000007')), 0)
        obs = self.post('/sample/add/', {'sample': 'new posted sample',
                                         'barcode': '000000007',
                                         'sample-set': 'Sample Set 1',
                                         'type': 'stool',
                                         'location': 'the freezer'})
        self.assertEqual(obs.code, 200)
        self.assertIn('Created sample new posted sample',
                      obs.body.decode('utf-8'))

        search = pm.sample.Sample.search(barcode='000000007')
        self.assertEqual(len(search), 1)
        self.assertEqual(search[0].barcode, '000000007')

    def test_post_barcode_error(self):
        self.assertEqual(len(pm.sample.Sample.search(barcode='000000007')), 0)
        obs = self.post('/sample/add/', {'sample': 'new posted sample',
                                         'barcode': '000000003',
                                         'sample-set': 'Sample Set 1',
                                         'type': 'stool',
                                         'location': 'the freezer'})
        self.assertEqual(obs.code, 200)
        self.assertIn('Barcode 000000003 already assigned!',
                      obs.body.decode('utf-8'))

    def test_post_file(self):
        file = StringIO('sample_name\tother_col\ntest1\tval1\ntest2\tval2\n')
        m = MultipartEncoder(
            fields={
                'sample-set': 'Sample Set 1',
                'type': 'test',
                'location': 'the freezer',
                'file': ('test_bc.txt', file, 'text/plain')}
        )

        self.assertEqual(len(pm.sample.Sample.search(sample_type='test')), 0)
        obs = self.post('/sample/add/', m.to_string(),
                        headers={'Content-Type': m.content_type})
        self.assertEqual(obs.code, 200)
        self.assertIn('Created 2 samples from test_bc.txt',
                      obs.body.decode('utf-8'))
        self.assertEqual(len(pm.sample.Sample.search(sample_type='test')), 2)

    def test_post_file_error(self):
        file = StringIO('sample_name\tbarcode\nSample 1\t000000001\n')
        m = MultipartEncoder(
            fields={
                'sample-set': 'Sample Set 1',
                'type': 'test',
                'location': 'the freezer',
                'file': ('test_bc.txt', file, 'text/plain')}
        )

        self.assertEqual(len(pm.sample.Sample.search(sample_type='test')), 0)
        obs = self.post('/sample/add/', m.to_string(),
                        headers={'Content-Type': m.content_type})
        self.assertEqual(obs.code, 200)
        self.assertIn('The object with name \'Sample 1\' already exists in '
                      'table \'sample\'', obs.body.decode('utf-8'))
        self.assertEqual(len(pm.sample.Sample.search(sample_type='test')), 0)


@rollback_tests()
class TestSampleEditHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/sample/edit/?sample-id=1')
        self.assertEqual(obs.code, 200)
        self.assertIn('<td> 000000001 </td>', obs.body.decode('utf-8'))
        self.assertIn('<input type="checkbox" checked="True" name="remaining"'
                      ' id="remaining">', obs.body.decode('utf-8'))

        obs = self.get('/sample/edit/?sample-id=3')
        self.assertEqual(obs.code, 200)
        self.assertIn('<input type="text" name="barcode" id="barcode">',
                      obs.body.decode('utf-8'))
        self.assertIn('<input type="checkbox" checked="False" name="remaining"'
                      ' id="remaining">', obs.body.decode('utf-8'))

    def test_get_nosample(self):
        obs = self.get('/sample/edit/')
        self.assertEqual(obs.code, 400)

    def test_post(self):
        data = {
            'sample-id': 1,
            'location': 'the other test thing',
            'type': 'skin'
        }
        obs = self.post('/sample/edit/', data)
        self.assertEqual(obs.code, 200)
        self.assertIn('Updated successfully', obs.body.decode('utf-8'))

        sample = pm.sample.Sample(1)
        self.assertFalse(sample.biomass_remaining)
        self.assertEqual(sample.location, 'the other test thing')
        self.assertEqual(sample.sample_type, 'skin')
        self.assertEqual(sample.barcode, '000000001')

        data = {
            'sample-id': 3,
            'location': 'the other test thing',
            'type': 'skin',
            'barcode': '000000007'
        }
        obs = self.post('/sample/edit/', data)
        self.assertEqual(obs.code, 200)
        self.assertIn('Updated successfully', obs.body.decode('utf-8'))

        sample = pm.sample.Sample(3)
        self.assertFalse(sample.biomass_remaining)
        self.assertEqual(sample.location, 'the other test thing')
        self.assertEqual(sample.sample_type, 'skin')
        self.assertEqual(sample.barcode, '000000007')

    def test_post_error(self):
        data = {
            'sample-id': 1,
            'location': 'the other test thing',
            'type': 'skin',
            'barcode': '000000001'
        }
        obs = self.post('/sample/edit/', data)
        self.assertEqual(obs.code, 200)
        self.assertIn('ERROR: Barcode 000000001 already assigned',
                      obs.body.decode('utf-8'))


if __name__ == '__main__':
    main()
