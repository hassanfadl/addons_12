# -*- coding: utf-8 -*-
{
    'name': 'Mail Messages Buttons.'
            ' Move buttons on Mail Message Form to header',
    'version': '12.0.1.1',
    'summary': """Optional extension for free 'Mail Messages Easy' app""",
    'author': 'Ivan Sokolov, Cetmix',
    'category': 'Discuss',
    'license': 'LGPL-3',
    'website': 'https://cetmix.com',
    'description': """
Mail Messages
""",
    'depends': ['prt_mail_messages'],
    'images': ['static/description/banner_buttons.png'],
    'data': [
        'views/prt_mail_buttons.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
