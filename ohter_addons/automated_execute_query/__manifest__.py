
{
    'name': "Automated Execute Query",

    'summary': """
        Automated Execute Query""",

    'description': """
        You can execute query from your odoo application
    """,

    'author': "Alfatih Ridho NT",
    'website': "alfatihridhont@gmail.com",    
    'category': 'Tools',
    'version': '11.0.1',    
    'license': 'AGPL-3',
    'depends': ['base'],
    'images': ['images/main_screenshot.jpg'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/scheduler.xml',
        'views/templates.xml',
    ],    
}