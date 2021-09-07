# -*- coding: utf-8 -*-
{
    'name': 'Periodic Purchase Report',
    'version': '12.0',
    'category': 'Purchase',
    'author': 'Preciseways',
    'website': "https://www.preciseways.com",
    'summary': "Periodic purchase information on basic of vendors",
    'description': """Information about all purchase products vendors wise 
                    in the period of daily, weekly and monthly""",
    'depends': ['purchase'],
    'data': [
        'wizard/daily_purchase_report_view.xml',
        'report/report.xml',
        'report/daily_purchase_report_template.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'images':['static/description/banner.png'],
    'live_test_url': 'https://preciseways.com',
    'license': 'OPL-1',
}
