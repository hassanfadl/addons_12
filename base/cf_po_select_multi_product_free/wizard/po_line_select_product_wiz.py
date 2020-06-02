from odoo import api, fields, models, SUPERUSER_ID, _

class PoSelectProductWiz(models.TransientModel):
    _name = 'po.select.product.wiz'
    _description = 'Add multi products in purchase order lines'

    purchase_order_id = fields.Many2one('purchase.order', 'Purchase Order Id')
    product_ids = fields.Many2many("product.product", "purchase_product_rel", "wiz_id", "product_id",
                                     string="Products", domain=[('purchase_ok', '=', True)])
    scheduled_date = fields.Datetime('Scheduled Date', required=True,default=fields.Datetime.now)

    ##### Fetch the Product line Name ####
    @api.multi
    def fetch_product_line_name(self,product_id):
        product_lang = product_id.with_context(
            lang=self.purchase_order_id.partner_id.lang,
            partner_id=self.purchase_order_id.partner_id.id,
        )
        product_name = product_lang.display_name
        if product_lang.description_purchase:
            product_name += '\n' + product_lang.description_purchase
        return product_name

    ##### Fetch the Taxes ####
    @api.multi
    def fetch_product_line_taxes(self, product_id):
        fpos = self.purchase_order_id.fiscal_position_id
        if self.env.uid == SUPERUSER_ID:
            company_id = self.env.user.company_id.id
            taxes_id = fpos.map_tax(product_id.supplier_taxes_id.filtered(lambda r: r.company_id.id == company_id))
        else:
            taxes_id = fpos.map_tax(product_id.supplier_taxes_id)
        return taxes_id

    ##### Fetch the Price ####
    @api.multi
    def fetch_product_line_price_unit(self, product_id):
        price_unit = 0.0
        params = {'order_id': self.purchase_order_id}
        uom = product_id.uom_po_id or product_id.uom_id
        seller = product_id._select_seller(
            partner_id=self.purchase_order_id.partner_id,
            quantity=1,
            date=self.purchase_order_id.date_order and self.purchase_order_id.date_order.date(),
            uom_id=uom,
            params=params)

        if not seller:
            if product_id.seller_ids.filtered(lambda s: s.name.id == self.purchase_order_id.partner_id.id):
                price_unit = 0.0
            return price_unit

        taxes_id = self.fetch_product_line_taxes(product_id)
        price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price,
                                                                             product_id.supplier_taxes_id,
                                                                             taxes_id,
                                                                             self.purchase_order_id.company_id) if seller else 0.0
        if price_unit and seller and self.purchase_order_id.currency_id and seller.currency_id != self.purchase_order_id.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, self.purchase_order_id.currency_id, self.purchase_order_id.company_id, self.purchase_order_id.date_order or fields.Date.today())

        if seller and uom and seller.product_uom != uom:
            price_unit = seller.product_uom._compute_price(price_unit, uom)
        return price_unit

    ##### Create Purchase line ####
    @api.multi
    def create_po_line(self, product_id):
        po_line_obj = self.env['purchase.order.line']
        for rec in self:
            product_name = rec.fetch_product_line_name(product_id)
            taxes_id = rec.fetch_product_line_taxes(product_id)
            price_unit = rec.fetch_product_line_price_unit(product_id)
            po_line_obj.create({'product_id': product_id.id,
                                'name': product_name,
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'date_planned': rec.scheduled_date,
                                'order_id': rec.purchase_order_id.id,
                                'product_qty': 1, 'price_unit': price_unit,
                                'taxes_id': [(6, 0, taxes_id.ids)]
                                })
        return True

    @api.multi
    def process(self):
        for rec in self:
            for product_id in rec.product_ids:
                rec.create_po_line(product_id)
        return {'type': 'ir.actions.act_window_close'}
