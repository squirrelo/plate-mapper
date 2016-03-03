# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from tornado.web import authenticated

from platemap.handlers.base import BaseHandler
import platemap as pm


class RunPageHandler(BaseHandler):
    @authenticated
    def get(self):
        runs = pm.run.Run.runs()
        self.render('view_run.html', runs=runs, msg='')

    @authenticated
    def post(self):
        name = self.get_argument('name')
        try:
            pm.run.Run.create(name, self.current_user.person)
        except Exception as e:
            msg = str(e)
        else:
            msg = 'Successfuly created run "%s"' % name

        runs = pm.run.Run.runs()
        self.render('view_run.html', runs=runs, msg=msg)


class RenderRunHandler(BaseHandler):
    @authenticated
    def get(self, run_id):
        run = pm.run.Run(int(run_id))
        self.render('render_run.html', run=run)


class PoolPageHandler(BaseHandler):
    @authenticated
    def get(self):
        pools = pm.run.Pool.pools()
        runs = pm.run.Run.runs()
        self.render('view_pool.html', runs=runs, pools=pools, msg='')

    @authenticated
    def post(self):
        name = self.get_argument('name')
        run = int(self.get_argument('run'))
        try:
            pm.run.Pool.create(name, pm.run.Run(run), self.current_user.person)
        except Exception as e:
            msg = str(e)
        else:
            msg = 'Successfuly created run "%s"' % name

        pools = pm.run.Pool.pools()
        runs = pm.run.Run.runs()
        self.render('view_pool.html', runs=runs, pools=pools, msg=msg)


class RenderPoolHandler(BaseHandler):
    @authenticated
    def get(self, pool_id):
        pass
