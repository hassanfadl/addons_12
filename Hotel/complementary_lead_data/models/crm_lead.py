# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class crm_lead(models.Model):
    """
    Overwritting to add complementary contact data fields
    """
    _inherit = "crm.lead"

    extra_contact_ids = fields.One2many(
        "extra.contact.info",
        "lead_id",
        string="Misc Contacts",
        limit=2000,
    )
