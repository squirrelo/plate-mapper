# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------


class PlateMapperError(Exception):
    """Base class for all plate mapper exceptions"""
    pass


class DeveloperError(PlateMapperError):
    """A developer did something they should not have"""
    pass


class UnknownIDError(PlateMapperError):
    """Exception for error when an object does not exists in the DB"""
    def __init__(self, missing_id, table):
        super(UnknownIDError, self).__init__()
        self.args = ("The object with ID '%s' does not exist in table '%s'"
                     % (missing_id, table),)


class DuplicateError(PlateMapperError):
    """Exception for error when an object already exists in the DB"""
    def __init__(self, external_name, table):
        super(DuplicateError, self).__init__()
        self.args = ("The object with name '%s' already exists in table '%s'"
                     % (external_name, table),)


class AssignError(PlateMapperError):
    """Trying to assign a value to something that can not change"""
    pass


class EditError(PlateMapperError):
    """Exception for error when trying to edit a finalized object"""
    def __init__(self, id_):
        super(EditError, self).__init__()
        self.args = ("The object with ID '%s' is finalized and can not be "
                     "edited" % str(id_),)
