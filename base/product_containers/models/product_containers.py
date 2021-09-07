# -*- coding: utf-8 -*-
# Part of Editor. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    container_id = fields.Many2one('product.product', string='Container Product', domain=[('container_ok','=',True)])
    max_qty = fields.Float('Contained Max Qty', help="The Max number of products you can have per pallet or box.")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    container_ok = fields.Boolean(string='Container', help='Select this if the product will act as a container to carry other products.')
    pallets_ok = fields.Boolean(string='Pallets', help='Select this if the product will act as a pallets to carry other container products.')


class ProductProduct(models.Model):
    _inherit = "product.product"

    container_id = fields.Many2one('product.product', string='Packed In', domain=[('container_ok','=',True)])
    pallets_id = fields.Many2one('product.product', string='Pallets Product', domain=[('pallets_ok','=',True)])
    pallets_qty = fields.Float('Pallets Contained Quantity', help="The total number of products you can have per pallet")
