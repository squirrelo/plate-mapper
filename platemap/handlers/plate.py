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
            '384 well': (12, 24),
        }

        plate = pm.plate.Plate.create(barcode, name, self.current_user,
                                      *plates[plate])

        self.redirect('/plate/edit/%d' % plate.id)


class PlateEditHandler(BaseHandler):
    @authenticated
    def get(self):
        pass