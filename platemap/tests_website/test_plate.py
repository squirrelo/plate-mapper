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
class TestPlateCreateHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/plate/add/')
        self.assertEqual(obs.code, 200)
        self.assertIn('<option value="96 well">', obs.body.decode('utf-8'))

    def test_post(self):
        self.assertEqual(len(pm.plate.Plate.plates()), 1)

        obs = self.post('/plate/add/', {'barcode': '000000007',
                                        'name': 'post plate',
                                        'plate': '96 well'})
        self.assertEqual(obs.code, 200)
        # make sure redirected to the edit page
        self.assertRegex(
            obs.effective_url,
            'http:\/\/[A-Za-z](.*):[0-9]{5}\/plate\/edit\/\?plate=000000007$')

        self.assertEqual(len(pm.plate.Plate.plates()), 2)


class TestPlateEditHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/plate/edit/')
        self.assertEqual(obs.code, 200)
        self.assertIn('<option value="000000003">000000003 - '
                      'Test plate 1</option>', obs.body.decode('utf-8'))


class TestPlateRenderHandler(TestHandlerBase):
    def test_get(self):
            obs = self.get('/plate/render/000000003')
            self.assertEqual(obs.code, 200)
            self.assertIn('<h3>Plate 000000003 - Test plate 1</h3>',
                          obs.body.decode('utf-8'))

    def test_get_blank(self):
        obs = self.get('/plate/render/')
        self.assertEqual(obs.code, 200)
        self.assertEqual('', obs.body.decode('utf-8'))

if __name__ == '__main__':
    main()
