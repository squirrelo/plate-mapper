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


class PlateRenderHandler(BaseHandler):
    @authenticated
    def get(self, plate_id):
        if not plate_id:
            # Blank info sent, so send blank info back
            self.write('')
            return

        plate = pm.plate.Plate(plate_id)
        self.render('render_plate.html', platemap=plate.platemap,
                    plate_id=plate_id, plate_name=plate.name,
                    finalized=plate.finalized)
