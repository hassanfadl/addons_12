# -*- coding: utf-8 -*-
{
    'name': 'SW - Inventory Batch Lock',
    'version': '12.0.1.0',
    'category': 'Warehouse',
    'summary': 'Prevent auto quantity reservation for certain batches by locking them',
    'description': """Lock particular batches to prevent quantity reservation on DOs.
""",
    'license':  "Other proprietary",
    'author' : 'Smart Way Business Solutions',
    'website' : 'https://www.smartway.co',
    'depends': ['base','stock'],
    'data': [
             'views/views.xml',
             ],
    "images":  ['static/description/image.png'],
}
