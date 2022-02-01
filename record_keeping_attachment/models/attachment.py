# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Attachment(models.Model):
    _name = 'ir.attachment'
    _inherit = ['ir.attachment', 'mail.thread', 'rk.document.mixin']
    _inherits = {'rk.document': 'document_id'}
