# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee']
    _inherits = {'rk.document': 'rk_id'}

    rk_id = fields.Many2one(
        comodel_name='rk.document',
        help='The record-keeping document of this employee',
        ondelete='restrict',
        required=True,
        readonly=True,
        string='Record-keeping Document',
    )
