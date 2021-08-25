# -*- coding: utf-8 -*-

import logging

from werkzeug import urls

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

MAXSHORTNAMESIZE = 24
# Favicon, Name for user, Url type
FAVICONS = [
    ("fa-phone", "Phone", "phone",),
    ("fa-volume-control-phone", "Mobile", "phone",),
    ("fa-envelope-square", "Email", "mail",),
    ("fa-globe", "Website", "url",),
    ("fa-skype", "Skype", "skype",),
    ("fa-whatsapp", "Whatsapp", "whatsapp"),
    ("fa-telegram", "Telegram", "telegram"),
    ("fa-slack", "Slack", "url"),
    ("fa-linkedin", "LinkedIn", "url",),
    ("fa-facebook-official", "Facebook", "url",),
    ("fa-twitter", "Twitter", "url",),
    ("fa-youtube", "Youtube", "url",),
    ("fa-google-plus", "Google Plus", "url",),
    ("fa-vk", "Vkontakte", "url",),
    ("fa-instagram", "Instagram", "url",),
    ("fa-pinterest", "Pinterest", "url",),
    ("fa-twitch", "Twitch", "url",),
    ("fa-github", "Github", "url",),
    ("fa-link", "Misc Urls", "url",),
    ("fa-tag", "Misc", "no",),
]


def _shorten_name(name):
    """
    Method to return shorten name for visibility purposes

    We do not use display_name, since in case of update it is not shown in real time
    We do not use compute since in our widget we do not have depends

    Args:
     * name - char

    Returns:
     * char
    """
    short_name = name and len(name) > MAXSHORTNAMESIZE and name[:MAXSHORTNAMESIZE] + ".." or name
    return short_name

class extra_contact_info(models.Model):
    """
    Introducing the model to keep a unit of contact info
    Example: extra phone number or social network link

    To-do:
     * amend csv rules
    """
    _name = "extra.contact.info"
    _description = "Complementary Contact Info"

    @api.model
    def _return_contact_info_type(self):
        """
        Return available contact info type
        """
        return [fav[:-1] for fav in FAVICONS]

    @api.model
    def _return_url_type(self):
        """
        Return available url types
        """
        return [(fav[-1], fav[-1]) for fav in FAVICONS]

    @api.multi
    def _inverse_name(self):
        """
        Inverse method for name

        Methods:
         * _shorten_name
         * _add_http_to_url
        """
        for info in self:
            info._add_http_to_url()
            info.short_name = _shorten_name(name=info.name)

    @api.multi
    def _inverse_contact_info_type(self):
        """
        Inverse method for contact_info_type

        Methods:
         * _return_favicon_url_type
         * _add_http_to_url
        """
        for info in self:
            info._add_http_to_url()
            info.url_type = info._return_favicon_url_type()

    @api.multi
    @api.onchange("name")
    def _onchange_name(self):
        """
        Onchanges method for name

        Methods:
         * _shorten_name
         * _add_http_to_url
        """
        for info in self:
            info._add_http_to_url()
            info.short_name = _shorten_name(name=info.name)

    @api.multi
    @api.onchange("contact_info_type")
    def _onchange_contact_info_type(self):
        """
        Onchanges method for contact_info_type

        Methods:
         * _return_favicon_url_type
         * _add_http_to_url
        """
        for info in self:
            info.url_type = info._return_favicon_url_type()
            info._add_http_to_url()

    contact_info_type = fields.Selection(
        _return_contact_info_type,
        string="Type",
    )
    url_type = fields.Selection(
        _return_url_type,
        string="Url type",
        help="We introduce it to simplify qweb rendering. T-if doesn't support 'in' operator",
    )
    name = fields.Char(
        string="Contact info",
        required="1",
    )
    short_name = fields.Char(
        string="Short name",
    )
    comment = fields.Char(string="Comment")
    partner_id = fields.Many2one(
        "res.partner",
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        help="""
            The lesser the closer to the top this contact info will be shown.
            Use it in case you would like to re-arrange the list of contacts.
        """,
    )

    @api.multi
    def _return_favicon_url_type(self):
        """
        Method to return favicon url type

        Returns:
         * char (possible key of url_type)

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        url_type = "no"
        for fav in FAVICONS:
            if fav[0] == self.contact_info_type:
                url_type = fav[-1]
                break
        return url_type

    _order = "sequence, id"

    @api.multi
    def _add_http_to_url(self):
        """
        The method to add http:// to urls which lack it
        """
        for info in self:
            if info.name and info.url_type == "url":
                    # and not info.name.startswith("http://") \
                    # and not info.name.startswith("https://"):
                info.name = self._clean_website(clean_url=info.name)

    @api.model
    def _clean_website(self, clean_url):
        """
        Method helper to make url clickable (add http:// if needed)

        Args:
         * clean_url - char

        Returns:
         * char
        """
        url = urls.url_parse(clean_url)
        if not url.scheme:
            if not url.netloc:
                url = url.replace(netloc=url.path, path='')
            clean_url = url.replace(scheme='http').to_url()
        return clean_url


