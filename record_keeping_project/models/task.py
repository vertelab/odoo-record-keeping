# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class Task(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'rk.document.mixin']
