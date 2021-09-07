from odoo import models, fields, api, _
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)


class AutoVacuumCleaner(models.Model):
    _name = 'auto.vacuum.cleaner'
    _description = 'Auto Vacuum Cleaner'

    name = fields.Char(default='New', readonly=True, copy=False)
    model_id = fields.Many2one('ir.model', 'Model', required=True)
    interval_number = fields.Integer('Interval Number', required=True)
    cleaning_preference = fields.Selection([
        ('delete', 'Permanently Delete'),
        ('archive', 'Archive (Deactivate)')
    ], 'Cleaning Preference', required=True)
    interval_type = fields.Selection([
                        ('minutes', 'Minutes'),
                        ('hours', 'Hours'),
                        ('days', 'Days'),
                        ('weeks', 'Weeks'),
        ], 'Interval Unit', required=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env.ref('vv_auto_vacuum_system.seq_auto_vacuum').next_by_id() or 'New'
        result = super(AutoVacuumCleaner, self).create(vals)
        return result

    @api.onchange('cleaning_preference')
    def onchange_cleaning_preference(self):
        if self.cleaning_preference and self.cleaning_preference == 'archive' and self.model_id and not hasattr(
                self.model_id, 'active'):
            self.cleaning_preference = False
            return {'warning': {'title': _('Invalid Configuration'),
                                'message': _('There is no option to archive the records of selected model.')}}

    @api.multi
    def auto_vacuum_cleaner(self):
        cleaners = self.search([])
        for cleaner in cleaners:
            if cleaner.interval_type == 'minutes':
                older_than = datetime.now() - timedelta(minutes=cleaner.interval_number)
            if cleaner.interval_type == 'hours':
                older_than = datetime.now() - timedelta(hours=cleaner.interval_number)
            if cleaner.interval_type == 'days':
                older_than = datetime.now() - timedelta(days=cleaner.interval_number)
            if cleaner.interval_type == 'weeks':
                older_than = datetime.now() - timedelta(weeks=cleaner.interval_number)

            unwanted_data = self.env[cleaner.model_id.model].search([('create_date', '<', older_than)])
            for data in unwanted_data:
                try:
                    if cleaner.cleaning_preference == 'archive':
                        data.write({'active': False})
                    elif cleaner.cleaning_preference == 'delete':
                        data.unlink()
                except Exception as e:
                    _logger.warning("Unable to clean the {0} : {1}".format(data.name, e))
                    continue
        return True
