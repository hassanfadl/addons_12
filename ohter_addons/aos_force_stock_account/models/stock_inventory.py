# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models, _
from datetime import datetime 
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero, float_compare

class stock_inventory(models.Model):
    _inherit = 'stock.inventory' 
    
    adjustment_type = fields.Selection([
        ('out_invoice', 'Receivable'),
        ('in_invoice', 'Payable'),
        ('initial', 'Initial Stock'),
        ('regular', 'Regular'),
        ('consume', 'Consume')], string='Adjustment Type', default='regular', help='Check this if you want to adjust to', 
        readonly=True, states={'draft': [('readonly', False)]})
    account_force_id = fields.Many2one('account.account',
        'Force Account', states={'draft': [('readonly', False)]}, help="Choose the accounting at which you want to value the stock "
             "moves created by the inventory instead of the default one")

class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"
    
    def _get_move_values(self, qty, location_id, location_dest_id, out):
        vals = super(InventoryLine, self)._get_move_values(qty=qty, location_id=location_id, location_dest_id=location_dest_id, out=out)
        #print ('====ssss==11==',vals)
        if self.inventory_id.accounting_date:
            vals['date'] = self.inventory_id.accounting_date    
        return vals