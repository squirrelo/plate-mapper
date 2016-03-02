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


class CreateProjectHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('add_project.html', msg='')

    @authenticated
    def post(self):
        name = self.get_argument('name')
        description = self.get_argument('description')
        pi = self.get_argument('pi')
        contact = self.get_argument('contact')
        sample_set = self.get_argument('sample_set')
        num_barcodes = self.get_argument('barcodes', None)

        try:
            num_barcodes = int(num_barcodes) if num_barcodes else None
            pm.project.Project.create(
                name, description, self.current_user.person, pi,
                contact, sample_set, num_barcodes)
        except Exception as e:
            msg = str(e)
        else:
            msg = 'Successfully created project "%s"' % name
        self.render('add_project.html', msg=msg)


class ViewProjectHandler(BaseHandler):
    @authenticated
    def get(self):
        projects = pm.project.Project.projects()
        self.render('view_project.html', projects=projects)

    @authenticated
    def post(self):
        pid = int(self.get_argument('project-id'))
        try:
            project = pm.project.Project(pid)
        except pm.exceptions.UnknownIDError:
            self.write('')
            return
        self.render('render_project.html', samples=project.samples,
                    project=project.name)
