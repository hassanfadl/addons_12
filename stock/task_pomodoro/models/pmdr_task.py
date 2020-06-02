# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import models, fields, api, exceptions, _


def to_datetime(odoo_dt_field):
    # raise exceptions.ValidationError('Type %r, %s' %
    #         (type(odoo_dt_field), odoo_dt_field))
    # Odoo 12: Type <class 'datetime.datetime'>, 2019-04-01 08:32:59.496646 
    # Odoo 11: Type <class 'str'>, 2019-04-01 07:53:53
    if isinstance(odoo_dt_field, datetime):
        return odoo_dt_field
    else: pass

    return datetime.strptime(str(odoo_dt_field), '%Y-%m-%d %H:%M:%S')


class User(models.Model):
    _inherit = 'res.users'

    pmdr_focus_length = fields.Integer(string='Focus', default=25)
    pmdr_short_length = fields.Integer(string='Short', default=5)
    pmdr_long_length = fields.Integer(string='Long', default=15)
    pmdr_max_running = fields.Integer(string='Max Running', default=4)

    def reset_default_pmdr(self):
        self.pmdr_focus_length = 25
        self.pmdr_short_length = 5
        self.pmdr_long_length = 15
        self.pmdr_max_running = 4


class Task(models.Model):
    _inherit = 'project.task'

    pmdr_count = fields.Integer(string='Pomodoros', readonly=False, copy=False)
    pmdr_running = fields.Integer(string='Running Count', readonly=True, copy=False)
    pmdr_status = fields.Selection(string='Pomodoro Status',
            readonly=True, copy=False,
            default='Stop', selection=[
                ('Stop', 'Stop'),
                ('Focus', 'Focus'),
                ('Short', 'Short'),
                ('Long', 'Long'),
                ('PFocus', 'Pause Focus'),
                ('PShort', 'Pause Short'),
                ('PLong', 'Pause Long'),
                ])
    pmdr_start = fields.Datetime(string='Started at',
            readonly=True, copy=False)
    pmdr_pause = fields.Datetime(string='Paused at', readonly=True, copy=False)
    pmdr_remaining_secs = fields.Integer(string='Remaining seconds',
            compute='_compute_remaining')

    pmdr_timestamp = fields.Integer(string='Timestamp',
            compute='_compute_timestamp')

    @property
    def duration(self):
        try:
            self._duration
        except AttributeError:
            self._duration = {
                'Focus': self.env.user.pmdr_focus_length,
                'Short': self.env.user.pmdr_short_length,
                'Long': self.env.user.pmdr_long_length,
            }
        return self._duration

    @property
    def max_running(self):
        return self.env.user.pmdr_max_running

    @api.depends('pmdr_start', 'pmdr_status')
    def _compute_remaining(self):
        for row in self:
            status = self.pmdr_status
            if status in ['Focus', 'Short', 'Long']: pass
            else:
                self.pmdr_remaining_secs = 0
                continue
            pmdr_start = to_datetime(self.pmdr_start)

            lapsed = (fields.datetime.now() - pmdr_start).total_seconds()
            self.pmdr_remaining_secs = self.duration[status]*60 - lapsed

    # Deprecated from 12.0, removed from 13.0 @api.one
    def _compute_timestamp(self):
        for row in self:
            row.pmdr_timestamp = fields.datetime.now().timestamp()

    def action_start_pomodoro(self):
        self.write({
            'pmdr_running': 0,
            'pmdr_start': fields.datetime.now(),
            'pmdr_status': 'Focus',
            'pmdr_pause': None,
            })

    def action_update_pomodoro(self):
        status = self.pmdr_status
        duration = self.duration[status]
        kwarg = {'minutes': duration}
        # For testing
        # kwarg = {'seconds': duration}
        pmdr_start = to_datetime(self.pmdr_start)
        pmdr_end = pmdr_start + timedelta(**kwarg)
        if fields.datetime.now() > pmdr_end: pass
        else: return

        new_pmdr = {
                'pmdr_start': fields.datetime.now(),
                }
        if status == 'Focus':
            new_running = self.pmdr_running + 1
            if new_running < self.max_running:
                new_status = 'Short'
            else:
                new_running = 0
                new_status = 'Long'
            new_pmdr.update({
                'pmdr_running': new_running,
                'pmdr_count': self.pmdr_count + 1,
                })
        else:
            new_status = 'Focus'
        new_pmdr['pmdr_status'] = new_status
        self.write(new_pmdr)

    def action_pause_pomodoro(self):
        prefix = 'P'
        status = self.pmdr_status
        pausing = status in ['PFocus', 'PShort', 'PLong']
        if pausing:
            pmdr_start = to_datetime(self.pmdr_start)
            pmdr_pause = to_datetime(self.pmdr_pause)
            new_pmdr = {
                'pmdr_start': fields.datetime.now()
                        - (pmdr_pause - pmdr_start),
                'pmdr_status': status[len(prefix):],
                'pmdr_pause': None,
                }
        else:
            new_pmdr = {
                'pmdr_status': prefix + status,
                'pmdr_pause': fields.datetime.now(),
                }
        self.write(new_pmdr)

    def action_stop_pomodoro(self):
        self.write({
            'pmdr_pause': fields.datetime.now(),
            'pmdr_status': 'Stop',
            })
