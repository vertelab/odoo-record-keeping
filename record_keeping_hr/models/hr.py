# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee', 'rk.mixin']
    _description = "Employees extended with Record-keeping Mixin"

