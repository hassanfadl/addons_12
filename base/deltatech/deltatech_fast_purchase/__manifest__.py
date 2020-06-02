# -*- coding: utf-8 -*-
# ©  2015-2019 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

{
    "name": "Fast Purchase",
    'version': '12.0.1.0.0',
    "author": "Terrabit, Dorin Hongu",
    "website": "https://www.terrabit.ro",
    'summary': 'Achizitie rapida',


    "category": "Purchases",
    "depends": [
        "base",
        "purchase_stock",
        "stock"
    ],

    "license": "LGPL-3",
    "data": [
        'views/purchase_view.xml',
        'views/stock_view.xml'
    ],
    "images": ['images/main_screenshot.png'],

    "installable": True,
}
