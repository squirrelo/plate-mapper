# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import main

from platemap.tests_website.tornado_test_base import TestHandlerBase
from platemap.lib.util import rollback_tests
import platemap as pm


@rollback_tests()
class TestAddProjectHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/project/add/')
        self.assertEqual(obs.code, 200)
        self.assertIn('<input type="submit" value="Create Project">',
                      obs.body.decode('utf-8'))

    def test_post_no_barcode(self):
        obs = self.post('/project/add/', {'name': 'newtestproj',
                                          'description': 'desc',
                                          'pi': 'pi',
                                          'contact': 'cont',
                                          'sample_set': 'sampset',
                                          'barcodes': ''})
        self.assertEqual(obs.code, 200)
        self.assertIn('Successfully created project "newtestproj"',
                      obs.body.decode('utf-8'))
        self.assertTrue(pm.project.Project.exists('newtestproj'))

    def test_post_barcode(self):
        obs = self.post('/project/add/', {'name': 'newtestproj',
                                          'description': 'desc',
                                          'pi': 'pi',
                                          'contact': 'cont',
                                          'sample_set': 'sampset',
                                          'barcodes': '2'})
        self.assertEqual(obs.code, 200)
        self.assertIn('Successfully created project "newtestproj"',
                      obs.body.decode('utf-8'))
        self.assertTrue(pm.project.Project.exists('newtestproj'))

    def test_post_error(self):
        obs = self.post('/project/add/', {'name': 'atestproj',
                                          'description': 'desc',
                                          'pi': 'pi',
                                          'contact': 'cont',
                                          'sample_set': 'sampset',
                                          'barcodes': '12'})
        self.assertEqual(obs.code, 200)
        self.assertIn('12 barcodes requested, only 6 available',
                      obs.body.decode('utf-8'))
        self.assertFalse(pm.project.Project.exists('atestproj'))


@rollback_tests()
class TestViewProjectHandler(TestHandlerBase):
    def test_get(self):
        obs = self.get('/project/view/')
        self.assertEqual(obs.code, 200)
        self.assertIn('<option value="2">Project 2</option>',
                      obs.body.decode('utf-8'))

    def test_post(self):
        obs = self.post('/project/view/', {'project-id': 2})
        self.assertEqual(obs.code, 200)
        self.assertIn('<h4>Sample Set 2</h4>',
                      obs.body.decode('utf-8'))

    def test_post_unknown(self):
        obs = self.post('/project/view/', {'project-id': 12321312})
        self.assertEqual(obs.code, 200)
        self.assertEqual('', obs.body.decode('utf-8'))


if __name__ == '__main__':
    main()
