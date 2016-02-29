# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import logging
from traceback import format_exception

from tornado.web import RequestHandler

from platemap.lib.config_manager import pm_config
# import platemap as pm


class BaseHandler(RequestHandler):
    def get_current_user(self):
        """Overrides default method of returning user currently connected"""
        username = self.get_secure_cookie('user')
        if username is not None:
            # strip off quotes added by get_secure_cookie
            username = str(username)
            return username
            # return pm.person.User(username)
        else:
            self.clear_cookie('user')
            return None

    def write_error(self, status_code, **kwargs):
        """Overrides the error page created by Tornado"""
        user = self.current_user

        # Nicely formatted error info if debugging in test environment
        other = ''
        if pm_config.test_environment:
            exc_info = kwargs["exc_info"]
            trace_info = ''.join(format_exception(*exc_info))
            request_info = ''.join(["%s:   %s\n" %
                                   (k, self.request.__dict__[k]) for k in
                                    self.request.__dict__])
            error = exc_info[1]
            formatted_error = (">User\n%s\n\n>Error\n%s\n\n>Traceback\n%s\n\n"
                               ">Request Info\n%s\n\n" %
                               (user, error, trace_info, request_info))
            other = formatted_error.replace('\n', '<br/>')
        self.render('error.html', code=status_code, other=other)

        logging.exception(kwargs["exc_info"])

    def head(self, *args, **kwargs):
        """Satisfy servers that this url exists"""
        self.finish()


class MainHandler(BaseHandler):
    """Index page"""
    def get(self):
        msg = self.get_argument('msg', '')
        self.render('index.html', msg=msg)


class NoPageHandler(BaseHandler):
    """404 page"""
    def get(self, *args, **kwargs):
        self.set_status(404)
        self.render("404.html")

    def head(self, *args, **kwargs):
        """Satisfy servers that this url is a 404"""
        self.set_status(404)
        self.finish()
