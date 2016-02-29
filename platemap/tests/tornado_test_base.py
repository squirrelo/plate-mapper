from mock import Mock
from urllib.parse import urlencode

from tornado.testing import AsyncHTTPTestCase
from qiita_pet.webserver import Application

from platemap.handlers.base import BaseHandler
import platemap as pm


class TestHandlerBase(AsyncHTTPTestCase):
    database = False
    app = Application()

    def get_app(self):
        BaseHandler.get_current_user = Mock(
            return_value=pm.person.User('User1'))
        self.app.settings['debug'] = False
        return self.app

    # helpers from http://www.peterbe.com/plog/tricks-asynchttpclient-tornado
    def get(self, url, data=None, headers=None, doseq=True):
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data, doseq=doseq)
            if '?' in url:
                url += '&amp;%s' % data
            else:
                url += '?%s' % data
        return self._fetch(url, 'GET', headers=headers)

    def post(self, url, data, headers=None, doseq=True):
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data, doseq=doseq)
        return self._fetch(url, 'POST', data, headers)

    def _fetch(self, url, method, data=None, headers=None):
        self.http_client.fetch(self.get_url(url), self.stop, method=method,
                               body=data, headers=headers)
        return self.wait(timeout=10)
