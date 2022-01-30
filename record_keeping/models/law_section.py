# -*- coding: utf-8 -*-

from odoo import _, fields, models


class LawSection(models.Model):
    """
    In order for a public authority to refuse to disclose information in an of-
    ficial document to a natural or legal person, or any kind of information
    to another public authority, in principle the information must be subject
    to secrecy. The public authority must examine whether there is any secrecy
    provision that may cover the information in question. If there is not, the
    information is public in all circumstances and must be disclosed.
    """
    _name = 'rk.law.section'
    _description = 'Law Section'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'name'

    name = fields.Char(
        help='The name of this secrecy provision',
        required=True,
        string='Name',
        tracking=True,
    )
    description = fields.Html(
        help='The description of this secrecy provision',
        required=True,
        string='Description',
        tracking=True,
    )
    url = fields.Char(
        help='The url of this secrecy provision',
        string='Url',
        tracking=True,
    )
