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


class SampleCreateHandler(BaseHandler):
    @authenticated
    def get(self):
        sets = ['set1', 'set2']
        types = pm.sample.Sample.types()
        locations = pm.sample.Sample.locations()
        self.render('add_sample.html', sets=sets, types=types,
                    locations=locations)
