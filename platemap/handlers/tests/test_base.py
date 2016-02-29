# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import main

import platemap as pm


@pm.util.rollback_tests()
class TestBaseHandler(pm.tests.tornado_test_base.TestHandlerBase):
    def test_error(self):
        obs = self.post('/auth/login/', {}, mocked=False)
        self.assertEqual(obs.code, 500)
        self.assertIn('Error code 500!', obs.body)


@pm.util.rollback_tests()
class TestMainHandler(pm.tests.tornado_test_base.TestHandlerBase):
    def test_load_noauth(self):
        obs = self.get('/', mocked=False)
        self.assertEqual(obs.code, 200)

        self.assertIn('Enter password', obs.body)
        self.assertNotIn('Add Sample', obs.body)

    def test_load_auth(self):
        obs = self.get('/')
        self.assertEqual(obs.code, 200)

        self.assertNotIn('Enter password', obs.body)
        self.assertIn('Add Sample', obs.body)


@pm.util.rollback_tests()
class TestNoPageHandler(pm.tests.tornado_test_base.TestHandlerBase):
    def test_unknown_page_noauth(self):
        obs = self.get('/', mocked=False)
        self.assertEqual(obs.code, 404)
        self.assertIn('Error 404!', obs.body)

    def test_unknown_page_auth(self):
        obs = self.get('/')
        self.assertEqual(obs.code, 404)
        self.assertIn('Error 404!', obs.body)


if __name__ == '__main__':
    main()
