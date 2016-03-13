plate-mapper
============

[![Build Status](https://travis-ci.org/squirrelo/plate-mapper.svg?branch=master)](https://travis-ci.org/squirrelo/plate-mapper)
[![Coveralls Status](https://coveralls.io/repos/squirrelo/plate-mapper/badge.png?branch=master)](https://coveralls.io/r/squirrelo/plate-mapper)

Knight lab internal sample and protocol tracking. Used to track all wet lab information for prep metadata generation

Requirements
============
 - Python 3
 - Postgres 9.3+

Setup
=====
 1) Install using setup.py
 
 2) Copy `platemap_config.txt.example` to `platemap_config.txt` in the same folder. Update settings in the new copy to match your system.
 
 2) Initialize the database by calling `platemap make`. You can optionallly add a `-t` flag to set the database to test mode and populate with test data.
 
 3) Start the webserver by calling `python webserver.py`. Navigate to `http://localhost:7778` in your browser to start using the tool. If you have populated with the test data, the username is `User1` and password is `password`. 
