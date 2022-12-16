# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class Mixin(models.AbstractModel):
    _name = 'rk.mixin'
    _description = 'Mixin'

    active = fields.Boolean(
        copy=False,
        default=True,
        string='Archived',
        tracking=True,
    )
    document_type_id = fields.Many2one(
        comodel_name='rk.document.type',
        copy=False,
        string='Document Type',
        tracking=True,
    )
    draw_up_date = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today(),
        help='The date when the document is ready to be used or sent',
        index=True,
        string='Drawn up',
        tracking=True,
    )
    draw_up_receive_date = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today(),
        help='The date when the document is ready to be used or sent',
        index=True,
        string='Drawn up/Received',
        tracking=True,
    )
    is_official = fields.Boolean(
        copy=False,
        default=False,
        help='Check this option if this document is an official document',
        string='Official document',
        tracking=True,
    )
    is_secret = fields.Boolean(
        copy=False,
        default=False,
        help='Check this option if it can be assumed that information contained '
             'in this document should not be disclosed on grounds of secrecy.',
        string='Secrecy marker',
        tracking=True,
    )
    law_section_id = fields.Many2one(
        comodel_name='rk.law.section',
        copy=False,
        help='The specified secrecy provision when the document has a secrecy marker',
        string='Secrecy provision',
        tracking=True,
    )
    receive_date = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today(),
        help='The date when the document has been received by a competent person.',
        index=True,
        string='Received',
        tracking=True,
    )
    receiver = fields.Char(
        copy=False,
        help='The competent person who received the document',
        string='Receiver ',
        tracking=True,
    )
    # THIS FIELD WAS BELIVED TO BE REDUNDANT AND THUS COMMENTED OUT
    # receiver_id = fields.Many2one(
    #     comodel_name='res.partner',
    #     copy=False,
    #     help='The competent person who received the document',
    #     string='Receiver',
    #     tracking=True,
    # )
    secrecy_grounds = fields.Char(
        copy=False,
        default=False,
        help='If marked as secret, please provide more information',
        string='Secrecy grounds',
        tracking=True,
    )
    sender = fields.Char(
        copy=False,
        help='The person who sent this document',
        string='Sender ',
        tracking=True,
    )
    # THIS FIELD WAS BELIVED TO BE REDUNDANT AND THUS COMMENTED OUT
    # sender_id = fields.Many2one(
    #     comodel_name='res.partner',
    #     copy=False,
    #     help='The person who sent this document',
    #     string='Sender',
    #     tracking=True,
    # )

    _sql_constraints = [
        ('is_secret_requires_provision',
         "CHECK(is_secret IS NOT TRUE OR law_section_id IS NOT NULL)",
         #  "CHECK(is_secret IS NOT TRUE OR (law_section_id IS NOT NULL AND secrecy_grounds IS NOT NULL))",
         'Please provide legal provision')]

    def _get_default_classification(self):
        param = 'record_keeping.matter_default_classification_id'
        return int(self.env['ir.config_parameter'].sudo().get_param(param))

    @api.onchange('is_official')
    def _onchange_is_official(self):
        if not self.is_official:
            self.is_secret = False

    @api.onchange('is_secret')
    def _onchange_is_secret(self):
        if not self.is_secret:
            self.law_section_id = False
            self.secrecy_grounds = False
