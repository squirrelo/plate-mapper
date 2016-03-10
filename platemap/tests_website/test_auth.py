# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import main

from platemap.tests_website.tornado_test_base import TestHandlerBase
import platemap as pm


@pm.util.rollback_tests()
class TestAuthLoginHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/auth/login/')
        self.assertEqual(obs.code, 200)
        # Make sure redirected back to index page
        self.assertRegex(obs.effective_url,
                         'http:\/\/[A-Za-z](.*):[0-9]{5}\/$')

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


@pm.util.rollback_tests()
class TestAuthLogoutHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/auth/logout/')
        self.assertEqual(obs.code, 200)


@pm.util.rollback_tests()
class TestCreateUserHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/user/add/')
        self.assertEqual(obs.code, 200)
        self.assertIn('Admin', obs.body.decode('utf-8'))
        self.assertNotIn('Basic access', obs.body.decode('utf-8'))

    def test_post(self):
        obs = self.post('/user/add/', {'username': 'newUser',
                                       'password': 'somePass',
                                       'name': 'New User',
                                       'email': 'new@user.com',
                                       'access': 'Override'})
        self.assertEqual(obs.code, 200)
        self.assertIn('Successfully created user newUser',
                      obs.body.decode('utf-8'))
        # Instantiate the user to make sure was added correctly
        user = pm.person.User('newUser')
        self.assertTrue(user.authenticate('somePass'))

    def test_post_bad(self):
        obs = self.post('/user/add/', {'username': 'User1',
                                       'password': 'somePass',
                                       'name': 'New User',
                                       'email': 'new@user.com',
                                       'access': 'No Idea!'})
        self.assertEqual(obs.code, 200)
        self.assertIn('The object with name \'User1\' already exists in table '
                      '\'user\'', obs.body.decode('utf-8'))


if __name__ == '__main__':
    main()
