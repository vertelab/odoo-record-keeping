# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Project(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'rk.document.mixin']
    _inherits = {'rk.document': 'document_id'}
