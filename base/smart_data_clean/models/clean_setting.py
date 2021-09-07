# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)

Not_Clean_Models = [
    'res.config.settings',
    'mail.message.subtype',
]


class CleanSetting(models.Model):
    _name = 'clean.setting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Data Clean Setting'

    name = fields.Char('Name', required=True)
    line_ids = fields.One2many('clean.setting.line', 'setting_id', 'Lines')

    def apply_clean(self):
        now = fields.datetime.now().strftime(DTF)

        try:
            self.line_ids.clean_data()
            self.message_post('Clean data success at %s' % now)
        except Exception as e:
            raise Warning(str(e))
            # self.message_post('Clean data fail at %s, error: %s' % (now, str(e)))


class CleanSettingLine(models.Model):
    _name = 'clean.setting.line'
    _order = 'sequence,id'
    _description = 'Clean Setting Line'

    def compute_have_xml_data(self):
        for one in self:
            if self.env['ir.model.data'].search_count([('model', '=', one.model)]):
                one.have_xml_data = True
            else:
                one.have_xml_data = False

    sequence = fields.Integer('Sequence', default=10)
    setting_id = fields.Many2one('clean.setting', "Setting")
    model_id = fields.Many2one('ir.model', 'Model')
    model = fields.Char('Model Name', related='model_id.model')
    have_xml_data = fields.Boolean('There are XML records', compute=compute_have_xml_data)
    clean_xml_data = fields.Boolean('Force clean XML records', default=False)
    need_cascade = fields.Boolean('cascade clean relation tables')

    _sql_constraints = [
        ('line_unique', 'unique(setting_id, model_id)', "The model of the setting must be unique"),
    ]

    @api.onchange('model_id')
    def onhcnage_model_id(self):
        if self.env['ir.model.data'].search_count([('model', '=', self.model_id.model)]):
            self.need_cascade = False
        else:
            self.need_cascade = True

    def get_fkey_model(self):

        exist_models = self.setting_id.line_ids.mapped('model')

        line_obj = self.env['wizard.clean.line']
        wizard = self.env['wizard.clean'].create({'setting_line_id': self.id})
        models = self.env['ir.model.fields'].search([('ttype', '=', 'many2one'),
                                                     ('relation', '=', self.model),
                                                     ('model', 'not like', 'ir.'),
                                                     ('model', 'not in', Not_Clean_Models),
                                                     ('model', 'not in', exist_models),
                                                     ('model_id.transient', '!=', True),
                                                     ('store', '=', True)
                                                     ]).mapped('model_id')

        for m in models:
            obj = self.env[m.model]
            if obj._auto:
                line_obj.create({
                    'wizard_id': wizard.id,
                    'model_id': m.id,
                    'model': m.model,
                })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Add data clean setting lines',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.clean',
            'target': 'new',
            'res_id': wizard.id,
        }

    def clean_data(self):
        for one in self:
            _logger.info('==clean_data==%s',  one.model)

            tb_name = self.env[one.model]._table

            if one.have_xml_data:
                xml_records = self.env['ir.model.data'].search([('model', '=', one.model)])
                res_ids = xml_records.mapped('res_id')
                query = "DELETE FROM %s WHERE id NOT IN %s" % tb_name
                tb_name_ids = [tuple(res_ids)]
                self._cr.execute(query, tb_name_ids)
            else:
                query = "DELETE FROM %s" % tb_name
                self._cr.execute(query)



            # else:
            #     query = """ TRUNCATE TABLE %s """ % tb_name
            #     # if one.need_cascade:
            #     #     query += ' CASCADE'
            #
            #     _logger.debug('==clean_data== %s', query)
            #     self._cr.execute(query)
