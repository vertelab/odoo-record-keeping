# -*- coding: utf-8 -*-

import logging

from datetime import datetime
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class RecordKeepingMixin(models.AbstractModel):
    _name = 'rk.mixin'
    _description = "Inherit this to add record keeping features"

    active = fields.Boolean(
        default=True,
        help='True if the document is visible. ',
        string='Active',
    )
    drawn_up_date = fields.Date(
        default=datetime.now().date(),
        help='The date when the document is ready to be used or sent',
        string='Drawn up',
    )
    is_secret = fields.Boolean(
        default=False,
        help='Check this option if it can be assumed that information contained '
             'in this document should not be disclosed on grounds of secrecy.',
        string='Secrecy marker',
    )
    is_official_document = fields.Boolean(
        default=False,
        help='Check this option if this document is an official document',
        string='Official document',
    )
    received_date = fields.Date(
        default=datetime.now().date(),
        help='The date when the document has been received by a competent person.',
        string='Received',
    )
    receiver_id = fields.Many2one(
        comodel_name='res.partner',
        string='Receiver',
    )
    sender_id = fields.Many2one(
        comodel_name='res.partner',
        help='A partner designated as sender',
        string='Sender',
    )
