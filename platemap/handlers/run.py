# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from tornado.web import authenticated, HTTPError

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
        instruments = pm.webhelp.get_instruments()
        self.render('view_run.html', runs=runs, instruments=instruments,
                    msg='')

    @authenticated
    def post(self):
        action = self.get_argument('action')

        if action == "create":
            name = self.get_argument('name')
            instrument = self.get_argument('instrument')
            try:
                pm.run.Run.create(name, self.current_user.person, instrument)
            except Exception as e:
                msg = str(e)
            else:
                msg = 'Successfuly created run "%s"' % name
        elif action == "finalize":
            run_id = int(self.get_argument('run'))
            try:
                run = pm.run.Run(run_id)
                run.finalize(self.current_user.person)
            except Exception as e:
                msg = str(e)
            else:
                msg = 'Successfuly finalized run "%s"' % run.name
        else:
            raise HTTPError(400, 'Unknown action %s' % action)

        runs = pm.run.Run.runs()
        instruments = pm.webhelp.get_instruments()
        self.render('view_run.html', runs=runs, instruments=instruments,
                    msg=msg)


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
        action = self.get_argument('action')
        if action == 'create':
            name = self.get_argument('name')
            run = int(self.get_argument('run'))
            try:
                pm.run.Pool.create(name, pm.run.Run(run),
                                   self.current_user.person)
            except Exception as e:
                msg = str(e)
            else:
                msg = 'Successfuly created pool "%s"' % name
        elif action == "finalize":
            pool_id = int(self.get_argument('pool'))
            try:
                pool = pm.run.Pool(pool_id)
                pool.finalize(self.current_user.person)
            except Exception as e:
                msg = str(e)
            else:
                msg = 'Successfuly finalized pool "%s"' % pool.name
        else:
            raise HTTPError(400, 'Unknown action %s' % action)

        pools = pm.run.Pool.pools()
        runs = pm.run.Run.runs()
        self.render('view_pool.html', runs=runs, pools=pools, msg=msg,
                    pool_id=None)


class RenderPoolHandler(BaseHandler):
    @authenticated
    def get(self, pool_id):
        pool = pm.run.Pool(int(pool_id))
        self.render('render_pool.html', pool=pool)
