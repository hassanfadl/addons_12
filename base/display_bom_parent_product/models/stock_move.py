# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class StockMove(models.Model):

    _inherit = "stock.move"

    mo_sequence = fields.Char(string="MO Sequence", store=True)
