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
        sets = ['Sample Set 1', 'Sample Set 2']
        types = pm.sample.Sample.types()
        locations = pm.sample.Sample.locations()
        self.render('add_sample.html', sets=sets, types=types,
                    locations=locations, msg='')

    @authenticated
    def post(self):
        name = self.get_argument('sample')
        barcode = self.get_argument('barcode', None)
        if not barcode:
            barcode = None
        sample_set = self.get_argument('sample-set')
        sample_type = self.get_argument('type')
        sample_location = self.get_argument('location')

        pm.sample.Sample.create(name, sample_type, sample_location, sample_set,
                                self.current_user.person, None, barcode)

        sets = ['Sample Set 1', 'Sample Set 2']
        types = pm.sample.Sample.types()
        locations = pm.sample.Sample.locations()
        self.render('add_sample.html', sets=sets, types=types,
                    locations=locations, msg='Created sample %s' % name)
