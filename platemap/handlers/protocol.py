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
            plates = pm.plate.Plate.plates(finalized=True)
            self.render('log_extraction.html', plates=plates, msg=str(e))
        else:
            self.redirect('/?msg=Successfully+logged+extraction+run')


class LogPCRHandler(BaseHandler):
    @authenticated
    def get(self):
        plates = pm.webhelp.get_extraction_plates()
        self.render('log_pcr.html', plates=plates, msg='')

    def post(self):
        plate_id = self.get_argument('plate-id')
        ex_id = self.get_argument('extraction-id')
        primer_lot = self.get_argument('primer_lot')
        mastermix_lot = self.get_argument('mastermix_lot')
        water_lot = self.get_argument('water_lot')
        processing_robot = self.get_argument('processing_robot')
        tm300_8_tool = self.get_argument('tm300_8_tool')
        tm50_8_tool = self.get_argument('tm50_8_tool')

        try:
            pm.protocol.PCRProtocol.create(
                self.current_user.person,
                pm.protocol.ExtractionProtocol(ex_id), primer_lot,
                mastermix_lot, water_lot, processing_robot, tm300_8_tool,
                tm50_8_tool, plate=pm.plate.Plate(plate_id))
        except Exception as e:
            # Render any error to the user interface
            plates = pm.webhelp.get_extraction_plates()
            self.render('log_pcr.html', plates=plates, msg=str(e))
        else:
            self.redirect('/?msg=Successfully+logged+PCR+run')
