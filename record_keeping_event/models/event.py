# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class EventEvent(models.Model):
    _name = 'event.event'
    _inherit = ['event.event']
    _inherits = {'rk.document': 'rk_id'}

    rk_id = fields.Many2one(
        comodel_name='rk.document',
        help='The record-keeping document of this event',
        ondelete='restrict',
        required=True,
        readonly=True,
        string='Record-keeping Document',
    )
