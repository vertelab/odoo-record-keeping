# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _name = 'ir.attachment'
    _inherit = ['ir.attachment', 'mail.thread']
    _inherits = {'rk.document': 'rk_id'}

    rk_id = fields.Many2one(
        comodel_name='rk.document',
        help='Link to corresponding record-keeping document',
        ondelete='restrict',
        required=True,
        readonly=True,
        string='Record-keeping Document',
    )
