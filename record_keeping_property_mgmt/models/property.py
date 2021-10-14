# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class PropertyProperty(models.Model):
    _name = 'property.property'
    _inherit = ['property.property']
    _inherits = {'rk.document': 'rk_id'}

    rk_id = fields.Many2one(
        comodel_name='rk.document',
        help='The record-keeping document of this property',
        ondelete='restrict',
        required=True,
        readonly=True,
        string='Record-keeping Document',
    )
