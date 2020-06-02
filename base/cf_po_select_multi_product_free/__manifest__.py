# -*- coding: utf-8 -*-
{
    'name': 'Purchase Order Multi Product Selection-Free',
    'version': '1.0',
    'category': 'Purchases',
    'description': """
            Add Multi Products in Purchase Order lines from Purchase Order.
            Create Purchase Order of multi product selected from product list view.
            
            """,
    'author': 'CodeFire Technologies',
    'website': 'https://www.codefire.org/',
    'license': 'AGPL-3',
    'images': ['static/description/odoo-free.jpg'],
    'depends': [
        'purchase','account'
    ],
    'data': [
        'security/security.xml',
        'wizard/po_line_select_product_wiz_view.xml',
        'wizard/po_create_wiz_view.xml',
        'views/product_view.xml',
        'views/purchase_view.xml',
        'security/ir.model.access.csv',

    ],
}
