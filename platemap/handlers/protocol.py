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
        self.render('log_extraction.html', plates=plates)
