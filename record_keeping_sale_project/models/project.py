# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    allow_sale_project = fields.Boolean(default=True, string='Allow Sale Order creation')