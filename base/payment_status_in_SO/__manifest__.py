# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software PVT. LTD.
# mail:   odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
#           Aktiv Software:
#              - Parth Dave
#              - Surabh Yadav
#              - Tanvi Gajera
{
    'name': "Payment Status in Sale Order",
    'website': "http://www.aktivsoftware.com",
    'category': 'Website',
    'version': '12.0.0.0.0',
    'license': 'AGPL-3',
    'summary': 'Payment Status in Sale Order',
    'description': """
Title: Payment Status in Sale Order \n
Display the currnet payment status from website\n
and display into the sale order
""",
    'author': 'Aktiv Software',
    'depends': ['base', 'website_sale_management', 'web', 'sale_management'],
    'css': [],
    'data': [
        'views/sale_order_view.xml',
    ],
    'images': [
        'static/description/banner.jpg'
    ],
    'installable': True,
    'auto_install': False,
}
