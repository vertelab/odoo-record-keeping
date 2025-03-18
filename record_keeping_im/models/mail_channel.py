# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class MailChannel(models.Model):
    _name = 'discuss.channel'
    _inherit = ['discuss.channel', 'rk.document.mixin']
