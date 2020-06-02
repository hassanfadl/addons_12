from odoo import models, fields

class account_invoice(models.Model):
    _inherit = "account.invoice"

    transaction_number = fields.Char(string="Transaction")
    

