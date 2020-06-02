# -*- coding: utf-8 -*-
{
    'name': 'Purchase Invoice Details',
    'summary': 'Invoice details in purchase order form',
    'version': '12.0.1.0.0',
    'category': 'Purchases',
    'author': 'Odosquare',
    'company': 'Odosquare',
    'maintainer': 'Odosquare',
    'depends': [
        'base',
        'purchase',
    ],
    'data': [
        'views/purchase_order_views.xml',
    ],
    'images': ['static/description/banner.jpeg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
