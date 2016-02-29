# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import main

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


if __name__ == '__main__':
    main()
