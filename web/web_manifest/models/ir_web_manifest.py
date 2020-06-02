# Part of web_pwa module. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class IrWebManifest(models.Model):
    _name = 'ir.web.manifest'
    _description = 'App manifest settings'

    name = fields.Char(required=True, default='Odoo')
    short_name = fields.Char(required=True, default='Odoo')
    app_id = fields.Char(default='odoo-1', required=True)
    app_version = fields.Integer(default=1, required=True, readonly=True)
    description = fields.Char(default='Odoo application')
    lang_id = fields.Many2one(
        comodel_name='res.lang',
        default=lambda self: self.env['res.lang']._lang_get(self.env.context.get('lang', 'en_US')),
        required=True
    )

    @api.multi
    def get_manifest_data(self):
        self.ensure_one()
        return {
            'id': self.app_id,
            'name': self.name,
            'lang': self.lang_id.iso_code,
            'short_name': self.short_name,
            'description': self.description,
            'version': str(self.app_version)
        }

    @api.multi
    def upgrade_version(self):
        for record in self:
            record.write({'app_version': record.app_version + 1})
