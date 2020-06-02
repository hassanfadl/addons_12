import datetime
import logging
import threading
from ast import literal_eval

from odoo import models, api

_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def process_email_queue(self, ids=None):
        """ Replace method process_email_queue
            Send immediately queued messages, committing after each
               message is sent - this is not transactional and should
               not be called during another transaction!

               :param list ids: optional list of emails ids to send. If passed
                                no search is performed, and these ids are used
                                instead.
               :param dict context: if a 'filters' key is present in context,
                                    this value will be used as an additional
                                    filter to further restrict the outgoing
                                    messages to send (by default all 'outgoing'
                                    messages are sent).
        """
        limit = 10
        try:
            params = self.env['ir.config_parameter'].sudo()
            limit = literal_eval(params.get_param('mail_limit'))
        except Exception as e:
            _logger.error(str(e))

        filters = ['&',
                   ('state', '=', 'outgoing'),
                   '|',
                   ('scheduled_date', '<', datetime.datetime.now()),
                   ('scheduled_date', '=', False)]
        if 'filters' in self._context:
            filters.extend(self._context['filters'])
        # TODO: make limit configurable
        filtered_ids = self.search(filters, limit=limit).ids
        if not ids:
            ids = filtered_ids
        else:
            ids = list(set(filtered_ids) & set(ids))
        ids.sort()

        res = None
        try:
            # auto-commit except in testing mode
            auto_commit = not getattr(threading.currentThread(), 'testing', False)
            res = self.browse(ids).send(auto_commit=auto_commit)
        except Exception:
            _logger.exception("Failed processing mail queue")
        return res
