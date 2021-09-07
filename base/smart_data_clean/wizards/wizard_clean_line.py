# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import Warning
from ..models.clean_setting import Not_Clean_Models

_logger = logging.getLogger(__name__)


class wizard_clean_line(models.TransientModel):
    _name = 'wizard.clean'
    _description = 'Wizard add data clean setting lines'

    setting_line_id = fields.Many2one('clean.setting.line', 'Setting_line')
    setting_id = fields.Many2one('clean.setting', 'Setting', related='setting_line_id.setting_id')
    line_ids = fields.One2many('wizard.clean.line', 'wizard_id')

    def apply(self):
        obj = self.env['clean.setting.line']
        for line in self.line_ids:
            record = obj.create({
                'setting_id': self.setting_id.id,
                'model_id': line.model_id.id,
                'sequence': self.setting_line_id.sequence - 1,
            })
            record.onhcnage_model_id()



class wizard_clean_line(models.TransientModel):
    _name = 'wizard.clean.line'
    _rec_name = 'model'
    _description = 'Wizard line'

    wizard_id = fields.Many2one('wizard.clean', 'Wizard')
    selected = fields.Boolean('Selected', default=True)
    model_id = fields.Many2one('ir.model', 'Model')
    model = fields.Char('Model Name')


