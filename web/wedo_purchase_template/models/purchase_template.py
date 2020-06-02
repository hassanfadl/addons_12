# -*- coding: utf-8 -*-
# Copyright 2020 WeDo Technology
# Website: http://wedotech-s.com
# Email: apps@wedotech-s.com 
# Phone:00249900034328 - 00249122005009

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class PurchaseOrderTemplate(models.Model):
    _name = 'purchase.order.template'
    _description = 'Purchase Template'

    name = fields.Char(required=True)
    vendor_ids = fields.Many2many('res.partner',string='Vendors')
    po_template_line_ids = fields.One2many('purchase.order.template.line', 'po_template_id', string='Lines', copy=True)
    note = fields.Text('Terms and conditions', translate=True)
    active = fields.Boolean('Active', default=True)



class PurchaseOrderTemplateLine(models.Model):
    _name = 'purchase.order.template.line'
    _description = "Purchase Template Line"
    _order = 'po_template_id, id'

    po_template_id = fields.Many2one(
        'purchase.order.template', string='Purchase Template Reference',
        required=True, ondelete='cascade', index=True)
    name = fields.Text('Description', required=True, translate=True)
    product_id = fields.Many2one('product.product', 'Product', domain=[('purchase_ok', '=', True)])
    product_qty = fields.Float('Quantity', required=True, default=1)
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    sequence = fields.Integer('Sequence', default=10)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.ensure_one()
        if self.product_id:
            name = self.product_id.display_name
            if self.product_id.description_purchase:
                name += '\n' + self.product_id.description_purchase
            self.name = name
            self.product_uom_id = self.product_id.uom_id.id

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    po_template_id = fields.Many2one('purchase.order.template',string='Purchase template')

    @api.onchange('po_template_id')
    def onchange_po_template_id(self):
        for po in self:
            if not po.po_template_id:
                return
            po.order_line = False
            data=[]
            for line in po.po_template_id.po_template_line_ids:
                vals ={
                              'name':line.name,}
                if line.product_id:
                    vals.update({
                                      'sequence': line.sequence,
                                      'product_id':line.product_id.id,
                                      'product_qty':line.product_qty,
                                      'product_uom_qty':line.product_qty,
                                      'product_uom':line.product_uom_id.id,
                                      'product_uom_category_id':line.product_uom_category_id.id,
                                      })
                data.append((0,0,vals))

            po.order_line = data
            po.notes = po.po_template_id.note
            for line in po.order_line:
                line._onchange_quantity()
