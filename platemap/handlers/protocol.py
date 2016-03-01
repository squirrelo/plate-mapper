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


class LogExtractionHandler(BaseHandler):
    @authenticated
    def get(self):
        plates = pm.plate.Plate.plates(finalized=True)
        self.render('log_extraction.html', plates=plates, msg='')

    @authenticated
    def post(self):
        plate_id = self.get_argument('plate-id')
        extract_lot = self.get_argument('extractionkit_lot')
        extract_robot = self.get_argument('extraction_robot')
        tm_tool = self.get_argument('tm1000_8_tool')

        try:
            pm.protocol.ExtractionProtocol.create(
                self.current_user.person, extract_lot, extract_robot,
                tm_tool, plate=pm.plate.Plate(plate_id))
        except Exception as e:
            # Render any error to the user interface
            msg = self.write(str(e))
            plates = pm.plate.Plate.plates(finalized=True)
            self.render('log_extraction.html', plates=plates, msg=msg)
        else:
            self.redirect('/?msg=Successfully+logged+PCR+run')
