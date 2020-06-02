# -*- coding: utf-8 -*-
{
    'name': "CJ Mail Limit",
    'summary': """Mail limit module""",
    'description': """
Add configuration to set send mail limit
========================================
- Go to settings -> General Settings -> Mail Send Limit. Set limit value when mail scheduler run.
    """,
    'author': "CakJuice",
    'website': "https://cakjuice.com",
    'category': 'Discuss',
    'version': '12.0.1',
    'images': [
        'static/description/main_screenshot.png',
        'static/description/ss_configuration.png',
    ],
    'depends': [
        'mail',
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}