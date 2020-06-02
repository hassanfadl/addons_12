# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    checked = fields.Boolean(string="Checked", default=False)
    previous_color = fields.Integer(string="Color", default=222)

    @api.multi
    def write(self, vals):
        if not self.checked:
            return super(CrmLead, self).write(vals)
        if 'color' not in vals:
            if self.color == 1 and self.previous_color != 222:
                vals['color'] = self.previous_color
                vals['previous_color'] = 222
        return super(CrmLead, self).write(vals)

    @api.multi
    def update_lead_color(self):
        records = self.env['crm.lead'].search([('checked', '=', False)])
        for record in records:
            current_daytime = datetime.datetime.now()
            last_update = record.create_date
            time_delta = current_daytime - last_update
            if (time_delta.seconds/3600) >= 2:
                record.write({'color': 1, 'checked': True, 'previous_color': record.color})

