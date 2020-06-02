# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Qweb Picking Slip',
    'version': '12.0.0.1.0',
    'license': 'AGPL-3',
    'category': 'Warehouse',
    'sequence': 1,
    'author': "Alphasoft",
    'summary': 'Form Qweb Picking Slip',
    'website': 'https://www.alphasoft.co.id/',
    'images':  ['images/main_screenshot.png'],
    'description': """ """,
    'depends': ['stock'],
    'data': [
        'report/picking_slip_report_view.xml',
        'report/report_view.xml',
        ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
