# -*- coding: utf-8 -*-
# Copyright 2018  Aurium Technologies
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from odoo.tools.translate import _



class ProductQuantityWizard(models.TransientModel):
    _name = 'wizard.product.change_quantities'
    _description = 'Set quantity on hand wizard'

    location_id = fields.Many2one('stock.location', string="Location", required=True, domain="[('usage', '=', 'internal')]")
    new_quantity = fields.Float(string="New Quantity", default=1, required=True)

    @api.constrains('new_quantity')
    def check_new_quantity(self):
        if any(record.new_quantity < 0 for record in self):
            raise UserError(_('Quantity cannot be negative.'))


    @api.multi
    def change_quantities(self):
        company_id = self.env.user.company_id.id
        context = dict(self._context or {})
        products = self.env['product.product'].browse(context.get('active_ids'))
        Inventory = self.env['stock.inventory']

        for product in products :
            product_with_context = product.with_context(location=self.location_id.id)
            th_qty = product_with_context.qty_available

            inv_line = {
               'product_qty': self.new_quantity,
               'location_id': self.location_id.id,
               'product_id': product.id,
               'product_uom_id': product.uom_id.id,
               'theoretical_qty': th_qty,
            }

            inventory = Inventory.create({
                'name': _('INV: %s') % ' INITIAL ',
                'filter': 'product',
                'product_id': product.id,
                'location_id': self.location_id.id,
                'line_ids': [(0, 0, inv_line)],
            })
        
            inventory.action_validate()
        
        return {'type': 'ir.actions.act_window_close'}

 


