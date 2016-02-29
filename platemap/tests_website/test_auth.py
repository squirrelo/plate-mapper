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
class TestAuthLoginHandler(TestHandlerBase):
    def test_post(self):
        obs = self.post('/auth/login/', {'username': 'User1',
                                         'password': 'password'})
        self.assertEqual(obs.code, 200)
        self.assertIn('Hello User1!', obs.body.decode('utf-8'))

    def test_post_bad_username(self):
        obs = self.post('/auth/login/', {'username': 'UnknownUser',
                                         'password': 'password'})
        self.assertEqual(obs.code, 200)
        self.assertIn('Unknown username', obs.body.decode('utf-8'))

    def test_post_bad_password(self):
        obs = self.post('/auth/login/', {'username': 'User1',
                                         'password': 'BADPASS'})
        self.assertEqual(obs.code, 200)
        self.assertIn('Bad password', obs.body.decode('utf-8'))


@rollback_tests()
class TestAuthLogoutHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/auth/logout/')
        self.assertEqual(obs.code, 200)


if __name__ == '__main__':
    main()
