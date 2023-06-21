# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class HelpDeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _inherit = ['helpdesk.ticket', 'rk.document.mixin']
