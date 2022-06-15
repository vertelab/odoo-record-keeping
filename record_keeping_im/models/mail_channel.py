# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class MailChannel(models.Model):
    _name = 'mail.channel'
    _inherit = ['mail.channel', 'rk.document.mixin']
