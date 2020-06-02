from odoo import api, fields, models, SUPERUSER_ID, _

class PoCreateWiz(models.TransientModel):
    _name = 'po.create.wiz'
    _description = 'Create purchase order'

    vendor_id = fields.Many2one('res.partner', 'Vendor', domain=[('supplier', '=', True)])
    scheduled_date = fields.Datetime('Scheduled Date', required=True, default=fields.Datetime.now)

    ##### Fetch the Product line Name ####
    @api.multi
    def fetch_product_line_name(self, product_id):
        product_lang = product_id.with_context(
            lang=self.vendor_id.lang,
            partner_id=self.vendor_id.id,
        )
        product_name = product_lang.display_name
        if product_lang.description_purchase:
            product_name += '\n' + product_lang.description_purchase
        return product_name

    ##### Fetch the Taxes ####
    @api.multi
    def fetch_product_line_taxes(self, product_id,purchase):
        fpos = purchase.fiscal_position_id
        if self.env.uid == SUPERUSER_ID:
            company_id = self.env.user.company_id.id
            taxes_id = fpos.map_tax(product_id.supplier_taxes_id.filtered(lambda r: r.company_id.id == company_id))
        else:
            taxes_id = fpos.map_tax(product_id.supplier_taxes_id)
        return taxes_id

    ##### Fetch the Price ####
    @api.multi
    def fetch_product_line_price_unit(self, product_id, purchase):
        price_unit = 0.0
        params = {'order_id': purchase}
        uom = product_id.uom_po_id or product_id.uom_id
        seller = product_id._select_seller(
            partner_id=self.vendor_id,
            quantity=1,
            date=purchase.date_order and purchase.date_order.date(),
            uom_id=uom,
            params=params)

        if not seller:
            if product_id.seller_ids.filtered(lambda s: s.name.id == self.vendor_id.id):
                price_unit = 0.0
            return price_unit
        taxes_id = self.fetch_product_line_taxes(product_id,purchase)
        price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price,
                                                                             product_id.supplier_taxes_id,
                                                                             taxes_id,
                                                                             purchase.company_id) if seller else 0.0
        if price_unit and seller and purchase.currency_id and seller.currency_id != purchase.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, purchase.currency_id, purchase.company_id,purchase.date_order or fields.Date.today())

        if seller and uom and seller.product_uom != uom:
            price_unit = seller.product_uom._compute_price(price_unit, uom)
        return price_unit

    @api.multi
    def process(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        purchase = self.env['purchase.order'].create({
                                                'partner_id': self.vendor_id.id,
                                                'state':'draft',
                                                })
        purchase.onchange_partner_id()
        for rec in self:
            vals = []
            for product_id in self.env['product.product'].browse(active_ids):
                data = dict()
                product_name = rec.fetch_product_line_name(product_id)
                taxes_id = rec.fetch_product_line_taxes(product_id,purchase)
                price_unit = rec.fetch_product_line_price_unit(product_id,purchase)
                data.update({'product_id': product_id.id,
                             'name': product_name,
                             'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                             'date_planned': rec.scheduled_date,
                             'product_qty': 1, 'price_unit': price_unit,
                             'taxes_id': [(6, 0, taxes_id.ids)]
                             })
                vals.append((0, 0, data))
            purchase.order_line = vals

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': purchase.id,
            'res_model': 'purchase.order',
            'view_id': self.env.ref('purchase.purchase_order_form').id,
        }
