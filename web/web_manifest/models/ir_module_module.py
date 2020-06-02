# Part of web_manifest module. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    @api.multi
    def _button_immediate_function(self, function):
        self.env['ir.web.manifest'].search([]).upgrade_version()
        return super(IrModuleModule, self)._button_immediate_function(function)
