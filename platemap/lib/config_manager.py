# -----------------------------------------------------------------------------
# Copyright (c) 2016--, The Plate Mapper Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from os.path import join, dirname, abspath, isfile
from os import environ
from functools import partial
import warnings

from future import standard_library
with standard_library.hooks():
    from configparser import (ConfigParser, NoOptionError,
                              Error as ConfigParser_Error)


class MissingConfigSection(ConfigParser_Error):
    """Exception when the config file is missing a required section"""
    def __init__(self, section):
        super(MissingConfigSection, self).__init__('Missing section(s): %r' %
                                                   (section,))
        self.section = section
        self.args = (section,)


def _warn_on_extra(extra, set_type):
    extra = ', '.join(extra)
    if extra:
        warnings.warn("Extra %s found: %r" % (set_type, extra))


class ConfigurationManager(object):
    """Holds the configuration information

    Parameters
    ----------
    conf_fp: str, optional
        Filepath to the configuration file. Default: platemap_config.txt

    Attributes
    ----------
    test_environment : bool
        Whether we are in a test environment or not
    cookie_secret : str
        The secret used to secure user session cookies
    user : str
        The postgres user
    password : str
        The postgres password for the previous user
    database : str
        The postgres database to connect to
    host : str
        The host where the database lives
    port : int
        The port used to connect to the postgres database in the previous host
    smtp_host
        The host where the SMTP server lives
    smtp_ssl
        Whether or not SSL connection is required by SMTP host
    smtp_port
        The port the SMTP serveris running on
    smtp_user
        The username for connecting to the SMTP server
    smtp_password
        The password for connecting to the SMTP server

    Raises
    ------
    IOError
        If the PLATEMAP_CONFIG environment variable is set, but does not point
        to anexisting file

    Notes
    -----
    - The environment variable PLATEMAP_CONFIG is checked for a path to the
    config file. If the environment variable is not set, the default config
    file isused.
    """
    def __init__(self):
        conf_fp = environ.get('PLATEMAP_CONFIG') or join(
            dirname(abspath(__file__)), '../platemap_config.txt')

        if not isfile(conf_fp):
            raise IOError("The configuration file '%s' is not an "
                          "existing file" % conf_fp)

        config = ConfigParser()

        self.defaults = set(config.defaults())

        # Parse the configuration file
        with open(conf_fp, 'U') as conf_file:
            config.readfp(conf_file)

        _expected_sections = {'main', 'postgres', 'email', 'thirdparty'}

        missing = _expected_sections - set(config.sections())
        if missing:
            raise MissingConfigSection(', '.join(missing))
        extra = set(config.sections()) - _expected_sections
        _warn_on_extra(extra, 'sections')

        self._get_main(config)
        self._get_postgres(config)
        self._get_email(config)

    def get_settings(self):
        """Returns settings that should be stored in postgres settings table

        Returns
        -------
        list of tuple
            Tuples are (parameter, argument)
        """
        return [('test_environment', self.test_environment)]

    def _get_main(self, config):
        """Get the configuration of the main section"""
        expected_options = {'test_environment', 'cookie_secret', 'error_email'}
        _warn_on_extra(set(config.options('main')) - expected_options -
                       'main section option(s)')

        get = partial(config.get, 'main')
        getboolean = partial(config.getboolean, 'main')

        self.test_environment = getboolean('TEST_ENVIRONMENT')
        self.cookie_secret = get('COOKIE_SECRET')
        self.error_email = get('ERROR_EMAIL')

    def _get_postgres(self, config):
        """Get the configuration of the postgres section"""
        expected_options = {'user', 'password', 'database', 'host', 'port'}
        _warn_on_extra(set(config.options('postgres')) - expected_options -
                       'postgres section option(s)')

        get = partial(config.get, 'postgres')
        getint = partial(config.getint, 'postgres')

        self.user = get('USER')
        try:
            self.password = get('PASSWORD')
        except NoOptionError as e:
            if self.test_environment:
                self.password = None
            else:
                raise e
        self.database = get('DATABASE')
        self.host = get('HOST')
        self.port = getint('PORT')

    def _get_email(self, config):
        get = partial(config.get, 'email')
        getint = partial(config.getint, 'email')
        getbool = partial(config.getboolean, 'email')

        self.smtp_host = get('HOST')
        self.smtp_ssl = getbool('SSL')
        self.smtp_port = getint('PORT')
        self.smtp_user = get('USERNAME')
        self.smtp_password = get('PASSWORD')

PM_CONFIG = ConfigurationManager()
