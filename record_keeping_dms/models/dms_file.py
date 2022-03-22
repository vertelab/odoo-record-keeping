# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class File(models.Model):
    _name = 'dms.file'
    _inherit = ['dms.file', 'rk.document.mixin']
