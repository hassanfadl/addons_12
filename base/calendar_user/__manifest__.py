# -*- coding: utf-8 -*-
# module template
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Calendar User',
    'version': '12.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'author': "Odoo Tips",
    'website': 'https://www.facebook.com/OdooTips/',
    'summary': 'Show the name of the user who Created the event in the Calendar View',
    'depends': ['base', 'calendar',
                ],

    'images': ['images/main_screenshot.png'],
    'data': [
             'views/calendar_view.xml',
             ],
    'installable': True,
    'application': True,
}
