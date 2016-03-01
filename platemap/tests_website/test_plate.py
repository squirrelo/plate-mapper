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


@rollback_tests()
class TestPlateEditHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/plate/edit/')
        self.assertEqual(obs.code, 200)
        self.assertIn('<option value="000000003">000000003 - '
                      'Test plate 1</option>', obs.body.decode('utf-8'))


@rollback_tests()
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


@rollback_tests()
class TestPlateStaticRenderHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/plate/html/000000003')
        exp = ('<table class="plate"><tr><th></th><th>1</th><th>2</th><th>3'
               '</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9'
               '</th><th>10</th><th>11</th><th>12</th></tr><tr><th>A</th><td>'
               '</td><td></td><td></td><td></td><td></td><td></td><td></td>'
               '<td></td><td></td><td></td><td></td><td></td></tr><tr><th>B'
               '</th><td></td><td>Sample 1</td><td>Sample 2</td><td></td><td>'
               '</td><td></td><td></td><td></td><td></td><td></td><td></td>'
               '<td></td></tr><tr><th>C</th><td></td><td></td><td></td><td>'
               'Sample 3</td><td></td><td></td><td></td><td></td><td></td><td>'
               '</td><td></td><td></td></tr><tr><th>D</th><td></td><td></td>'
               '<td></td><td></td><td></td><td></td><td></td><td></td><td>'
               '</td><td></td><td></td><td></td></tr><tr><th>E</th><td></td>'
               '<td></td><td></td><td></td><td></td><td></td><td></td><td>'
               '</td><td></td><td></td><td></td><td></td></tr><tr><th>F</th>'
               '<td></td><td></td><td></td><td></td><td></td><td></td><td>'
               '</td><td></td><td></td><td></td><td></td><td></td></tr><tr>'
               '<th>G</th><td></td><td></td><td></td><td></td><td></td><td>'
               '</td><td></td><td></td><td></td><td></td><td></td><td></td>'
               '</tr><tr><th>H</th><td></td><td></td><td></td><td></td><td>'
               '</td><td></td><td></td><td></td><td></td><td></td><td></td>'
               '<td></td></tr></table>')
        self.assertEqual(obs.code, 200)
        self.assertEqual(obs.body.decode('utf-8'), exp)

    def test_get_blank(self):
        obs = self.get('/plate/html/')
        self.assertEqual(obs.code, 200)
        self.assertEqual(obs.body.decode('utf-8'), '')


@rollback_tests()
class TestPlateUpdateHandler(TestHandlerBase):
    plate = pm.plate.Plate('000000003')

    def test_post_update(self):
        self.assertEqual(self.plate[6, 10], None)

        obs = self.post('/plate/update/', {'plate_id': '000000003',
                                           'action': 'update',
                                           'rowcol': '6-10',
                                           'sample': 'Sample 3'})
        self.assertEqual(obs.code, 200)
        self.assertEqual(obs.body.decode('utf-8'), '')
        self.assertEqual(self.plate[6, 10], pm.sample.Sample(3))

    def test_post_update_unknown_sample(self):
        self.assertEqual(self.plate[6, 10], None)

        obs = self.post('/plate/update/', {'plate_id': '000000003',
                                           'action': 'update',
                                           'rowcol': '6-10',
                                           'sample': 'UNKNOWN'})
        self.assertEqual(obs.code, 200)
        self.assertEqual(obs.body.decode('utf-8'),
                         'Could not find sample "UNKNOWN"')
        self.assertEqual(self.plate[6, 10], None)

    def test_post_update_bad_well(self):
        obs = self.post('/plate/update/', {'plate_id': '000000003',
                                           'action': 'update',
                                           'rowcol': '25-100',
                                           'sample': 'Sample 2'})
        self.assertEqual(obs.code, 200)
        self.assertEqual(obs.body.decode('utf-8'),
                         'Position 25, 100 not on plate')

    def test_post_finalize(self):
        self.assertEqual(self.plate.finalized, False)

        obs = self.post('/plate/update/', {'plate_id': '000000003',
                                           'action': 'finalize'})
        self.assertEqual(obs.code, 200)
        self.assertEqual(obs.body.decode('utf-8'), '')
        self.assertEqual(self.plate.finalized, True)

    def test_post_unknown(self):
        obs = self.post('/plate/update/', {'plate_id': '000000003',
                                           'action': 'bad'})
        self.assertEqual(obs.code, 400)


if __name__ == '__main__':
    main()
