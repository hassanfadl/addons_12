# -*- coding: utf-8 -*-
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale


class ForceLogin(WebsiteSale):
    @route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        if not request.session.uid:
            return request.redirect('/web/login?redirect=/shop')
        return super(ForceLogin, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post
        )

    @route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=False)
    def product(self, product, category='', search='', **kwargs):
        if not request.session.uid:
            return request.redirect('/web/login?redirect=/shop')
        return super(ForceLogin, self).product(product, category=category, search=search, **kwargs)
