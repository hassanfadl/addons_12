# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class extra_contact_info(models.Model):
    """
    Overwritting to add link to crm.lead
    """
    _inherit = "extra.contact.info"

    lead_id = fields.Many2one(
        "crm.lead",
        ondelete="cascade",
    )
