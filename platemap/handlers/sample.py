# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from io import StringIO
from tornado.web import authenticated

from platemap.handlers.base import BaseHandler
import platemap as pm


class SampleCreateHandler(BaseHandler):
    @authenticated
    def get(self):
        sets = sets = pm.project.Project.all_sample_sets()
        types = pm.sample.Sample.types()
        locations = pm.sample.Sample.locations()
        self.render('add_sample.html', sets=sets, types=types,
                    locations=locations, msg='')

    @authenticated
    def post(self):
        sample_set = self.get_argument('sample-set')
        sample_type = self.get_argument('type')
        sample_location = self.get_argument('location')

        # check if file or single sample
        if len(self.request.files) != 0:
            fileinfo = self.request.files['file'][0]
            file = StringIO(fileinfo['body'].decode('utf-8'))
            try:
                count = pm.sample.Sample.from_file(
                    file, sample_type, sample_location, sample_set,
                    self.current_user.person, None)
            except Exception as e:
                # Catch any error and show to user
                msg = str(e)
            else:
                msg = 'Created %d samples from %s' % (count,
                                                      fileinfo['filename'])
        else:
            name = self.get_argument('sample')
            barcode = self.get_argument('barcode', None)
            if not barcode:
                barcode = None
            try:
                pm.sample.Sample.create(
                    name, sample_type, sample_location, sample_set,
                    self.current_user.person, None, barcode)
            except Exception as e:
                # Catch any error and show to user
                msg = str(e)
            else:
                msg = 'Created sample %s' % name

        sets = sets = pm.project.Project.all_sample_sets()
        types = pm.sample.Sample.types()
        locations = pm.sample.Sample.locations()
        self.render('add_sample.html', sets=sets, types=types,
                    locations=locations, msg=msg)


class SampleEditHandler(BaseHandler):
    @authenticated
    def get(self):
        sample_id = int(self.get_argument('sample-id'))
        sample = pm.sample.Sample(sample_id)
        types = pm.sample.Sample.types()
        locations = pm.sample.Sample.locations()
        sample = pm.sample.Sample(sample_id)
        self.render('edit_sample.html', types=types, locations=locations,
                    sample=sample, msg='')

    @authenticated
    def post(self):
        sample_id = int(self.get_argument('sample-id'))
        sample = pm.sample.Sample(sample_id)
        sample_type = self.get_argument('type').strip()
        sample_location = self.get_argument('location').strip()
        remaining = self.get_argument('remaining', False)
        remaining = bool(remaining)
        barcode = self.get_argument('barcode', '').strip()
        msg = 'Updated successfully'

        try:
            sample.sample_type = sample_type
            sample.location = sample_location
            sample.biomass_remaining = remaining
            if barcode:
                sample.barcode = barcode
        except Exception as e:
            # Show any error to the user
            msg = 'ERROR: ' + str(e)

        types = pm.sample.Sample.types()
        locations = pm.sample.Sample.locations()
        self.render('edit_sample.html', types=types, locations=locations,
                    sample=sample, msg=msg)
