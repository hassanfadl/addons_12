# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
          
    @api.one
    @api.constrains('name')
    def _check_unique_constraint(self):
        record = self.search([('name', '=ilike', self.name),('id','!=',self.id)])
        if record:
            raise ValidationError(_('Another product with the same name exists!'))
    
    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        res.name = res.name.rstrip().lstrip()
        return res
    
    @api.multi
    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].rstrip().lstrip()
        return super(ProductTemplate, self).write(vals)
