from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mail_limit = fields.Integer(string="Mail Send Limit", config_parameter='mail_limit', default=10)
