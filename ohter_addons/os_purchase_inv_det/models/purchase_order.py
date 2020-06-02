# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def get_invoice_amount(self):
        for purchase_id in self:
            purchase_id.invoice_due = 0
            purchase_id.invoice_total = 0
            for invoice_id in purchase_id.invoice_ids:
                if invoice_id.state not in ['draft', 'cancelled']:
                    purchase_id.invoice_due += invoice_id.residual
                    purchase_id.invoice_total += invoice_id.amount_total

    invoice_due = fields.Monetary(
        string='Invoice Due', compute='get_invoice_amount')
    invoice_total = fields.Monetary(
        string='Total Invoiced', compute='get_invoice_amount')
