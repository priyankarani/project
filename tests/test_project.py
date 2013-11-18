#!/usr/bin/env python
#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

import sys
import os
DIR = os.path.abspath(os.path.normpath(os.path.join(__file__,
    '..', '..', '..', '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import unittest
import trytond.tests.test_tryton
from trytond.transaction import Transaction
from trytond.tests.test_tryton import test_view, test_depends, DB_NAME, USER, POOL, CONTEXT


class ProjectTestCase(unittest.TestCase):
    '''
    Test Project module.
    '''

    def setUp(self):
        trytond.tests.test_tryton.install_module('project')

    def test0005views(self):
        '''
        Test views.
        '''
        test_view('project')

    def test0006depends(self):
        '''
        Test depends.
        '''
        test_depends()

    def test0010active(self):
        '''
        Test Active Field changes
        '''
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            Work = POOL.get('timesheet.work')
            ProjectWork = POOL.get('project.work')
            Company = POOL.get('company.company')
            Currency = POOL.get('currency.currency')
            Party = POOL.get('party.party')

            currency, = Currency.create([{
                'name': 'US Dollar',
                'code': 'USD',
                'symbol': '$',
            }])
            company_party, = Party.create([{
                'name': 'Openlabs',
            }])
            company, = Company.create([{
                'party': company_party.id,
                'currency': currency.id,
            }])

            work1, = Work.create([{
                'name': 'Test Project1',
                'company': company.id,
            }])
            work2, = Work.create([{
                'name': 'Test Project2',
                'company': company.id,
            }])
            work3, = Work.create([{
                'name': 'Test Project3',
                'company': company.id,
            }])
            self.assertEqual(Work.search([], count=True), 3)

            work1.active = False
            work1.save()
            self.assertEqual(Work.search([], count=True), 2)





def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProjectTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
