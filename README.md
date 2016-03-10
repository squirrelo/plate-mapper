plate-mapper
============

[![Build Status](https://travis-ci.org/squirrelo/plate-mapper.png)](https://travis-ci.org/squirrelo/plate-mapper)
[![Coveralls Status](https://coveralls.io/repos/squirrelo/plate-mapper/badge.png?branch=master)](https://coveralls.io/r/squirrelo/plate-mapper)

Knight lab internal sample and protocol tracking. Used to track all wet lab information for prep metadata generation

Requirements
------------
 - Python 3
 - Postgres 9.3+

 Setup
 -----
 1) Install using setup.py
 
 2) Copy `platemap_config.txt.example` to `platemap_config.txt` in the same folder. Update settings in the new copy to match your system.
 
 2) Initialize the database by calling `platemap make`. You can optionallly add a `-t` flag to populate the test database.
 
 3) Start the webserver by calling `python webserver.py`