# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': "Discuss Extended",
    "summary": "Extended view for chatter ",
    'category': 'Discuss',
    'version': "12.0.1.0.0",
    "author": "Entrivis Tech Pvt. Ltd.",
    'website': 'https://entrivistech.com',
    'depends': ['web', 'mail'],
    'data': [
        'views/web_assests_view.xml',
        'views/discuss_extended_view.xml',
    ],
    'qweb': [
        'static/src/xml/discuss_extended.xml',
    ],
    'images': [
        'static/description/images.jpeg'
    ],
    'license': 'LGPL-3',
    'auto_install': False,
    'installable': True,
    'web_preload': True,
}