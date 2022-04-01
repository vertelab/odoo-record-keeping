# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    allow_create_sale = fields.Boolean(
        default=True,
        help='Allow Sale Order creation',
        string='Allow Create Sale',
    )
