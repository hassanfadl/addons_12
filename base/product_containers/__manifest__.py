# -*- coding: utf-8 -*-
# Part of Editor. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Containers',
    'version': '12.0.1.0',
    'author': 'Editor d.o.o.',
    'price': 0,
    'currency': 'EUR',
    'sequence': 110,
    'category': 'Warehouse Management',
    'website': 'https://www.editor.si',
    'license': 'LGPL-3',
    'summary': 'Managing the container products',
    'description': """
	The module allows for efficient management and tracking of containers and pallets as products.
	The containers are physical products used to store and ship other products eg. Plastic, wooden or metal boxes, pallets, bags etc.
	They are usually returned to the seller after use, but some containers are meant for single use only and may not be returned - like cardboard boxes.
	The module is particulary useful for managing and tracking containers in which products are delivered - to be retrieved or to be sold to the customer, together with the main product.
""",
    'depends': ['product'],
    'data': [
        'views/product_containers_view.xml'
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False
}
