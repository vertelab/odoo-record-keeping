# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class Account(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'rk.document.mixin']
