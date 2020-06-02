# -*- coding: utf-8 -*-
{
    'name': "Vendor default list (tree) view in the purchase module", 
    'version': '12.0.0.99.15',
    'category': 'Purchases',
    'depends': ['purchase'],
    'license': 'AGPL-3',
    'summary': 'Set list (tree) as a default view for vendor in the Purchase module',
    'description': """
Changes default view of vendor to a list (tree) in the Purchase module
========================================================================
    """,
    'installable': True,
    'auto_install': False,
    'author': "odoocraft.com",
    
    
    'images': [
        'images/main_screenshot.png',
        ],
    'data': [
        'views/views.xml',
    ],
}
