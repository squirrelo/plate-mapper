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


class PlateCreateHandler(BaseHandler):
    @authenticated
    def get(self):
        plates = ['96 well', '384 well']
        self.render('add_plate.html', plates=plates)

    @authenticated
    def post(self):
        barcode = self.get_argument('barcode')
        name = self.get_argument('name')
        plate = self.get_argument('plate')
        plates = {
            '96 well': (8, 12),
            '384 well': (16, 24)
        }

        plate = pm.plate.Plate.create(barcode, name, self.current_user.person,
                                      *plates[plate])

        self.redirect('/plate/edit/?plate=%s' % plate.id)


class PlateEditHandler(BaseHandler):
    @authenticated
    def get(self):
        plate_id = self.get_argument('plate', None)
        plates = pm.plate.Plate.plates()
        self.render('edit_plate.html', plates=plates, plate_id=plate_id)


class PlateEditableRenderHandler(BaseHandler):
    @authenticated
    def get(self, plate_id):
        if not plate_id:
            # Blank info sent, so send blank info back
            self.write('')
            return

        override = self.current_user.check_access('Override')
        if override:
            sets = pm.project.Project.all_sample_sets()
            types = pm.sample.Sample.types()
            locations = pm.sample.Sample.locations()
        else:
            sets, types, locations = [], [], []
        plate = pm.plate.Plate(plate_id)
        self.render('render_plate.html', platemap=plate.platemap,
                    plate_id=plate_id, plate_name=plate.name,
                    finalized=plate.finalized, sets=sets, types=types,
                    locations=locations, override=override)


class PlateStaticRenderHandler(BaseHandler):
    @authenticated
    def get(self, plate_id):
        if plate_id:
            self.write(pm.plate.Plate(plate_id).to_html())
        else:
            self.write('')


class PlateUpdateHandler(BaseHandler):
    @authenticated
    def post(self):
        plate_id = self.get_argument('plate_id')
        action = self.get_argument('action')

        if action == 'finalize':
            pm.plate.Plate(plate_id).finalize()
            return
        elif action == 'update':
            row, col = map(int, self.get_argument('rowcol').split('-', 1))
            samp_name = self.get_argument('sample')

            sample = pm.sample.Sample.search(name=samp_name)
            if not sample:
                self.write('Could not find sample "%s"' % samp_name)
                return
            try:
                pm.plate.Plate(plate_id)[row, col] = sample[0]
                self.write('')
            except Exception as e:
                # Catch any error and show to user
                self.write(str(e))
            return
        else:
            raise HTTPError(400, 'Unknown action %s' % action)


class PlateRevertHandler(BaseHandler):
    @authenticated
    def get(self):
        plates = pm.plate.Plate.plates(finalized=True)
        self.render('revert_plate.html', plates=plates, msg='')

    @authenticated
    def post(self):
        plate_id = self.get_argument('plate-id')
        msg = "Successfully reverted %s" % plate_id
        try:
            pm.webhelp.revert_plate(self.current_user, plate_id)
        except Exception as e:
            msg = "ERROR: " + str(e)

        plates = pm.plate.Plate.plates(finalized=True)
        self.render('revert_plate.html', plates=plates, msg=msg)
