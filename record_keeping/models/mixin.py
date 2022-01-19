# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Mixin(models.AbstractModel):
    _name = 'rk.mixin'
    _description = 'Mixin'

    classification_id = fields.Many2one(
        comodel_name='rk.classification',
        string='Classification',
        default=lambda self: self._default_classification(),
        tracking=True,
    )
    document_type_id = fields.Many2one(
        comodel_name='rk.document.type',
        string='Document Type',
        tracking=True,
    )
    draw_up_date = fields.Date(
        default=False,
        help='The date when the document is ready to be used or sent',
        string='Drawn up',
        tracking=True,
    )
    is_official = fields.Boolean(
        default=False,
        help='Check this option if this document is an official document',
        string='Official document',
        tracking=True,
    )
    is_secret = fields.Boolean(
        default=False,
        help='Check this option if it can be assumed that information contained '
             'in this document should not be disclosed on grounds of secrecy.',
        string='Secrecy marker',
        tracking=True,
    )
    law_section_id = fields.Many2one(
        comodel_name='rk.law.section',
        help='The specified secrecy provision when the document has a secrecy marker',
        string='Secrecy provision',
        tracking=True,
    )
    receive_date = fields.Date(
        default=False,
        help='The date when the document has been received by a competent person.',
        string='Received',
        tracking=True,
    )
    receiver_id = fields.Many2one(
        comodel_name='res.partner',
        help='The competent person who received the document',
        string='Receiver',
        tracking=True,
    )
    secrecy_grounds = fields.Char(
        default=False,
        help='If marked as secret, please provide more information',
        string='Secrecy grounds',
        tracking=True,
    )
    sender_id = fields.Many2one(
        comodel_name='res.partner',
        help='The person who sent this document',
        string='Sender',
        tracking=True,
    )

    _sql_constraints = [
        ('is_secret_requires_provision',
         "CHECK(is_secret IS NOT TRUE OR law_section_id IS NOT NULL)",
         #  "CHECK(is_secret IS NOT TRUE OR (law_section_id IS NOT NULL AND secrecy_grounds IS NOT NULL))",
         'Please provide legal provision')]

    def _default_classification(self):
        ParameterSudo = self.env['ir.config_parameter'].sudo()
        return int(ParameterSudo.get_param('record_keeping.default_classification'))

    @api.onchange('is_official')
    def _onchange_is_official(self):
        if not self.is_official:
            self.is_secret = False

    @api.onchange('is_secret')
    def _onchange_is_secret(self):
        if not self.is_secret:
            self.law_section_id = False
            self.secrecy_grounds = False
