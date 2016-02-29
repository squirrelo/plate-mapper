# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from os.path import dirname, join

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line

from platemap.lib.config_manager import pm_config
from platemap.handlers.base import MainHandler, NoPageHandler
from platemap.handlers.auth import AuthLoginHandler, AuthLogoutHandler
from platemap.handlers.sample import SampleCreateHandler
from platemap.handlers.plate import PlateCreateHandler, PlateEditHandler

define("port", default=7778, help="run on the given port", type=int)


class PMApplication(Application):
    def __init__(self):
        basedir = dirname(__file__)

        handlers = [
            (r"/", MainHandler),
            (r"/static/(.*)", StaticFileHandler),
            (r"/auth/login/", AuthLoginHandler),
            (r"/auth/logout/", AuthLogoutHandler),
            # (r"/auth/create/", AuthCreateHandler),
            # (r"/auth/delete/", AuthDeleteHandler),
            # (r"/auth/profile/", UserProfileHandler),
            (r'/sample/add/', SampleCreateHandler),
            (r'/plate/add/', PlateCreateHandler),
            (r'/plate/edit/', PlateEditHandler),
            # 404 PAGE MUST BE LAST IN THIS LIST!
            (r".*", NoPageHandler)
        ]

        settings = {
            "static_path": join(basedir, "static"),
            "template_path": join(basedir, "templates"),
            "debug": pm_config.test_environment,
            "cookie_secret": pm_config.cookie_secret,
            "login_url": "/auth/login/"
        }
        Application.__init__(self, handlers, **settings)


def main():
    options.log_file_prefix = 'platemapper_%d.log' % (options.port)
    options.logging = 'warning'
    parse_command_line()
    http_server = HTTPServer(PMApplication())
    http_server.listen(options.port)
    print("Tornado started on port", options.port)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()
