# -*- coding: utf-8 -*-
{
    'name': "data clean,clean data, smart clean,智能数据清理",
    'summary': """
        clean data smart data clean,智能数据清理""",

    'description': """
        Easy to clean odoo test datas, smart to define the relation model want to clean, don't clean the external identifiers datas.
        智能数据清理,方便定义一键清楚业务数据,但不删除外部数据记录.
    """,

    'author': "jon<alangwansui@qq.com>",
    'website': "http://47.104.249.25",

    'category': 'tools',
    'version': '1.0',
    'license': 'OPL-1',

    'depends': ['base', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/clean_setting.xml',
        'wizards/wizard_clean_line.xml',
    ],

    'images': [
        'static/description/theme.jpg',
    ],

    'installable': True,
    'active': True,
    'price': 0,
    'currency': 'EUR',
    'auto_install': False,

}