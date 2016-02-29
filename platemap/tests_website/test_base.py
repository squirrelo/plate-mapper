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


@rollback_tests()
class TestBaseHandler(TestHandlerBase):
    def test_error(self):
        obs = self.post('/auth/login/', {})
        self.assertEqual(obs.code, 400)
        self.assertIn('HTTP 400: Bad Request (Missing argument username)',
                      obs.body.decode('utf-8'))


@rollback_tests()
class TestMainHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/')
        self.assertEqual(obs.code, 200)

        self.assertNotIn('Enter password', obs.body.decode('utf-8'))
        self.assertIn('Add Sample', obs.body.decode('utf-8'))


@rollback_tests()
class TestNoPageHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/randombadurl')
        self.assertEqual(obs.code, 404)
        self.assertIn('ERROR 404!', obs.body.decode('utf-8'))


if __name__ == '__main__':
    main()
