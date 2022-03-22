# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class Event(models.Model):
    _name = 'event.event'
    _inherit = ['event.event', 'rk.document.mixin']
