# noinspection PyStatementEffect
{
    'name': "Stock Client Order Ref",

    'summary': """Adds a customer reference field to the stock picking record""",

    'author': "Arxi",
    'website': "http://www.arxi.pt",

    'category': 'Warehouse',
    'version': '12.0.0.0.2',
    'license': 'OPL-1',

    'price': 0.00,
    'currency': 'EUR',

    'depends': ['stock', 'sale'],

    'data': [
        'views/stock_picking_views.xml',
        'report/stock_picking_templates.xml'
    ],

    'images': [
        'static/description/banner.png',
    ],
}
