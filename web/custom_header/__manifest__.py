# -*- coding: utf-8 -*-
{
    'name': "Custom Header",

    'summary': """
	This module is developed to customise the colour of the header,button's colour and highlight the mandatory fields
    in the odoo default theme. The process is done under maintenance of oodles technologies.""",

    'description': """
        Change color of default odoo color theme
    """,

    'author': "Sahil Dwivedi",
    'website': "https://github.com/Sahildwivedi",
    "license": "LGPL-3",
    "support": "sahildwivedi857@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Theme',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/header.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
