# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from tornado.web import authenticated
from tornado.escape import url_escape

from platemap.handlers.base import BaseHandler
import platemap as pm


class AuthBasehandler(BaseHandler):
    def set_current_user(self, user=None):
        if user is not None:
            self.set_secure_cookie('user', user)
        else:
            self.clear_cookie('user')


class AuthLoginHandler(AuthBasehandler):
    """user login, no page necessary"""
    def get(self, *args, **kwargs):
        self.redirect('/')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        try:
            login = pm.person.User(username).authenticate(password)
        except pm.exceptions.UnknownIDError:
            msg = url_escape('Unknown username')
            self.redirect('/?msg=%s' % msg)
            return

        if login:
            # everything good so log in
            self.set_current_user(username)
            self.redirect(self.get_argument('next', '/'))
            return
        else:
            msg = url_escape('Bad password')
            self.redirect('/?msg=%s' % msg)
            return


class AuthLogoutHandler(AuthBasehandler):
    'Logout handler, no page necessary'
    @authenticated
    def get(self):
        self.set_current_user()
        self.redirect('/')
