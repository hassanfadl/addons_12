# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    """
    Overwritting to add complementary contact data fields
    """
    _inherit = "res.partner"

    extra_contact_ids = fields.One2many(
        "extra.contact.info",
        "partner_id",
        string="Misc Contacts",
        limit=2000,
    )
