# -*- coding: utf-8 -*-
# Copyright 2018 Aurium Technologies.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Change product quantities on hand in mass',
    'summary': """
        This helps you to quickly change quantites on hand for multiple products simultanously.""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Aurium Technologies',
    'website': 'www.auriumtechnologies.com',
    'depends': [
        'stock',
    ],
    'data': [
        'wizard/bulk_quantity_change.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
