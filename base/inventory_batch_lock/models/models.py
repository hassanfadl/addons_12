# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv import expression


class StockQuant(models.Model):
    _inherit = "stock.quant"
    
    def _gather(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False):
        if lot_id:
            return super(StockQuant, self)._gather(product_id, location_id, lot_id, package_id, owner_id, strict)
        else:
            return super(StockQuant, self.with_context(exclude_locked=1))._gather(product_id, location_id, lot_id, package_id, owner_id, strict)
    
    
    @api.model
    def _where_calc(self, domain, active_test=True): 
        if self.env.context.get('exclude_locked'):
            domain = expression.AND([[('lot_id.state', '=', 'unlocked')], domain])
        return super(StockQuant, self)._where_calc(domain,active_test)
    
    
class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"
    
    state = fields.Selection([('unlocked', 'Unlocked'), ('locked', 'Locked')], default='unlocked', required=True, track_visibility='always')
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        args = expression.AND([[('state', '=', 'unlocked')], args])
        return super(StockProductionLot, self).name_search(name, args, operator, limit)
    
    def action_lock(self):
        self.write({'state':'locked'})
    
    def action_unlock(self):
        self.write({'state':'unlocked'})
