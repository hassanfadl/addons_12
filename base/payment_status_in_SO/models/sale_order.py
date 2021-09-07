# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.

from odoo import models, fields, api, _
from odoo.tools import float_compare, UserError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    payment_ids_nbr = fields.Char(compute='_compute_payment_ids_nbr')
    payment_status = fields.Char(compute='_compute_payment_status')

    @api.multi
    def _compute_payment_status(self):
        # fetched the payment transcation
        for trans in self:
            payment_ids = self.env['payment.transaction'].search([('sale_order_ids', '=', trans.id)])
            for payment in payment_ids:
                if payment.state == 'done':
                    trans.payment_status = 'PAID'
                else:
                    trans.payment_status = 'PENDING'

    @api.multi
    def _compute_payment_ids_nbr(self):
        for trans in self:
            payment_ids = self.env['payment.transaction'].search([('sale_order_ids', '=', trans.id)])
            if payment_ids:
                # Set the payment acquire name in transcation
                trans.payment_ids_nbr = payment_ids[0].acquirer_id.name

    @api.multi
    def action_view_account_payment(self):
        for payment in self:
            payment_ids = self.env['payment.transaction'].search([('sale_order_ids', '=', payment.id)])
            action = {
                'name': _('Payment Transaction'),
                'type': 'ir.actions.act_window',
                'res_model': 'payment.transaction',
                'target': 'current',
            }
            payment_ids = payment_ids.ids
            action['view_mode'] = 'tree,form'
            action['domain'] = [('id', 'in', payment_ids)]
            # return the Payment Transaction view when matched the transcation.
            return action
