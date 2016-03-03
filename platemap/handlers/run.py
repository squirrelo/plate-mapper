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


class GeneratePrepTemplate(BaseHandler):
    @authenticated
    def get(self, run_id):
        # write out prep metadata
        self.add_header('Content-type', 'application/octet-stream')
        self.add_header('Content-Transfer-Encoding', 'binary')
        self.add_header('Accept-Ranges', 'bytes')
        self.add_header('Content-Encoding', 'none')
        self.add_header('Content-Disposition',
                        'attachment; filename=prep_metadata.txt')
        self.write(pm.run.Run(int(run_id)).generate_prep_metadata())
        self.flush()
        self.finish()


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
        pool_id = self.get_argument('pool_id', None)
        pools = pm.run.Pool.pools()
        runs = pm.run.Run.runs()
        self.render('view_pool.html', runs=runs, pools=pools, pool_id=pool_id,
                    msg='')

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
