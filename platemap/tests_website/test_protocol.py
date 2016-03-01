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
class TestLogExtractionHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/log/extraction/')
        self.assertEqual(obs.code, 200)
        self.assertIn('<input type="hidden" name="plate-id" id="plate-id">',
                      obs.body.decode('utf-8'))
        self.assertNotIn('<option value="000000003">',
                         obs.body.decode('utf-8'))

    def test_post(self):
        pm.plate.Plate('000000003').finalize()
        obs = self.post('/log/extraction/', {'plate-id': '000000003',
                                             'extractionkit_lot': 'lot12',
                                             'extraction_robot': 'rob-e',
                                             'tm1000_8_tool': 'tool12'})
        self.assertEqual(obs.code, 200)
        self.assertRegex(
            obs.effective_url,
            'http:\/\/[A-Za-z](.*):[0-9]{5}\/\?'
            'msg=Successfully\+logged\+PCR\+run$'
        )

    def test_post_error(self):
        obs = self.post('/log/extraction/', {'plate-id': '000000012',
                                             'extractionkit_lot': 'lot12',
                                             'extraction_robot': 'rob-e',
                                             'tm1000_8_tool': 'tool12'})
        self.assertEqual(obs.code, 200)
        self.assertIn('<div id="message">The object with ID \'000000012\' '
                      'does not exist in table \'plate\'</div>',
                      obs.body.decode('utf-8'))


if __name__ == '__main__':
    main()
