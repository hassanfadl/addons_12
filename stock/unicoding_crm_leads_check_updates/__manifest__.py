# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': u'Crm leads updates',
    'summary': "Check crm leads updates",
    'version': '1.0',
    'author': "Unicoding",
    'website': 'http://www.teambelarus.net',
    'license': 'AGPL-3',
	'depends': [
        'crm'
    ],
    'data': [
        'views/crm_lead_cron_view.xml',
    ],
    'images': [
        'static/description/img.png',
    ],
    'installable': True,
}