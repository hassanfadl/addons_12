{
    # App information
    'name': 'Automatic Vacuum Settings',
    'version': '12.0',
    'category': 'Extra Tools',
    'license': 'OPL-1',
    'summary':'To configure an automatic vacuum cleaner to cleanup the unnecessary data.',

    # Author
    'author': 'Er. Vaidehi Vasani',
    'maintainer': 'Er. Vaidehi Vasani',

    # Dependencies
    'depends': ['base'],

    'data':[
        'data/vacuum_cron.xml',
        'views/auto_vacuum_cleaner.xml',
        'security/ir.model.access.csv'
    ],

    'images': ['static/description/auto_vacuum_system_coverpage.jpeg'],

    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 0.00,
    'currency': 'EUR',
}
